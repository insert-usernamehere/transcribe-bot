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
    try:
        await inter.response.defer(ephemeral='true')
        await message.attachments[0].save("audio.ogg")
        mp3file = AudioSegment.from_ogg("audio.ogg")
        mp3file.export("audio.wav", format="wav")
        convertemessage = sr.AudioFile("audio.wav")
        with convertemessage as sounds:
            transcribeaudo = st.record(sounds)
        await inter.edit_original_message(content=st.recognize_sphinx(transcribeaudo))
        os.remove("audio.ogg")
        os.remove("audio.wav")
    except Exception as e:
        await inter.edit_original_message(content=f'an error appears to have occoured please report it to the developer: {e}')


bot.run(os.getenv("TOKEN"))