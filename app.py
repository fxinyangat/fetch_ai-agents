from flask import Flask, request, jsonify, render_template
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
import json
import os
import asyncio
import queue
import time
from models import TranslationRequest, TranslationResponse

app = Flask(__name__)

# Load student agent config
CONFIG_PATH = os.path.join("agents", "student_agent", "config.json")
with open(CONFIG_PATH) as config_file:
    CONFIG = json.load(config_file)

# Create protocol for web requests
web_protocol = Protocol()

# Create a queue for pending requests
request_queue = queue.Queue()

# Store translation responses with request IDs
translation_responses = {}

# Initialize student agent with unique name and port
student_agent = Agent(
    name="web_student_agent_" + os.urandom(4).hex(),
    port=8004,
    endpoint=["http://127.0.0.1:8004/submit"]
)

@web_protocol.on_message(TranslationResponse)
async def handle_response(ctx: Context, sender: str, msg: TranslationResponse):
    """Handle translation responses"""
    print(f"Received translation response: {msg.dict()}")  # Debug log
    # Only store if it's an actual translation (not just an acknowledgment)
    if msg.translated_text != "Message forwarded to translation service":
        translation_responses[sender] = msg.translated_text
        ctx.logger.info(f"Received translation: {msg.translated_text}")
        print(f"Current translations: {translation_responses}")  # Debug log

@web_protocol.on_interval(period=0.1)
async def process_requests(ctx: Context):
    """Process translation requests from the queue"""
    try:
        while not request_queue.empty():
            request = request_queue.get_nowait()
            print(f"Processing request: {request.dict()}")  # Debug log
            await ctx.send(CONFIG["broker_address"], request)
            print("Request sent to broker")  # Debug log
    except queue.Empty:
        pass
    except Exception as e:
        print(f"Error processing request: {str(e)}")  # Debug log

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text', '')
        source_lang = data.get('source_language', 'en')
        target_lang = data.get('target_language', 'es')

        print(f"Received translation request: {text}")  # Debug log

        # Clear previous responses
        translation_responses.clear()

        # Create translation request
        translation_request = TranslationRequest(
            text=text,
            source_language=source_lang,
            preferred_language=target_lang
        )

        # Add request to queue
        request_queue.put(translation_request)
        print("Request added to queue")  # Debug log

        # Wait for translation
        max_attempts = 40  # Increased attempts for longer wait
        for attempt in range(max_attempts):
            print(f"Waiting for translation (attempt {attempt + 1})")  # Debug log
            time.sleep(0.5)
            if translation_responses:
                response = list(translation_responses.values())[0]
                if response != "Message forwarded to translation service":
                    print(f"Found translation: {response}")  # Debug log
                    return jsonify({
                        "success": True,
                        "translation": response
                    })

        print("Translation timeout")  # Debug log
        return jsonify({
            "success": False,
            "error": "Translation timeout"
        })

    except Exception as e:
        print(f"Error in translate endpoint: {str(e)}")  # Debug log
        return jsonify({
            "success": False,
            "error": str(e)
        })

def run_agent():
    """Run the agent in a separate thread"""
    try:
        student_agent.run()
    except Exception as e:
        print(f"Agent error: {str(e)}")

if __name__ == '__main__':
    # Fund the agent if needed
    fund_agent_if_low(student_agent.wallet.address())
    
    # Include the protocol
    student_agent.include(web_protocol)
    
    # Run the agent in a separate thread with error handling
    import threading
    agent_thread = threading.Thread(target=run_agent)
    agent_thread.daemon = True
    agent_thread.start()
    
    # Run Flask app
    app.run(debug=False, port=5000)