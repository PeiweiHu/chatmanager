import time
from collections import defaultdict

from chatmanager import ChatManager


class TestKeyStrategy:

    def testA(self):
        cm = ChatManager()
        cm.set_session('s1')
        cm.add_key('key1', 'sk-xxx1')
        cm.add_key('key2', 'sk-xxx2')
        cm.add_key('key3', 'sk-xxx3')

        # test default/roll-pooling
        cnt = defaultdict(int)
        for _ in range(5):
            k = cm.keys.get_key()
            assert (k)
            name = cm.keys.get_key_name(k)
            cnt[name] += 1
        assert (cnt['key1'] == 2)
        assert (cnt['key2'] == 2)
        assert (cnt['key3'] == 1)

        # test least-used
        cm.keys.set_strategy('least-used')
        assert (k := cm.keys.get_key())
        name = cm.keys.get_key_name(k)
        assert (name == 'key3')

        # test rest-time
        cm.keys.set_strategy('rest-time')
        time.sleep(0.5)
        cm.keys.get_key('key3')
        time.sleep(0.5)
        cm.keys.get_key('key2')
        time.sleep(0.5)
        assert (k := cm.keys.get_key())
        name = cm.keys.get_key_name(k)
        assert (name == 'key1')
