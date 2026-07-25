import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError, ClientError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_gemini(prompt):

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            return response.text

        except ServerError:
            if attempt < 2:
                time.sleep(5)
            else:
                return "⚠️ Gemini servers are busy. Please try again in a minute."

        except ClientError as e:
            return f"❌ API Error:\n{e}"


def transcribe_audio(audio_path):

    uploaded_file = client.files.upload(file=audio_path)

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=[
                    "Generate an accurate transcript of the speech in this audio. Return only the spoken words.",
                    uploaded_file,
                ],
            )

            return response.text

        except ServerError:
            if attempt < 2:
                time.sleep(5)
            else:
                return "⚠️ Gemini servers are busy. Please try again in a minute."

        except ClientError as e:
            return f"❌ API Error:\n{e}"