from .client import QuoteGuessr;

def register(client: QuoteGuessr) -> None:
    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")

