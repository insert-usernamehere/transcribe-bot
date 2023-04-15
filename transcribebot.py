import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
from os import path
from pydub import AudioSegment
import speech_recognition as sr

st = sr.Recognizer()
load_dotenv()
bot = commands.Bot(command_prefix='.')

@bot.message_command(name="Transcrible")
async def transcribe(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    # Reversing the message and sending it back.
    await message.attachments[0].save("audio.ogg")
    mp3file = AudioSegment.from_ogg("audio.ogg")
    mp3file.export("audio.wav", format="wav")
    convertemessage = sr.AudioFile("audio.wav")
    with convertemessage as sounds:
        transcribeaudo = st.record(sounds)
    await inter.response.send_message(st.recognize_sphinx(transcribeaudo), file=disnake.File("audio.mp3"))
    os.remove("audio.ogg")
    os.remove("audio.wav")

bot.run(os.getenv("TOKEN"))