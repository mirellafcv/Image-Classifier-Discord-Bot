import discord
# This example requires the 'members' and 'message_content' privileged intents to function.
from discord.ext import commands
import random
import os
import requests
from getclass import get_class

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

model_path = "./keras_model.h5"

def img():
    lista = os.listdir('imagem')
    imgs = random.choice(lista)
    return imgs

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def meme(ctx):
    with open(f'imagem/{img()}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def analisar_foto(ctx):
    if not ctx.message.attachments:
        await ctx.send('Por favor, envie uma imagem anexada ao comando.')
        return

    labels_path = "./labels.txt"
    if not os.path.exists(model_path) or not os.path.exists(labels_path):
        await ctx.send('Modelo ou arquivo de labels não encontrado. Coloque keras_model.h5 e labels.txt na pasta do bot.')
        return

    for anexo in ctx.message.attachments:
        nome_anexo = anexo.filename
        await anexo.save(f"./{nome_anexo}")

        results = get_class(model=model_path, label=labels_path, image=f"./{nome_anexo}", top_k=2)
        if not results:
            await ctx.send('Não foi possível classificar a imagem.')
            continue

        lines = [f'{label}: {score * 100:.1f}% de certeza' for label, score in results]
        await ctx.send('Resultado da classificação:\n' + '\n'.join(lines))

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

def get_fox_image_url():    
    url = 'https://meme-api.com/gimme/AnimalsBeingDerps'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Uma vez que chamamos o comando duck, o programa chama a função get_duck_image_url '''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command('cat')
async def fox(ctx):
    image_url = get_fox_image_url()
    await ctx.send(image_url)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

bot.run("TOKEN")
