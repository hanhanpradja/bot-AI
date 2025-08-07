import discord
from discord.ext import commands
import os, random
import requests
from model import get_class

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''The duck command returns the photo of the duck'''
    print('hello')
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def classify(ctx):
    if ctx.message.attachments:
        for file in ctx.message.attachments:
            file_name = file.filename
            file_url = file.url
            await file.save(f'./{file_name}')
            await ctx.send(f'file berhasil disimpan dengan nama {file_name}')
            await ctx.send(f'dapat juga diakses melalui cloud discord di {file_url}')

            kelas, skor = get_class('keras_model.h5', 'labels.txt', f'./{file.filename}')

            # INFERENSI
            if kelas == 'Motherboard' and skor >= 0.75:
                await ctx.send('dia adalah motherboard')
                # tambahkan inferensi
            elif kelas == 'CPU (Central Prosessing Unit)' and skor >= 0.75:
                await ctx.send('dia adalah CPU')
                # tambahkan inferensi
            else:
                await ctx.send('aku tidak tahu itu apa')
    else:
        await ctx.send('kamu tidak melampirkan apa apa!')


bot.run('TOKEN')