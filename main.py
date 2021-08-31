# Standard
import random

# Community
from asyncio.tasks import wait
import discord
from discord.channel import TextChannel
from discord.ext import commands
from discord.guild import Guild
from discord_slash import SlashCommand, SlashContext
from discord_slash.context import MenuContext
from discord_slash.utils.manage_components import (
    create_select,
    create_select_option,
    create_actionrow,
    create_button,
    wait_for_component,
)
from discord_slash.model import ButtonStyle
from discord_slash.model import ContextMenuType

# Custom
import settings


def get_random_text_channel(guild: Guild):
    """
    Returns a random text channel from the given server that
    the bot has send messages permissions in.
    """
    bot_member = guild.get_member(bot.user.id)
    return random.choice(
        [
            channel
            for channel in guild.text_channels
            if channel.permissions_for(bot_member).send_messages
        ]
    )


bot = commands.Bot(
    command_prefix="=", intents=discord.Intents.default(), help_command=None
)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print("Logged in as:")
    print(bot.user.name + "#" + bot.user.discriminator)
    print(bot.user.id)
    print("------\n")

    print("Guilds:")
    print(bot.guilds)
    print("------\n")


@bot.event
async def on_message(message):
    if message.content in settings.REPLY_DICT:
        await message.reply(settings.REPLY_DICT[message.content])


@slash.context_menu(
    target=ContextMenuType.USER,
    name="Annoy",
    guild_ids=settings.COMMAND_GUILD_IDS,
)
async def _annoy(ctx: MenuContext):
    if ctx.target_author.id == bot.user.id:
        await ctx.send(
            "I'm sorry Dave, I'm afraid I can't do that",
            hidden=True,
        )
        return

    # Get a random channel the selected user can see
    selected_channel = get_random_text_channel(ctx.guild)

    # Annoy the selected user
    await selected_channel.send(
        f"{ctx.target_author.mention} LOL, someone wanted to annoy you :grin:"
    )
    await ctx.send(
        f"The deed has been done! Check {selected_channel.mention}", hidden=True
    )


@slash.context_menu(
    target=ContextMenuType.USER,
    name="Send a fun link",
    guild_ids=settings.COMMAND_GUILD_IDS,
)
async def _send_fun_link(ctx: MenuContext):
    if ctx.target_author.id == bot.user.id:
        await ctx.send(
            "I'm sorry Dave, I'm afraid I can't do that",
            hidden=True,
        )
        return

    text, link = random.choice(list(settings.RANDOM_LINKS.items()))
    await ctx.target_author.send(f"I was told to send you this link: <{link}>")
    await ctx.send(f"{text}", hidden=True)


@slash.slash(name="hello", guild_ids=settings.COMMAND_GUILD_IDS)
async def _hello(ctx: SlashContext):

    action_row = create_actionrow(
        create_button(style=ButtonStyle.blue, label="No You!")
    )
    await ctx.send("Hello!", components=[action_row])

    while True:
        button_ctx = await wait_for_component(bot, components=action_row)
        if button_ctx.author == ctx.author:
            await button_ctx.edit_origin(content="Goodbye!", components=None)
            break
        else:
            await button_ctx.reply("This button isn't for you!", hidden=True)


@slash.slash(name="clear", guild_ids=settings.COMMAND_GUILD_IDS)
async def _clear(ctx: SlashContext):
    await ctx.send("Clearing channel!")
    await ctx.channel.send("⠀\n" * 999)


bot.run(settings.DISCORD_TOKEN)
