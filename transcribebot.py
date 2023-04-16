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

@bot.message_command(name="Transcribe Using Sphinx")
async def transcribesphinx(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    try:
        await inter.response.defer(ephemeral='true')
        await message.attachments[0].save("audio.ogg")
        embed=disnake.Embed(title=st.recognize_sphinx(prepaudio("audio.ogg")), color=0x3584e4)
        embed.set_author(name=message.author.nick, url=message.jump_url, icon_url=message.author.display_avatar)
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
        embed=disnake.Embed(title=st.recognize_google(prepaudio("audio.ogg")), color=0x3584e4)
        embed.set_author(name=message.author.display_name, url=message.jump_url, icon_url=message.author.display_avatar)
        await inter.edit_original_message(embed=embed, components=[disnake.ui.Button(label="See more posibilites", style=disnake.ButtonStyle.success, custom_id="gp")])
        os.remove("audio.ogg")
        os.remove("audio.wav")
    except Exception as e:
        await inter.edit_original_message(content=f'an error appears to have occoured please report it to the developer: {e}')

@bot.listen("on_button_click")
async def extratranscribe(inter: disnake.MessageInteraction, message: disnake.Message):
    if inter.component.custom_id == "gp":
        await inter.response.defer(ephemeral='true')
        await message.attachments[0].save("audio.ogg")
        embed=disnake.Embed(title=st.recognize_google(prepaudio("audio.ogg"), show_all=True), color=0x3584e4)
        embed.set_author(name=message.author.nick, url=message.jump_url, icon_url=message.author.display_avatar)
        await inter.edit_original_message(embed=embed)
        os.remove("audio.ogg")
        os.remove("audio.wav")

bot.run(os.getenv("TOKEN"))