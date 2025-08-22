import asyncio
import random
from datetime import datetime

import discord


class Bumper:
    def __init__(self, token: str, channel_id: int, delay: float, bump_cooldown: float, max_random_delay: float) -> None:
        self._token = token
        self._channel_id = channel_id

        self._delay = delay
        self._bump_cooldown = bump_cooldown
        self._max_random_delay = max_random_delay

        self._client = discord.Client()
        self._client.event(self.on_ready)

    async def run(self) -> None:
        await self._client.start(self._token)

    async def on_ready(self) -> None:
        await asyncio.sleep(self._delay)
        await self._start_bumping()

    async def _start_bumping(self) -> None:
        while True:
            await self._bump(self._channel_id)
            await asyncio.sleep(self._bump_cooldown + random.uniform(1, self._max_random_delay))

    async def _bump(self, channel_id: int) -> None:
        commands = []
        channel = self._client.get_channel(channel_id)
        if not channel:
            print(f"The bump channel of {channel.guild.name} is not found.")
            return

        application_commands = await channel.application_commands()
        commands = [cmd for cmd in application_commands if cmd.name == "bump"]

        if not commands:
            print(f"The bump channel of {channel.guild.name} has no bump command.")
            return

        for command in commands:
            await command.__call__(channel)
            await asyncio.sleep(2)

        current_time = datetime.today().strftime("%d/%m/%y %H:%M:%S")
        print(f"{current_time} - The server got bumped: {channel.guild.name}")
