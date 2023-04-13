import os
import openai
import discord
from discord.ext import commands

# Configure your Discord bot token and OpenAI API key
DISCORD_BOT_TOKEN = "your_discord_bot_token"
OPENAI_API_KEY = "your_openai_api_key"

openai.api_key = OPENAI_API_KEY
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# Keep track of conversation history
conversation_history = {}

# GPT-3.5 API call function
async def get_gpt3_5_response(prompt, chat_id, user_id):
    if chat_id not in conversation_history:
        conversation_history[chat_id] = {}

    if user_id not in conversation_history[chat_id]:
        conversation_history[chat_id][user_id] = []

    conversation_history[chat_id][user_id].append(prompt)
    conversation_text = "\n".join(conversation_history[chat_id][user_id])

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=conversation_text,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.9,
    )

    conversation_history[chat_id][user_id].append(response.choices[0].text.strip())
    return response.choices[0].text.strip()

# Command to interact with GPT-3.5
@bot.command(name="ai4d")
async def ai4d(ctx, *, message):
    prompt = f"User: {message}\nAI:"
    response = await get_gpt3_5_response(prompt, ctx.channel.id, ctx.author.id)
    await ctx.send(response)

# Error handling
@ai4d.error
async def ai4d_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a sentence after the command '/ai4d'.")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
