import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
bot = commands.Bot(command_prefix='.')

@bot.message_command(name="Transcrible")
async def transcribe(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    # Reversing the message and sending it back.
    await message.attachments[0].save("audio.mp3")
    await inter.response.send_message("audio saved", file=disnake.File("audio.mp3"))

bot.run(os.getenv("TOKEN"))