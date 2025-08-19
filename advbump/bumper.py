from datetime import datetime
import discord
import asyncio
import random

class Bumper:
    def __init__(self, token: str, channel_id: int, delay: int,  bump_cooldown: int, max_random_delay: int):
        self.token = token
        self.channel_id = channel_id
        
        self.delay = delay
        self.bump_cooldown = bump_cooldown
        self.max_random_delay = max_random_delay

        self.client = discord.Client()
        self.client.event(self.on_ready)
    
    async def run(self):
        await self.client.start(self.token)

    async def bump(self, channel_id: int):
        commands = []
        channel = self.client.get_channel(channel_id)
        if not channel:
            print(f'The bump channel of {channel.guild.name} is not found.')
            return
        
        application_commands = await channel.application_commands()
        for cmd in application_commands:
            if cmd.name == 'bump':
                commands.append(cmd)

        if not commands:
            print(f'The bump channel of {channel.guild.name} has no bump command.')
            return
        
        for command in commands:
            await command.__call__(channel)
            await asyncio.sleep(2)

        current_time = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        print(f'{current_time} - The server got bumped: {channel.guild.name}')

    async def start_bumping(self):
        while True:
            await self.bump(self.channel_id)
            await asyncio.sleep(self.bump_cooldown + random.uniform(1, self.max_random_delay))

    async def on_ready(self):
        await asyncio.sleep(self.delay)
        await self.start_bumping()