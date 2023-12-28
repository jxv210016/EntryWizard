import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix='!')

@bot.command()
async def change_unit(ctx, unit_size):
    # Make an API call to Flask backend to change unit size
    response = requests.post('http://localhost:5000/unit', json={'unit_size': unit_size})
    if response.status_code == 200:
        await ctx.send('Unit size updated successfully.')
    else:
        await ctx.send('Failed to update unit size.')

@bot.command()
async def toggle_task(ctx):
    # Make an API call to Flask backend to toggle task status
    response = requests.post('http://localhost:5000/toggle_task')
    if response.status_code == 200:
        new_status = response.json().get('new_status')
        await ctx.send(f'Task {"started" if new_status else "stopped"} successfully.')
    else:
        await ctx.send('Failed to toggle task.')

bot.run('your_discord_bot_token')
