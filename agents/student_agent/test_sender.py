from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from student_agent import TranslationRequest, TranslationResponse

# Create sender agent
sender = Agent(
    name="sender",
    port=8001,
    seed="sender_secret_phrase",
    endpoint=[f"http://127.0.0.1:8001/submit"]
)

# Fund the agent if needed
fund_agent_if_low(sender.wallet.address())

# Store the student agent address from your running instance
STUDENT_AGENT_ADDRESS = "agent1qw2hlxxqvk9v8g32726gj8qcze6tz7nrd8f8skhzchuamrxw3wlfupzylyu" 
 # Update this with your student agent's actual address

@sender.on_interval(period=5.0)
async def send_translation_request(ctx: Context):
    # Create translation request
    request = TranslationRequest(
        text="Hello, world!",
        source_language=""
    )
    
    # Send to student agent
    ctx.logger.info(f"Sending request to student agent at {STUDENT_AGENT_ADDRESS}")
    await ctx.send(STUDENT_AGENT_ADDRESS, request)
    ctx.logger.info(f"Sent translation request: {request}")

@sender.on_message(model=TranslationResponse)
async def handle_response(ctx: Context, sender_address: str, msg: TranslationResponse):
    """Handle responses from the student agent"""
    ctx.logger.info(f"Received response from {sender_address}: {msg.message}")

if __name__ == "__main__":
    sender.run() 