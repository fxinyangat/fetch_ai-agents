from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from google.cloud import translate_v2 as translate
import json
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import TranslationRequest, TranslationResponse

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH) as config_file:
    CONFIG = json.load(config_file)

# Initialize Google Cloud Translation client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CONFIG.get("google_credentials_path", "cloud/google_credentials.json")
translate_client = translate.Client()

# Initialize Translation Agent
translation_agent = Agent(
    name=CONFIG["agent_name"],
    port=CONFIG["port"],
    endpoint=[f"http://{CONFIG['host']}:{CONFIG['port']}/submit"],
)

@translation_agent.on_message(TranslationRequest)
async def handle_translation(ctx: Context, sender: str, msg: TranslationRequest):
    """
    Handles translation requests using Google Cloud Translation API.
    """
    try:
        ctx.logger.info(f"Received translation request from {sender}")
        ctx.logger.info(f"Request content: {msg.dict()}")
        
        # Call Google Translate API
        result = translate_client.translate(
            msg.text,
            target_language=msg.preferred_language,
            source_language=msg.source_language
        )
        
        # Create response using TranslationResponse model
        response = TranslationResponse(
            translated_text=result["translatedText"],
            error=""
        )
        
        ctx.logger.info(f"Sending response: {response.dict()}")  # Use dict() for logging only
        await ctx.send(sender, response)  # Send the Model object
            
    except Exception as e:
        ctx.logger.error(f"Translation error: {str(e)}")
        error_response = TranslationResponse(
            translated_text="",
            error=f"Translation failed: {str(e)}"
        )
        await ctx.send(sender, error_response)

if __name__ == "__main__":
    fund_agent_if_low(translation_agent.wallet.address())
    translation_agent.run()