from typing import Optional


class ChatSetup:
    """ Setup openai interface

    """

    model: str = "gpt-3.5-turbo"
    api_base: str = "https://api.openai.com/v1"
    temperature: Optional[float] = None
    top_p: Optional[float] = None
