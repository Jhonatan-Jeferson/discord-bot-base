from discord import ClientUser, Intents
from discord.ext.commands import (Bot as DiscordBot)
from .logger import LOGGER
from .helpcmd import CustomHelpCommand

import os
import asyncio
from typing import cast

class Bot(DiscordBot):
    
    def __init__(self, command_prefix: str, intents: Intents) -> None:
        super().__init__(command_prefix, intents=intents, help_command=CustomHelpCommand())
       
    async def setup_hook(self) -> None:
        LOGGER.info("Starting to load commands.")
        commands_dir = os.getenv("COMMANDS_DIR", "commands")
        commands_dir_os: str = os.path.join("src", commands_dir)
        modules: list[str] = os.listdir(commands_dir_os)
        if "__pycache__" in modules: modules.remove("__pycache__")
        separator: str = os.path.sep
        load: list[asyncio.Task[None]] = []
        for module in modules:
            module_path: str = os.path.join(commands_dir, module)\
                .replace(separator, ".")
            task = asyncio.create_task(self.load_extension(module_path))
            load.append(task)
        await asyncio.gather(*load)
        await self.tree.sync()
        LOGGER.info("All commands loaded.")
    
    async def on_ready(self) -> None:
        user: ClientUser = cast(ClientUser, self.user)
        LOGGER.info(f"Logged in as \"{user.name}\" (ID: {user.id})")