import xgboost as xgb

def predict(features_df):
    emotion_map = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

    model = xgb.XGBClassifier()
    model.load_model("xgb_model.json")  # Assumes you have a saved XGBoost model

    predictions = model.predict(features_df)
    return emotion_map[predictions[0]]
