import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
from os import path
import asyncio
from pydub import AudioSegment
import deepspeech
import numpy as np
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

@bot.message_command(name="Transcribe Using Sphinx")
async def transcribesphinx(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    try:
        await inter.response.defer(ephemeral='true')
        await message.attachments[0].save("audio.ogg")
        embed=disnake.Embed(title="Audio Transcription",description=st.recognize_sphinx(prepaudio("audio.ogg")), color=0x3584e4)
        embed.set_author(name=message.author.display_name, url=message.jump_url, icon_url=message.author.display_avatar)
        embed.set_footer(text="Accuracy not guaranteed")
        await inter.edit_original_message(embed=embed)
        os.remove("audio.ogg")
        os.remove("audio.wav")
    except Exception as e:
        await inter.edit_original_message(content=f'an error appears to have occoured please report it to the developer: {e}')

@bot.message_command(name="Transcribe Using Google")
async def transcribesphinx(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    try:
        await inter.response.defer(ephemeral='true')
        await message.attachments[0].save("audio.ogg")
        # WARNING Google is propritary, consider disabling however sphynix is currently not very good so this provides an option
        embed=disnake.Embed(title="Audio Transcription",description=st.recognize_google(prepaudio("audio.ogg")), color=0x3584e4)
        embed.set_author(name=message.author.display_name, url=message.jump_url, icon_url=message.author.display_avatar)
        embed.set_footer(text="Accuracy not guaranteed")
        await inter.edit_original_message(embed=embed)
        await asyncio.sleep(3)
        os.remove("audio.ogg")
        os.remove("audio.wav")
    except Exception as e:
        await inter.edit_original_message(content=f'an error appears to have occoured please report it to the developer: {e}')

@bot.message_command(name="Transcribe Using DeepSpeech")
async def transcribesphinx(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    try:
        await inter.response.defer(ephemeral='true')
        await message.attachments[0].save("audio.ogg")
        audio = AudioSegment.from_file("audio.ogg", format="ogg")
        audio.export("audio.wav", format="wav")

        model = deepspeech.Model('deepspeech-0.9.3-models.pbmm')
        model.enableExternalScorer('deepspeech-0.9.3-models.scorer')
        model.setBeamWidth(500)
        model.setScorerAlphaBeta(0.75, 1.85)
        
        with open("audio.wav", 'rb') as f:
            audio = np.frombuffer(f.read(), np.int16)
        embed=disnake.Embed(title="Audio Transcription",description=model.stt(audio), color=0x3584e4)
        embed.set_author(name=message.author.display_name, url=message.jump_url, icon_url=message.author.display_avatar)
        embed.set_footer(text="Accuracy not guaranteed")
        await inter.edit_original_message(embed=embed)
        await asyncio.sleep(3)
        os.remove("audio.ogg")
        os.remove("audio.wav")
    except Exception as e:
        await inter.edit_original_message(content=f'an error appears to have occoured please report it to the developer: {e}')

bot.run(os.getenv("TOKEN"))