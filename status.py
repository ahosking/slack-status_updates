"""
This module contains functions to update and clear Slack statuses for
multiple workspaces.

The module uses the Slack SDK to interact with the Slack API and the
python-dotenv package to manage environment variables.

Functions:
- update_status(token, STATUS_TEXT, STATUS_EMOJI, EXPIRATION_IN_SECONDS):
    Update the Slack status for a given token.
- clear_status(token): Clear the Slack status for a given token.

Usage:
1. Set up your Slack workspaces and obtain the necessary tokens.
2. Store the tokens in environment variables or a .env file.
3. Use the functions to update or clear the statuses for your workspaces.
"""

import argparse
import random
import os
import sys
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()


# List of food-based emojis for lunch status
food_emojis = [
    ":pizza:",
    ":hamburger:",
    ":bento:",
    ":sushi:",
    ":taco:",
    ":burrito:",
    ":ramen:",
    ":spaghetti:",
    ":sandwich:",
    ":fries:",
]

# List of your Slack workspace tokens
tokens = [
    os.getenv("SLACK_TOKEN_1"),
    os.getenv("SLACK_TOKEN_2"),
    # Add more tokens as needed by referencing additional .env variables
]

# Function to update status


def update_status(slack_token, status_text, status_emoji,
                  expiration_in_seconds):
    """
    Update the Slack status for a given token.

    Parameters:
    token (str): The Slack API token for the workspace.
    status_text (str): The text to be displayed as the status.
    status_emoji (str): The emoji to be displayed as the status.
    expiration_in_seconds (int): The duration in seconds for which the
    status should be active.

    Returns:
    None: This function does not return a value. It prints a success or
          error message to the console.
    """
    if not slack_token:
        print("No valid Slack token found.")
        return
    client = WebClient(token=slack_token)

    # Calculate the expiration timestamp
    expiration_timestamp = int(time.time()) + expiration_in_seconds

    client = WebClient(token=slack_token)
    try:
        client.users_profile_set(
            profile={
                "status_text": status_text,
                "status_emoji": status_emoji,
                "status_expiration": expiration_timestamp,
            }
        )
        print(
            f"Status updated successfully in workspace with token: {
                slack_token[:12]}"
        )
    except SlackApiError as e:
        print(
            f"Error updating status in workspace with token: {
                slack_token}: {e.response['error']}"
        )


# Function to clear status


def clear_status(slack_token):
    """Clear the Slack status for a given token.

    Args:
        slack_token (str): The Slack API token for the workspace.
    """
    if not slack_token:
        print("No valid Slack token found.")
        return
    client = WebClient(token=slack_token)
    try:
        client.users_profile_set(
            profile={"status_text": "",
                     "status_emoji": "", "status_expiration": 0}
        )
        print(f"Status cleared successfully in workspace with token: {
              slack_token[:12]}")
    except SlackApiError as e:
        print(
            f"Error clearing status in workspace with token: {
                slack_token[:12]}: {e.response['error']}"
        )


# Argument parsing
parser = argparse.ArgumentParser(description="Slack Status Manager")
parser.add_argument(
    "action",
    choices=["brb", "lunch", "custom", "clear"],
    help="Action to set the status",
)
parser.add_argument("--emoji", type=str, help="Custom emoji for the status")
parser.add_argument("--message", type=str,
                    help="Custom message for the status")
parser.add_argument(
    "--time", type=int, help="Duration in minutes for the custom status"
)
args = parser.parse_args()

# Determine the action
if args.action == "brb":
    STATUS_TEXT = "I'll Be Right Back!"
    STATUS_EMOJI = ":brb:"
    EXPIRATION_IN_SECONDS = 15 * 60  # 15 minutes
elif args.action == "lunch":
    STATUS_TEXT = "Lunch Time"
    STATUS_EMOJI = random.choice(food_emojis)
    EXPIRATION_IN_SECONDS = 60 * 60  # 60 minutes
elif args.action == "custom":
    if not args.message or not args.time:
        print("Custom status requires --message and --time arguments.")
        sys.exit(1)
    STATUS_TEXT = args.message
    STATUS_EMOJI = ":speech_balloon:"  # Default emoji
    if args.emoji:
        STATUS_EMOJI = args.emoji  # Use provided emoji
    EXPIRATION_IN_SECONDS = args.time * 60  # Convert minutes to seconds
elif args.action == "clear":
    for token in tokens:
        clear_status(token)
    sys.exit(0)

# Update status in all workspaces
for token in tokens:
    update_status(token, STATUS_TEXT, STATUS_EMOJI, EXPIRATION_IN_SECONDS)
