import numpy as np
import librosa

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)

    # MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfccs_mean = np.mean(mfccs.T, axis=0)

    # Chroma
    stft = np.abs(librosa.stft(y))
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
    chroma_mean = np.mean(chroma.T, axis=0)

    # Mel Spectrogram
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_mean = np.mean(mel.T, axis=0)

    # Spectral Contrast
    contrast = librosa.feature.spectral_contrast(S=stft, sr=sr)
    contrast_mean = np.mean(contrast.T, axis=0)

    # Root Mean Square Energy (RMSE)
    rmse = librosa.feature.rms(y=y)
    rmse_mean = np.mean(rmse.T, axis=0)

    # Concatenate all features
    features = np.hstack((mfccs_mean, chroma_mean, mel_mean, contrast_mean, rmse_mean))
    return features

features_df = extract_features()