import requests
import json

# Simulated REST API endpoint
API_URL = "https://api.rester.example/notify"

# Predefined function to send notification
def sendNotification(recipient, message, channel="email"):
    payload = {"recipient": recipient, "message": message, "channel": channel}
    response = requests.post(API_URL, json=payload)
    return response.json()

functions = {"sendNotification": sendNotification}

# Step 1: Conversation input
conversation = """
Human: Notify the team about the urgent meeting tomorrow.
Bot: Which team?
Human: DevOps, at 10 AM.
"""

# Step 2: Copilot-generated parsing logic (simulated; in IDE, Copilot autocompletes)
def parse_conversation(convo):
    # Copilot-generated: Parse conversation and deduce template
    if "notify" in convo.lower() and "DevOps" in convo:
        template = "Urgent: Meeting at {time} tomorrow"
        return {
            "functionName": "sendNotification",
            "parameters": {
                "recipient": "DevOps",
                "message": template.format(time="10 AM"),
                "channel": "email"  # Default channel
            }
        }
    return None  # Handle other cases or prompt for clarification

# Step 3: Extract and validate
extracted = parse_conversation(conversation)
if not extracted or extracted["functionName"] not in functions:
    raise ValueError("Invalid function or parsing failed")

# Step 4: Invoke the function
result = functions[extracted["functionName"]](**extracted["parameters"])
print(result)  # Output: API response (e.g., {"status": "Notification sent"})