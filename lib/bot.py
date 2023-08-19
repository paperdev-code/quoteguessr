from .client import QuoteGuessr
from .database import Database
from .game import Game
from .commands import register as register_commands
from .events import register as register_events

def start(api_token: str, guild_id: str, path_to_db: str, guessing_time: str) -> None:
    try:
        Database().init(path_to_db)
        Game().init()

        print(f"Guessing time: {guessing_time} seconds.")
        client = QuoteGuessr(guild_id=guild_id, guessing_time=int(guessing_time))
        register_events(client)
        register_commands(client)
        client.run(api_token)

    except Exception as error:
        print(f"QuoteGuessr crashed and burned; {error}")
        raise
