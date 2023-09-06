from typing import Optional, List

import openai

from .session import Session
from .key import KeyGroup


def send_msg(messages) -> str:
    response = openai.Completion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
    )
    return response


class ChatManager:
    """High-level interface for interaction with ChatGPT

    Attributes:
        cur_session: The current session
        sessions: A list of all sessions
        keys: A KeyGroup object managing key-related stuff

    """

    def __init__(self) -> None:
        self.cur_session: Optional[Session] = None
        self.sessions: List[Session] = []
        self.keys: KeyGroup = KeyGroup()
