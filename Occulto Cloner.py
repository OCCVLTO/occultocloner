# Refined & Transalted by Occulto, the whole idea and some parts of the code are not mine.

import discord
from pystyle import *
import os

Write.Print("Benvenuto nell'Occvlto Cloner", Colors.green_to_red, interval=0)
client = discord.Client()
token = Write.Input('\nInserisci il tuo token: \n', Colors.blue_to_purple, interval=0)
os.system("cls")

class ServerCloner:
    def __init__(self, client: discord.Client, i_guild: discord.Guild, o_guild: discord.Guild):
        self.created_map = {}
        self.client = client
        self.input_guild = i_guild
        self.output_guild = o_guild
    
    async def clear_server(self):
        Write.Print('Inizio pulizia del Server.\n', Colors.blue_to_purple, interval=0)
        Write.Print('Stato Attuale: Rimuovendo ruoli\n', Colors.blue_to_purple, interval=0)
        for role in self.output_guild.roles:
            try:
                await role.delete()
                Write.Print(f'Ruoli Rimossi: {str(role.id)}.\n', Colors.blue_to_purple, interval=0)
            except:
                Write.Print(f'Impossibile cancellare il ruolo {str(role.id)}.\n', Colors.blue_to_purple, interval=0)
                continue

        Write.Print("I ruoli sono stati puliti\n", Colors.red, interval=0)

        for channel in self.output_guild.channels:
            try:
                await channel.delete()
                Write.Print(f'Rimosso il canale {str(channel.id)}.\n', Colors.purple_to_blue, interval=0)
            except:
                Write.Print(f'Impossibile rimuovere il canale {str(channel.id)}.\n', Colors.purple_to_blue, interval=0)

        Write.Print("Pulizia Terminata\n", Colors.red, interval=0)
        
    async def create_roles(self):
        server_roles = []
        for role in self.input_guild.roles:
            server_roles.insert(0, role)

        for role in server_roles:
            new_role = await self.output_guild.create_role(name=role.name, permissions=role.permissions, colour=role.colour, hoist=role.hoist, mentionable=role.mentionable)
            Write.Print(f'Creato il Ruolo : {str(new_role.id)}\n', Colors.green_to_red, interval=0)
    
    async def create_categories(self):
        
        for category in self.input_guild.categories:
            overwrites_to = {}
            for key, value in category.overwrites.items():
                role = discord.utils.get(self.input_guild.roles, name=key.name)
                overwrites_to[role] = value
            new_category = await self.output_guild.create_category_channel(
                name=category.name, overwrites=overwrites_to
            )
            await new_category.edit(
                position=int(category.position), nsfw=category.is_nsfw()
            )
            Write.Print(f'Creata la Categoria : {str(new_category.id)}\n', Colors.green_to_blue, interval=0)
            self.created_map[str(category.id)] = new_category.id
    
    async def create_text_channels(self):
        for channel in self.input_guild.text_channels:
            overwrites_to = {}
            for key, value in channel.overwrites.items():
                    role = discord.utils.get(self.input_guild.roles, name=key.name)
                    overwrites_to[role] = value
            if channel.category_id is not None:
                new_category_id = self.created_map.get(str(channel.category_id))

                new_category = await self.client.fetch_channel(int(new_category_id))
                new_channel = await new_category.create_text_channel(
                    name=channel.name, topic=channel.topic, position=channel.position, slowmode_delay=channel.slowmode_delay, 
                    nsfw=channel.is_nsfw(), overwrites=overwrites_to
                )
                Write.Print(f'Creato il canale {str(new_channel.id)}.\n', Colors.green_to_cyan, interval=0)
            else:
                new_channel = await self.output_guild.create_text_channel(name=channel.name, topic=channel.topic, position=channel.position,
                                                slowmode_delay=channel.slowmode_delay, nsfw=channel.is_nsfw(),
                                                overwrites=overwrites_to)
                Write.Print(f'Creato il canale {str(new_channel.id)}.\n', Colors.green_to_cyan, interval=0)

    async def create_voice_channels(self):
        for channel in self.input_guild.voice_channels:
            overwrites_to = {}
            for key, value in channel.overwrites.items():
                    role = discord.utils.get(self.input_guild.roles, name=key.name)
                    overwrites_to[role] = value
            if channel.category_id is not None:
                new_category_id = self.created_map.get(str(channel.category_id))
                new_category = await self.client.fetch_channel(int(new_category_id))
                new_channel = await new_category.create_voice_channel(name=channel.name, position=channel.position,
                                                    user_limit=channel.user_limit, overwrites=overwrites_to)
                Write.Print(f'Creato Il Canale {str(new_channel.id)}.\n', Colors.green_to_white, interval=0)
            else:
                new_channel = await self.output_guild.create_voice_channel(name=channel.name, position=channel.position,
                                                 user_limit=channel.user_limit, overwrites=overwrites_to)
                Write.Print(f'Creato Il Canale {str(new_channel.id)}.\n', Colors.green_to_cyan, interval=0)

    async def start(self):
        not_finished = True
        while not_finished:
            await self.clear_server()    
            await self.create_roles()
            await self.create_categories()
            await self.create_text_channels()
            await self.create_voice_channels()
            not_finished = False

Write.Print("Operazione in Corso...\n", Colors.green_to_red, interval=0)

async def cloning():
    i_guild = client.get_guild(int(Write.Input("Inserisci l'ID del server che VUOI Copiare: \n", Colors.green_to_red, interval=0)))
    o_guild = client.get_guild(int(Write.Input("Inserisci l'ID del server DOVE vuoi Copiare: \n", Colors.green_to_red, interval=0)))

    cloner = ServerCloner(client, i_guild, o_guild)
    await cloner.start()
    Write.Print('Pulizia Effettuata\n', Colors.green_to_red, interval=0)
    Write.Input('Premi invio per chiudere il programma', Colors.green_to_red, interval=0)

@client.event
async def on_ready():
    await cloning()

client.run(token, bot=False)

