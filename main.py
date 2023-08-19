import os;
import lib.bot as bot;
from dotenv import load_dotenv

def main():
    # load environment variables from .env
    load_dotenv();

    try:
        bot.start(
            api_token=get_env_var("DISCORD_API_TOKEN"),
            guild_id=get_env_var("DISCORD_GUILD_ID"),
            guessing_time=get_env_var("GUESSING_TIME"),
            path_to_db="./quotes.db");
    except Exception as error:
        print("Runtime error:\n{}".format(error))
        raise

def get_env_var(env_name: str) -> str:
    env_value = os.getenv(env_name)
    if env_value is None:
        raise ValueError("'{}' is not defined!".format(env_name))
    return env_value

if __name__ == "__main__":
    main()
