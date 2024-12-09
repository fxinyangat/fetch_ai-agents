from google.cloud import translate_v2 as translate
import os

# Set up credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud/google_credentials.json"

def test_translation():
    try:
        # Create the client
        translate_client = translate.Client()
        
        # Test text
        text = "Hello, this is a test message!"
        target_language = "es"
        
        # Test 1: With source language specified
        result1 = translate_client.translate(
            text,
            target_language=target_language,
            source_language="en"
        )
        print("\nTest 1 - With source language:")
        print(f"Original text: {text}")
        print(f"Translated text: {result1['translatedText']}")
        
        # Test 2: Without source language (auto-detect)
        result2 = translate_client.translate(
            text,
            target_language=target_language
        )
        print("\nTest 2 - Auto-detect language:")
        print(f"Original text: {text}")
        print(f"Translated text: {result2['translatedText']}")
        print(f"Detected language: {result2['detectedSourceLanguage']}")
        
    except Exception as e:
        print(f"Error during translation test: {str(e)}")

if __name__ == "__main__":
    test_translation()