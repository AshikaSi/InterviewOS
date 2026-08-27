import os
import base64
from io import BytesIO

class STTService:
    """Speech-to-Text - Placeholder for future ML integration"""
    
    def __init__(self):
        # Using browser's Web Speech API for now (no backend needed)
        pass
    
    def transcribe_from_bytes(self, audio_bytes: bytes) -> str:
        """
        For now, return placeholder.
        In production, integrate with:
        - AssemblyAI (free tier available)
        - Deepgram (free tier available)  
        - Stripe's Whisper alternative
        - Or use Google Cloud Speech-to-Text free tier
        """
        try:
            # Just acknowledge receipt for now
            return "Audio received. Using browser speech recognition."
        except Exception as e:
            print(f"[STT] Error: {e}")
            return ""

stt_service = STTService()