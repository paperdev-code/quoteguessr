import asyncio
import discord
from .game import Game
from discord.ext import tasks

class QuoteGuessr(discord.Client):
    def __init__(self, *, guild_id, guessing_time):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.guild_id = discord.Object(id=guild_id)
        self.tree = discord.app_commands.CommandTree(self)
        self.guessing_time = guessing_time

    async def setup_hook(self):
        self.tree.copy_global_to(guild=self.guild_id)
        await self.tree.sync(guild=self.guild_id)

    async def getUserFromId(self, user_id: int):
        user = self.get_user(user_id)
        if user is None:
            user = await self.fetch_user(user_id)
        return user


    #INFO: Something about a type problem (PrivateChannel) here, but ill never encounter it.
    async def game(self, channel_id: int):
        if channel_id == 0:
            raise ValueError("Something else went horribly wrong.")
        Game().start()
        quote = Game().quote;
        
        channel = self.get_channel(channel_id)
        if (channel is None):
            raise ValueError("Something went horribly wrong.")
        await channel.send(
            f"""Who said the following quote;
            {quote.asMessage()}
            {"...whilst speaking with who?" if quote.recipient is not None else ""}
            """)
       
        print("Collecting guesses!")
        await asyncio.sleep(self.guessing_time)
        
        speaker, recipient, correct_guessers = Game().finishAndGetResults()
        speaker_user = await self.getUserFromId(speaker)
        recipient_user = await self.getUserFromId(recipient) if recipient is not None else None

        await channel.send(
            f"""It was said by {speaker_user.mention} {f"to {recipient_user.mention}!" if recipient_user is not None else "!"}"""
        )

        if len(correct_guessers) > 0:
            users = "";
            for correct_guesser in correct_guessers:
                guesser = await self.getUserFromId(correct_guesser);
                users += f"{guesser.mention}\n"
            await channel.send(f"The following people guessed correctly!\n{users}")
        else:
            await channel.send("...Oof, nobody remembered that!")
