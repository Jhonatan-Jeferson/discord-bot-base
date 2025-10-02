import os
import multiprocessing

def make_folder_structure() -> None:
    paths = [
        os.path.join("src", "commands"),
        os.path.join("src", "utils"),
        os.path.join("src", "database")
    ]
    for path in paths: os.makedirs(path, exist_ok=True)
    
def create_main_file() -> None:
    file = open(os.path.join("src", "main.py"), "w")
    file.write(
        "from discord_bot_base import Bot\n"+\
        "from discord import Intents\n"+\
        "from os import getenv\n\n"+\
        "bot: Bot = Bot(command_prefix=getenv(\"BOT_PREFIX\"), intents=Intents.all())\n"+\
        "bot.run(getenv(\"BOT_TOKEN\"))"
    )
    file.close()
    
def create_bot():
    make_folder_structure()
    create_main_file()
    
def create_env_file() -> None: 
    file = open(".env", "w")
    file.write(
        "COMMANDS_DIR=commands\n"+\
        "BOT_TOKEN=bot_token_here\n"+\
        "BOT_PREFIX=!"
    )
    file.close()
    
def main() -> None:
    process = multiprocessing.Process(target=create_bot)
    process.start()
    create_env_file()
    process.join()