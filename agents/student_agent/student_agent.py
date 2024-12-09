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

# Create protocol for translation
translation_protocol = Protocol()

# Initialize the Student Agent with correct endpoint
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
        # Get broker address from config
        broker_address = CONFIG["broker_address"]
        
        ctx.logger.info(f"Sending translation request to broker at {broker_address}")
        
        # Convert the message to a dictionary and add preferred language
        message_dict = message.dict()
        message_dict["preferred_language"] = CONFIG["preferred_language"]

        # Send to broker
        response = await ctx.send(broker_address, message_dict)
        
        if response:
            ctx.logger.info(f"Received response from broker: {response}")
        else:
            ctx.logger.warning("No response received from broker")
            
    except Exception as e:
        ctx.logger.error(f"Error communicating with broker: {str(e)}")

# Add a periodic test message
@translation_protocol.on_interval(period=5.0)
async def send_test_message(ctx: Context):
    try:
        broker_address = CONFIG["broker_address"]
        
        # Create message using TranslationRequest model
        test_message = TranslationRequest(
            text="How are you today?",
            source_language="en",
            preferred_language="fr"
        )
        
        ctx.logger.info("🔄 TEST: Sending translation request to broker")
        ctx.logger.info(f"📤 Message: {test_message.dict()}")  # Use dict() for logging only
        
        response = await ctx.send(
            broker_address,
            test_message,  # Send the Model object
            timeout=10
        )
        
        if response:
            ctx.logger.info(f"✅ TEST: Received response: {response}")
        else:
            ctx.logger.warning("❌ TEST: No response received")
            
    except Exception as e:
        ctx.logger.error(f"❌ TEST: Error during test: {str(e)}")
        ctx.logger.error(f"Error type: {type(e)}")
        ctx.logger.error(f"Error details: {str(e)}")

# Include the protocol
student_agent.include(translation_protocol)

# Run the Student Agent
if __name__ == "__main__":
    fund_agent_if_low(student_agent.wallet.address())
    student_agent.run()