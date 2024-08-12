import argparse
import random
import os
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()


# List of food-based emojis for lunch status
food_emojis = [":pizza:", ":hamburger:", ":bento:", ":sushi:", ":taco:",
               ":burrito:", ":ramen:", ":spaghetti:", ":sandwich:", ":fries:"]

# List of your Slack workspace tokens
tokens = [
    os.getenv("SLACK_TOKEN_1"),
    os.getenv("SLACK_TOKEN_2"),
    # Add more tokens as needed by referencing additional .env variables
]

# Function to update status


def update_status(token, status_text, status_emoji, expiration_in_seconds):
    if not token:
        print("No valid Slack token found.")
        return
    client = WebClient(token=token)

    # Calculate the expiration timestamp
    expiration_timestamp = int(time.time()) + expiration_in_seconds

    client = WebClient(token=token)
    try:
        response = client.users_profile_set(
            profile={
                "status_text": status_text,
                "status_emoji": status_emoji,
                "status_expiration": expiration_timestamp
            }
        )
        print(f"Status updated successfully in workspace with token: {
              token[:12]}")
    except SlackApiError as e:
        print(f"Error updating status in workspace with token: {
              token}: {e.response['error']}")

# Function to clear status


def clear_status(token):
    if not token:
        print("No valid Slack token found.")
        return
    client = WebClient(token=token)
    try:
        response = client.users_profile_set(
            profile={
                "status_text": "",
                "status_emoji": "",
                "status_expiration": 0
            }
        )
        print(f"Status cleared successfully in workspace with token: {token}")
    except SlackApiError as e:
        print(f"Error clearing status in workspace with token: {
              token}: {e.response['error']}")


# Argument parsing
parser = argparse.ArgumentParser(description="Slack Status Manager")
parser.add_argument("action", choices=[
                    "brb", "lunch", "custom", "clear"], help="Action to set the status")
parser.add_argument("--emoji", type=str,
                    help="Custom emoji for the status")
parser.add_argument("--message", type=str,
                    help="Custom message for the status")
parser.add_argument("--time", type=int,
                    help="Duration in minutes for the custom status")
args = parser.parse_args()

# Determine the action
if args.action == "brb":
    status_text = "I'll Be Right Back!"
    status_emoji = ":brb:"
    expiration_in_seconds = 15 * 60  # 15 minutes
elif args.action == "lunch":
    status_text = "Lunch Time"
    status_emoji = random.choice(food_emojis)
    expiration_in_seconds = 60 * 60  # 60 minutes
elif args.action == "custom":
    if not args.message or not args.time:
        print("Custom status requires --message and --time arguments.")
        exit(1)
    status_text = args.message
    status_emoji = ":speech_balloon:"  # Default emoji
    if args.emoji:
        status_emoji = args.emoji  # Use provided emoji
    expiration_in_seconds = args.time * 60  # Convert minutes to seconds
elif args.action == "clear":
    for token in tokens:
        clear_status(token)
    exit(0)

# Update status in all workspaces
for token in tokens:
    update_status(token, status_text, status_emoji, expiration_in_seconds)
