# chatmanager

`chatmanager` provides various interfaces to facilitate the use of OpenAI API like ChatGPT. It supports functions including API key management, session managementm, and interaction with ChatGPT with multi-threads, and etc.

## Install

Download this repository:

```
git clone https://github.com/PeiweiHu/chatmanager.git
```

Build and install locally:

```
cd chatmanager 
./script/build.sh
```

## Quickstart

Here is an exmple to show how to use `chatmanager`.

```python
from chatmanager import ChatManager, ChatSetup, ChatMessage, ChatResponse

"""
ChatManager is the main interface that the user uses to send prompts and get the
response. 

ChatSetup stores the configurations.

ChatMessage is the interface to construct the prompts sent to the openai API.

ChatResponse parses and stores the responses from openai API.
"""

ChatSetup.api_base = "https://api.openai.com/v1" # default api_based

cm = ChatManager()

"""
Before communicating with the openai API, set a session. The session is used
to store the <ChatMessage, ChatResponse> pairs during the communication.

The following code set a session named session1.
"""
cm.set_session("session1")

"""
The following code adds new API keys, then sets the strategy for key usage.

Currently there are four strtegies:

    1. default/roll-polling: use in turn
    2. random: choose a random key
    3. least-used: choose the key that has been used the least
    4. rest-time: choose the key that has not been used for the longest time
"""
cm.add_key("key_name1", "sk-xxx")
cm.add_key("key_name2", "sk-yyy")
cm.keys.set_strategy("rest-time")


"""
To construct your prompt sent to ChatGPT (or other models), you can use ChatMessage.
"""
msg = ChatMessage()
msg.push_system("You are an assistant for programming")
msg.push_user("Can you write a loop in C language?")
response = cm.send(msg) # response: Optional[ChatResponse]

if response:
    msg1 = ChatMessage()

    """
    By the following two lines of code, we construct the <msg> and the
    response of <msg> in <msg1>.
    """
    msg1.push_msg(msg.drain())
    msg1.push_assistant(resposne.get_msg())

    new_query = "Is the above loop correct?"
    msg1.push_user(new_query)

    response = cm.send(msg1)

"""
You can also send multiple ChatMessage one time with multi-threads.
"""
msgs = [msg for _ in range(10)]
response_lst = cm.send(msgs, thread_num = 10) # response_lst: List[Optioanl[ChatResponse]]

"""
All the above communication with openai is saved in the session1.
You can export it.

You can also define the export manner. Please check the method export_session of
ChatManager.
"""

exported_json_str = cm.export_session("session1")
with open('log', 'w') as w:
    w.write(exported_json_str)
```
