from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
import uvicorn

app = FastAPI()

@app.get("/subtitles/{video_id}")
async def get_subtitles(video_id: str, lang: str = "es"):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        return {"video_id": video_id, "subtitles": transcript}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
