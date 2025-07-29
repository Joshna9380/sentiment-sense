from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from typing import List

app = FastAPI()

# Allow CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text: str):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        label = 'Positive'
    elif compound <= -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'
    return {"label": label, "confidence": abs(compound), "scores": scores}

@app.post("/analyze")
def analyze_text(text: str = Form(...)):
    result = get_sentiment(text)
    return {"text": text, **result}

@app.post("/analyze_csv")
def analyze_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    if 'text' not in df.columns:
        return {"error": "CSV must have a 'text' column."}
    results = []
    for t in df['text']:
        sentiment = get_sentiment(str(t))
        results.append({"text": t, **sentiment})
    return {"results": results} 