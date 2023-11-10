from typing import List
from langchain.schema import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage
)


def base_messages_to_default(messages: List[BaseMessage]):
    new_messages = []
    for message in messages:
        if message.type.lower() in ["system"]:
            new_messages.append(SystemMessage(content=message.content))
        elif message.type.lower() in ["human", "user"]:
            new_messages.append(HumanMessage(content=message.content))
        elif message.type.lower() in ["assisstant", "ai", "chat"]:
            new_messages.append(AIMessage(content=message.content))
        else:
            new_messages.append(message)
    return new_messages    
