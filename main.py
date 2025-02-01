from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import uvicorn
import logging

# Configurar logging para depuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/subtitles/{video_id}")
async def get_subtitles(video_id: str):
    try:
        logger.info(f"Solicitando subtítulos para el video: {video_id}")

        # Intentar obtener la lista de subtítulos
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except TranscriptsDisabled:
            raise HTTPException(status_code=404, detail="Los subtítulos están deshabilitados para este video.")
        except NoTranscriptFound:
            raise HTTPException(status_code=404, detail="No se encontraron subtítulos para este video.")
        except Exception as e:
            logger.error(f"Error al obtener subtítulos: {e}")
            raise HTTPException(status_code=500, detail="Error inesperado al intentar recuperar los subtítulos.")

        # Intentar primero con subtítulos manuales
        for transcript in transcript_list:
            if not transcript.is_generated:
                try:
                    subtitles = transcript.fetch()
                    full_text = " ".join([entry["text"] for entry in subtitles])
                    return {
                        "video_id": video_id,
                        "language": transcript.language,
                        "generated": False,
                        "text": full_text
                    }
                except Exception as e:
                    logger.warning(f"Error al obtener subtítulos manuales: {e}")
                    continue

        # Si no hay subtítulos manuales, intentar con los generados automáticamente
        for transcript in transcript_list:
            if transcript.is_generated:
                try:
                    subtitles = transcript.fetch()
                    full_text = " ".join([entry["text"] for entry in subtitles])
                    return {
                        "video_id": video_id,
                        "language": transcript.language,
                        "generated": True,
                        "text": full_text
                    }
                except Exception as e:
                    logger.warning(f"Error al obtener subtítulos automáticos: {e}")
                    continue

        # Si no hay subtítulos disponibles
        raise HTTPException(status_code=404, detail="No subtitles available for this video.")

    except HTTPException as http_exc:
        raise http_exc  # Mantiene el código de error HTTP correcto
    except Exception as e:
        logger.error(f"Error inesperado en la API: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
