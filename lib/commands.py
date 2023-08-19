from typing import Optional
import discord
from discord import app_commands
import asyncio
from .client import QuoteGuessr
from .game import Game
from .database import Database

def register(client: QuoteGuessr):
    @client.tree.command()
    async def ping(interaction: discord.Interaction):
        """Am I alive?"""
        user = interaction.user
        await interaction.response.send_message(f"Oh {user.mention}! What a grand and intoxicating innocence!")

    @client.tree.command()
    async def play(interaction: discord.Interaction):
        """Start a round of QuoteGuessr"""
        if Game().ongoing:
            await interaction.response.send_message("A round is currently ongoing!", ephemeral=True)
            return
        await interaction.response.send_message("Starting round!")
        channel_id: int = interaction.channel_id if interaction.channel_id is not None else 0;
        asyncio.create_task(client.game(channel_id));

    @client.tree.command()
    @app_commands.describe(quote="The thing they said", speaker="The thing that spoke", recipient="The thing that was spoken to")
    async def quote(interaction: discord.Interaction, quote: str, speaker: discord.Member, recipient: Optional[discord.Member]):
        """Save a quote"""
        speaker_id = speaker.id
        recipient_id = recipient.id if recipient is not None else None
        Database().saveQuote(speaker_id, recipient_id, quote)
        await interaction.response.send_message("Saved quote.", ephemeral=True)

    @client.tree.command()
    @app_commands.describe(speaker="The person that spoke", recipient="An optional reciever of said quote")
    async def guess(interaction: discord.Interaction, speaker: discord.Member, recipient: Optional[discord.Member]):
        """Make a guess"""
        if not Game().ongoing:
            await interaction.response.send_message("No game currently ongoing!", ephemeral=True)
            return
        speaker_id = speaker.id
        recipient_id = recipient.id if recipient is not None else None
        Game().lockGuess(interaction.user.id, speaker_id, recipient_id)
        await interaction.response.send_message("Locked in guess.", ephemeral=True)

    @client.tree.command()
    async def quotecount(interaction: discord.Interaction):
        """The amount of quotes stored in the underlying database"""
        await interaction.response.send_message(f"There are currently {Database().countQuotes()} quotes stored", ephemeral=True)
