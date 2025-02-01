from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
import uvicorn

app = FastAPI()

@app.get("/subtitles/{video_id}")
async def get_subtitles(video_id: str):
    try:
        # Obtener lista de subtítulos disponibles
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Intentar primero con subtítulos manuales
        for transcript in transcript_list:
            if not transcript.is_generated:  # Verifica si es manual
                try:
                    subtitles = transcript.fetch()
                    return {
                        "video_id": video_id,
                        "language": transcript.language,
                        "generated": False,
                        "subtitles": subtitles
                    }
                except Exception:
                    continue

        # Si no hay subtítulos manuales, intentar con los generados automáticamente
        for transcript in transcript_list:
            if transcript.is_generated:  # Verifica si es automático
                try:
                    subtitles = transcript.fetch()
                    return {
                        "video_id": video_id,
                        "language": transcript.language,
                        "generated": True,
                        "subtitles": subtitles
                    }
                except Exception:
                    continue

        # Si no hay subtítulos disponibles en absoluto
        raise HTTPException(status_code=404, detail="No subtitles available for this video.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

