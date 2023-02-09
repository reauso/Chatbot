from chatbotsclient.chatbot import Chatbot
from chatbotsclient.message import Message
from typing import List

from model.spacy_chatbot import SpacyChatbot


def compute_answer(message: str, conversation: List[Message]):
    # Corpus based chatbot answer
    corpusbased = SpacyChatbot()
    answer = corpusbased(input)

    # template based chatbot answer

    return answer


def respond(message: Message, conversation: List[Message]):
    answer = compute_answer(message.message, conversation)
    return answer


if __name__ == "__main__":
    print("Shall we endeavor to forge a link with other digital conversationalists?")
    print("Affirm with 'yes', and negate with 'no'... a simple enough task, I should think.")
    user_input = input(">>> ").lower().strip()

    if(user_input == "yes"):
        chatbot = Chatbot(respond, "TyrionBot")

    else:
        print("Very well, you have leave to speak, but choose your words wisely.")
        user_input = input(">>> ").lower().strip()
        while "exit" not in user_input.lower():

            answer = compute_answer(user_input)

            print(answer)
            user_input = input(">>> ").lower().strip()
