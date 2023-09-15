"""
Manage the api keys
"""

import random
import time
from typing import List, Dict, Optional, Callable


class Key:

    def __init__(self, name: str, key: str) -> None:
        self.name: str = name
        self.key: str = key


class KeyGroup:
    """ Manage multiple api keys

    Attributes:
        keys: A collection of keys
        strategy: The strategy for choosing a key
        last_use_time: The time when each key was last used
        use_cnt: The number of times each key has been used
        key_index: Sorted names of the keys, used for roll-polling
        cur_key_index: Store the index of the next key to use in key_index

    """

    def __init__(self) -> None:
        self.keys: Dict[str, Key] = dict()
        self.strategy: Callable[[], str] = self.strategy_roll_polling
        self.last_use_time: Dict[str, float] = dict()
        self.use_cnt: Dict[str, int] = dict()
        self.key_index: List[str] = []
        self.cur_key_index: Optional[int] = None

    def has_key(self) -> bool:
        return len(self.keys) != 0

    def get_key(self, key_name: Optional[str] = None) -> Optional[str]:
        """ Get the next key to use according to strategy """

        if len(self.keys) == 0:
            return None

        if not key_name:
            name = self.strategy()
        else:
            name = key_name

        # update
        self.last_use_time[name] = time.time()
        self.use_cnt[name] += 1

        return self.keys[name].key

    def set_strategy(self, strategy: str) -> None:
        """Set the strategy for choosing a key

        default/roll-polling: use in turn
        random: choose a random key
        least-used: choose the key that has been used the least
        rest-time: choose the key that has not been used for the longest time

        """

        tab = {
            'default': self.strategy_roll_polling,
            'roll-polling': self.strategy_roll_polling,
            'random': self.strategy_random,
            'least-used': self.strategy_least_used,
            'rest-time': self.strategy_rest_time,
        }

        assert (strategy in tab), "Invalid strategy"

        self.strategy = tab[strategy]

    def strategy_roll_polling(self) -> str:
        """ all strategy functions return the name of the key """
        if self.cur_key_index is None:
            self.cur_key_index = 0
        else:
            self.cur_key_index = (self.cur_key_index + 1) % len(self.key_index)
        return self.key_index[self.cur_key_index]

    def strategy_random(self) -> str:
        return random.choice(list(self.keys.keys()))

    def strategy_least_used(self) -> str:
        return min(self.use_cnt, key=lambda k: self.use_cnt[k])

    def strategy_rest_time(self) -> str:
        cur_time = time.time()
        return max(self.last_use_time,
                   key=lambda k: cur_time - self.last_use_time[k])

    def update_key_status(self) -> None:
        self.key_index = sorted(self.keys.keys())
        self.cur_key_index = None

        def align_dict(dic, keys, val):
            """ Align the keys in dic with keys, and set the new value to val """

            new_key = keys - dic.keys()
            for _ in new_key:
                dic[_] = val
            [dic.pop(_) for _ in dic.keys() - keys]

        align_dict(self.use_cnt, self.keys.keys(), 0)
        align_dict(self.last_use_time, self.keys.keys(), 0)

    def key_value_exist(self, key: str) -> bool:
        """ Whether the key value exists """
        for _ in self.keys.values():
            if _.key == key:
                return True
        return False

    def key_name_exist(self, name: str) -> bool:
        """ Whether the key name exists """
        return name in self.keys

    def get_key_name(self, key: str) -> Optional[str]:
        """ Get the name of the key with the given value """

        for _ in self.keys.values():
            if _.key == key:
                return _.name
        return None

    def add_key(self, name: str, key: str) -> None:
        assert (not self.key_name_exist(name)), "Key name already exists"
        assert (not self.key_value_exist(key)), "Key value already exists"

        self.keys[name] = Key(name, key)
        self.update_key_status()

    def remove_key(self, name: str) -> None:
        assert (name in self.keys), "Key name does not exist"
        self.keys.pop(name)
        self.update_key_status()
