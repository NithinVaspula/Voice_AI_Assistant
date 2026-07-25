from gtts import gTTS
import os

def text_to_speech(text):

    os.makedirs("audio", exist_ok=True)

    output_path = "audio/response.mp3"

    tts = gTTS(
        text=text,
        lang="en",
        slow=False
    )

    tts.save(output_path)

    return output_path