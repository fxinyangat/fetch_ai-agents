from uagents import Agent, Context, Protocol
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

# Initialize the Student Agent
student_agent = Agent(
    name=CONFIG["agent_name"],
    port=CONFIG["port"],
    endpoint=["http://127.0.0.1:8000/submit"]
)

@student_agent.on_message(TranslationRequest)
async def handle_translation_request(ctx: Context, message: TranslationRequest):
    """
    Handles translation requests and forwards them to the Broker Agent.
    """
    try:
        broker_address = CONFIG["broker_address"]
        ctx.logger.info(f"Sending translation request to broker at {broker_address}")
        
        response = await ctx.send(broker_address, message)
        
        if response:
            ctx.logger.info(f"Received response from broker: {response}")
        else:
            ctx.logger.warning("No response received from broker")
            
    except Exception as e:
        ctx.logger.error(f"Error communicating with broker: {str(e)}")

if __name__ == "__main__":
    fund_agent_if_low(student_agent.wallet.address())
    student_agent.run()