from typing import Dict, Tuple, List, Optional
from .database import Database

class Quote():
    def __init__(self, quote: str, speaker: int, recipient: Optional[int]) -> None:
        self.quote = quote
        self.speaker = speaker
        self.recipient = recipient

    def compare(self, guess: Tuple[int, Optional[int]]) -> bool:
        return self.speaker == guess[0] and self.recipient == guess[1]

    def asMessage(self) -> str:
        return f"*'{self.quote}'*";

class Game():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.ongoing: bool
        self.guesses: Dict[int, Tuple[int, Optional[int]]]
        self.quote: Quote

    def init(self) -> None:
        self.ongoing = False
        self.guesses = {}
        self.quote = Quote("if u see this, dis broke", -1, -1)

    def start(self) -> None:
        self.guesses.clear()
        self.ongoing = True
        speaker, recipient, quote = Database().randomQuote();
        self.quote = Quote(quote, speaker, recipient)
        print("New round started!")

    def finishAndGetResults(self) -> Tuple[int, Optional[int], List[int]]:
        self.ongoing = False
        correct_users: List[int] = []
        for guesser, guess in self.guesses.items():
            if self.quote.compare(guess):
                correct_users.append(guesser)
        print("Finished round!")
        return (self.quote.speaker, self.quote.recipient, correct_users)

    def lockGuess(self, user_id: int, speaker: int, recipient: Optional[int]) -> None:
        self.guesses[user_id] = (speaker, recipient)
