from google.cloud import translate_v2 as translate
import os

# Set up credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud/google_credentials.json"

def translate_text(text, target_language="es"):
    """
    Translates text using Google Cloud Translate API.
    Args:
        text (str): Text to translate.
        target_language (str): Language code for translation.
    Returns:
        str: Translated text.
    """
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

# Test the function
if __name__ == "__main__":
    print(translate_text("Hello, world!", "es"))