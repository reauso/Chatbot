from chatbotsclient.chatbot import Chatbot
from chatbotsclient.message import Message
from typing import List

from model.spacy_chatbot import SpacyChatbot


def compute_answer(message: str, conversation: List[Message]=None):
    # Corpus based chatbot reply
    reply, similarity = corpus_based(message)
    print(similarity)

    # template based chatbot reply
    # TODO

    # default answer
    if similarity < 0.5:
        print('Sorry but I don`t know what you mean.')

    return reply


def respond(message: Message, conversation: List[Message]):
    return compute_answer(message.message, conversation)


if __name__ == "__main__":
    # initialize necessary objects
    corpus_based = SpacyChatbot()

    print("Shall we endeavor to forge a link with other digital conversationalists?")
    print("Affirm with 'yes', and negate with 'no'... a simple enough task, I should think.")
    user_input = input(">>> ").lower().strip()

    if user_input == "yes":
        chatbot = Chatbot(respond, "TyrionBot")

    else:
        print("Very well, you have leave to speak, but choose your words wisely.")
        user_input = input(">>> ").strip()
        while "exit" not in user_input.lower():

            answer = compute_answer(user_input)

            print(answer)
            user_input = input(">>> ").strip()
