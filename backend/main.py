from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
import shutil
import os
import uuid
import numpy as np
import asyncio

from generate_features import extract_features
from predict import predict
from generate_transcript import generate_transcript
from llm import get_chatbot_response
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    temp_input_path = f"temp_{uuid.uuid4().hex}.webm"
    temp_output_path = f"converted_{uuid.uuid4().hex}.wav"

    with open(temp_input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        audio = AudioSegment.from_file(temp_input_path, format="webm")
        audio.export(temp_output_path, format="wav")
    except Exception as e:
        return {"response": f"Failed to convert audio: {str(e)}"}

    os.remove(temp_input_path)

    features = extract_features(temp_output_path)
    features = np.array(features).reshape(1, -1)

    detected_emo = predict(features)
    print("Predicted output:", detected_emo)

    print("Calling transcripting from main.py..")
    audio_text = await asyncio.to_thread(generate_transcript, temp_output_path)
    print("Done transcripting..")
   # audio_text = generate_transcript(temp_output_path)
    print(audio_text)
    response = get_chatbot_response(audio_text, detected_emo)
    return {"response": response}
