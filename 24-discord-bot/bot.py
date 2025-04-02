import discord # Import the discord.py library for interacting with Discord's API
import os # Import the os module to access environment variables
from dotenv import load_dotenv # Import load_dotenv to load environment variables from a .env file


# Load environment variables from a .env file (ensures security by keeping the token hidden)
load_dotenv()

# Retrieve the bot token from the environment variables
# This token is used to authenticate the bot with Discord's API
TOKEN = os.getenv("TOKEN")

# Check if the token was loaded properly; if not, raise an error
if not TOKEN:
    raise ValueError("❌ TOKEN is not set! Check your .env file or environment variables.")

# Set up bot intents (permissions to interact with messages, etc.)
intents = discord.Intents.default()
# Enable message content intent (required to read user messages)
intents.message_content = True  

# Create a Discord client instance with the specified intents
client = discord.Client(intents=intents)

# Event handler that triggers when the bot successfully logs in
@client.event
async def on_ready():
    # Print bot's username when logged in
    # This is useful for debugging and confirming the bot is running 
    print(f"✅ Logged in as {client.user}")

# Event handler that triggers when a message is sent in a server the bot is in
@client.event
async def on_message(message):
    print(f"📨 Received message: {message.content}")  # Debugging
    if message.author == client.user: # Ignore messages sent by the bot itself to prevent loops
        return

    # If the message starts with "$hello", respond with "Hello!"
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Try to run the bot and handle errors gracefully
try:
    print(" Running bot...") # Indicate that the bot is starting
    client.run(TOKEN) # Start the bot with the provided token
except discord.errors.LoginFailure:
    print("❌ Incorrect or invalid token! Check your token again.") # Error if token is incorrect
