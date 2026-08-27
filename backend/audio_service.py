import pyttsx3
from io import BytesIO
import base64

class AudioService:
    """Handles text-to-speech conversion"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed
        self.engine.setProperty('volume', 0.9)  # Volume
    
    def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech and return audio bytes"""
        
        try:
            # Create BytesIO object to store audio
            audio_buffer = BytesIO()
            
            # Save to buffer
            self.engine.save_to_file(text, 'temp_audio.mp3')
            self.engine.runAndWait()
            
            # Read the file and return as bytes
            with open('temp_audio.mp3', 'rb') as f:
                audio_data = f.read()
            
            return audio_data
        except Exception as e:
            print(f"[Audio] TTS Error: {e}")
            return b""
    
    def text_to_speech_base64(self, text: str) -> str:
        """Convert text to speech and return as base64 string"""
        
        audio_bytes = self.text_to_speech(text)
        if audio_bytes:
            return base64.b64encode(audio_bytes).decode('utf-8')
        return ""

# Initialize service
audio_service = AudioService()