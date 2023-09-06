import json
import os
from typing import Dict


class Session:
    """Store a session with ChatGPT

    Attributes:
        name: the name of this session
        repo: store the messages, order sensitive, {index: {role: message}}

    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.repo: Dict[int, Dict[str, str]] = dict()

    def set_repo(self, index: int, message: Dict[str, str]) -> None:
        self.repo[index] = message

    def repo_next_index(self) -> int:
        ks = self.repo.keys()
        if not ks:
            return 0
        return max(ks) + 1

    def set_system(self, system_prompt: str) -> None:
        system = {
            'role': 'system',
            'content': system_prompt,
        }
        self.set_repo(0, system)

    def push_message(self, message: Dict[str, str]) -> None:
        next_index = self.repo_next_index()
        self.set_repo(next_index, message)

    def export_json(self, jpath: str) -> None:
        assert (not os.path.exists(jpath))

        with open(jpath, 'w') as w:
            json.dump(self.repo, w, indent=4)

    def load_json(self, jpath: str) -> None:
        """ construct new repo by json """

        assert (os.path.exists(jpath))

        with open(jpath, 'r') as r:
            self.repo = {int(k): v for k, v in json.load(r).items()}
