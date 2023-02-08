from chatbotsclient.chatbot import Chatbot
from chatbotsclient.message import Message
from chatbot import get_response
from typing import List


def compute(message: str, conversation: List[Message]):
    return get_response(message)


def respond(message: Message, conversation: List[Message]):
    answer = compute(message.message, conversation)
    return answer


if __name__ == "__main__":
    ##model = SpacyChatbot()
    print("Shall we endeavor to forge a link with other digital conversationalists?")
    print("Affirm with 'yes', and negate with 'no'... a simple enough task, I should think.")
    user_input = input(">>> ").lower().strip()

    if(user_input == "yes"):
        chatbot = Chatbot(respond, "TyrionBot")

    else:
        print("Very well, you have leave to speak, but choose your words wisely.")
        user_input = input(">>> ").lower().strip()
        while "exit" not in user_input.lower():

            answer = get_response(user_input)

            print(answer)
            user_input = input(">>> ").lower().strip()
