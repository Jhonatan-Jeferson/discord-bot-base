from discord import Embed
from discord.ext.commands import Cog, Command, HelpCommand, Context, Bot, AutoShardedBot

from typing import Optional, TypeVar, cast

BotT = TypeVar("BotT", bound="Bot | AutoShardedBot")


class CustomHelpCommand(HelpCommand):
    async def command_callback(self, ctx: Context[BotT], /, *, command: Optional[str] = None) -> None:
        """
        This is the help command that gets called when the user invokes the help command.
        """
        if command and (cmd:=ctx.bot.get_command(command)):
            await ctx.reply(embed=Embed(title=f"Ajuda para o comando `{command}`", description=cmd.help))
            return
        cmds = self.get_bot_mapping()
        del cmds[None]
        cmds = cast(dict[Cog, list[Command]], cmds)
        msg: str = str()
        for cog, commands in cmds.items():
            msg += f"**{cog.qualified_name}**:\n\t\"{cog.description}\"\n"
            cmd_listed = [f"\t{cmd.name} ⇒ {cmd.help}" for cmd in commands]
            msg += "{}\n\n".format("\n".join(cmd_listed))
        await ctx.reply(embed=Embed(title="Comandos do Bot", description=msg))
            
            