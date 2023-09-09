from typing import Dict, Optional, List, Callable, Tuple


class ChatMessage:
    """Construct the message for single interaction

    Attributes:
        repo: store the messages, order sensitive
    """

    def __init__(self) -> None:
        self.repo: List[Dict[str, str]] = list()

    def set_repo(self, index: int, message: Dict[str, str]) -> None:
        self.repo[index] = message

    def push_system(self, msg: str) -> None:
        self.push_msg({
            "role": "system",
            "content": msg
        })

    def push_user(self, msg: str) -> None:
        self.push_msg({
            "role": "user",
            "content": msg
        })

    def push_assistant(self, msg: str) -> None:
        self.push_msg({
            "role": "assistant",
            "content": msg
        })

    def push_msg(self, message: Dict[str, str]) -> None:
        self.repo.append(message)

    def del_msg(self, delete_checker: Callable[[Dict[str, str]], bool]) -> None:
        """ Delete the entries that satisfy delete_checker (i.e. return True) """

        self.repo = list(filter(lambda x: not delete_checker(x), self.repo))

    def drain(self) -> List[Dict[str, str]]:
        return self.repo


class ChatResponse:
    """Parse the response from openai

    Attributes:
        response: The response from openai

    Methods:
        token_usage: Get the number of tokens used
        choice_num: Get the number of choices
        get_msg: Get the message of a choice
    """

    def __init__(self, response) -> None:
        self.response = response

    def token_usage(self) -> int:
        return self.response["usage"]["total_tokens"]

    def choice_num(self) -> int:
        return len(self.response["choices"])

    def get_msg(self, choice:int = 0) -> Optional[str]:
        if choice >= self.choice_num():
            return None

        return self.response["choices"][choice]["message"]["content"]


class Session:
    """Log the interaction between user and openai

    Store each message and response in a list

    Attributes:
        name: The name of the session
        repo: The list of (message, response) tuples
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.repo: List[Tuple[ChatMessage, ChatResponse]] = list()

    def push(self, msg: ChatMessage, response: ChatResponse) -> None:
        self.repo.append((msg, response))
