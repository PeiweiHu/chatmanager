from typing import Optional, List, Dict, Tuple

import openai

from .session import Session, ChatMessage, ChatResponse
from .key import KeyGroup


class ChatSetup:
    """ Setup openai interface

    """

    model: str = "gpt-3.5-turbo"
    api_base: str = "https://api.openai.com/v1"


"""
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-3.5-turbo-0613",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}

"""


def send_msg(msg: List[Dict[str, str]], key) -> ChatResponse:
    """Send a message to openai

    Args:
        msg: A list of messages
        setup: The ChatSetup object

    Returns:
        The ChatCompletion object

    """

    openai.api_base = ChatSetup.api_base
    openai.api_key = key

    #TODO different parameters
    response = openai.ChatCompletion.create(
        model=ChatSetup.model,
        messages=msg,
    )

    return ChatResponse(response)


class ChatManager:
    """High-level interface for interaction with ChatGPT

    Attributes:
        cur_session: The current session
        sessions: A list of all sessions
        keys: A KeyGroup object managing key-related stuff

    Methods:
        set_session: Set the current session

    """

    def __init__(self) -> None:
        self.cur_session: Optional[Session] = None
        self.sessions: List[Session] = []
        self.keys: KeyGroup = KeyGroup()
        self.setup: ChatSetup = ChatSetup()

    def is_ready(self) -> bool:
        """Check if the ChatManager is ready to work

        TODO: Add hints for reasons of failure
        """

        # key check
        if not self.keys.has_key():
            return False

        # cur session check
        if self.cur_session is None:
            return False

        return True

    def add_key(self, name: str, key: str) -> None:

        self.keys.add_key(name, key)

    def send(self, msg: ChatMessage) -> Optional[ChatResponse]:
        """Send a message to openai

        Args:
            msg: The message to send

        Returns:
            ChatResponse if the ChatManager is ready, None otherwise

        """

        if not self.is_ready():
            # TODO: throw error
            return None

        return send_msg(msg.drain(), self.keys.get_key())


    def set_session(self, name: str) -> None:
        """Assign the current session

        If the session does not exist, create a new one.

        Args:
            name: The name of the session
        """

        session = self.get_session(name)
        if not session:
            self.sessions.append(session := Session(name))
        self.cur_session = session

    def get_session(self, name: str) -> Optional[Session]:
        """Get a session by name

        Args:
            name: The name of the session

        Returns:
            The session if it exists, None otherwise

        """

        for session in self.sessions:
            if session.name == name:
                return session
        return None

    def export_session(self, name: str, export_path: str, format: str = 'json') -> bool:
        """Export the current session

        Args:
            name: The name of the session
            format: The format of the export file

        Returns:
            True if the export is successful, False otherwise

        """

        if not (session := self.get_session(name)):
            # TODO: throw error
            return False

        handlers = {}

        if not (handler := handlers.get(format)):
            # TODO: throw error
            return False

        handler(export_path)
        return True
