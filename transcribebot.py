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

def prepaudio(audiofile):
    oggfile = AudioSegment.from_ogg(audiofile)
    oggfile.export("audio.wav", format="wav")
    convertemessage = sr.AudioFile("audio.wav")
    with convertemessage as sounds:
        transcribeaudo = st.record(sounds)
    return transcribeaudo

@bot.message_command(name="Transcrible Using Sphinx")
async def transcribesphinx(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    try:
        await inter.response.defer(ephemeral='true')
        await message.attachments[0].save("audio.ogg")
        await inter.edit_original_message(content=st.recognize_sphinx(prepaudio("audio.ogg")))
        os.remove("audio.ogg")
        os.remove("audio.wav")
    except Exception as e:
        await inter.edit_original_message(content=f'an error appears to have occoured please report it to the developer: {e}')

@bot.message_command(name="Transcrible Using Google")
async def transcribesphinx(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    try:
        await inter.response.defer(ephemeral='true')
        await message.attachments[0].save("audio.ogg")
        await inter.edit_original_message(content=st.recognize_google(prepaudio("audio.ogg")))
        os.remove("audio.ogg")
        os.remove("audio.wav")
    except Exception as e:
        await inter.edit_original_message(content=f'an error appears to have occoured please report it to the developer: {e}')

@bot.message_command(name="Transcrible Using Bing")
async def transcribesphinx(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    try:
        await inter.response.defer(ephemeral='true')
        await message.attachments[0].save("audio.ogg")
        await inter.edit_original_message(content=st.recognize_bing(prepaudio("audio.ogg")))
        os.remove("audio.ogg")
        os.remove("audio.wav")
    except Exception as e:
        await inter.edit_original_message(content=f'an error appears to have occoured please report it to the developer: {e}')

bot.run(os.getenv("TOKEN"))