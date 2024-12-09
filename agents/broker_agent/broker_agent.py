from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
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

# Initialize the Broker Agent
broker_agent = Agent(
    name=CONFIG["agent_name"],
    port=CONFIG["port"],
    endpoint=[f"http://{CONFIG['host']}:{CONFIG['port']}/submit"],
)

@broker_agent.on_message(TranslationRequest)
async def handle_translation_request(ctx: Context, sender: str, msg: dict):
    """
    Handles translation requests from the Student Agent.
    """
    try:
        ctx.logger.info(f"Received translation request from {sender}")
        ctx.logger.info(f"Request content: {msg}")
        
        # Get translation agent address from config
        translation_address = CONFIG.get("translation_agent_address")
        
        if not translation_address:
            error_response = TranslationResponse(
                translated_text="",
                error="Translation agent address not configured"
            )
            await ctx.send(sender, error_response)
            return
            
        # Forward to translation agent
        response = await ctx.send(translation_address, msg)
        
        if response and hasattr(response, 'status') and response.status == 'delivered':
            ctx.logger.info(f"Message delivered to Translation Agent")
            # Send acknowledgment as Pydantic object
            ack_response = TranslationResponse(
                translated_text="Message forwarded to translation service",
                error=""
            )
            await ctx.send(sender, ack_response)
        else:
            error_response = TranslationResponse(
                translated_text="",
                error="Failed to reach translation agent"
            )
            await ctx.send(sender, error_response)
            
    except Exception as e:
        ctx.logger.error(f"Error: {str(e)}")
        error_response = TranslationResponse(
            translated_text="",
            error=str(e)
        )
        await ctx.send(sender, error_response)

if __name__ == "__main__":
    fund_agent_if_low(broker_agent.wallet.address())
    broker_agent.run()