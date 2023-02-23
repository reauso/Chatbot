import os.path

from chatbotsclient.chatbot import Chatbot
from chatbotsclient.message import Message
from typing import List

from model.patternbased_chatbot import PatternBasedChatbot
from model.spacy_chatbot import SpacyChatbot
from model.ner import print_ner


def compute_reply(message: str, conversation: List[Message]=None):
    # define reply
    reply = {}

    # template based chatbot reply
    reply['pattern'] = patter_based(message)

    # Corpus based chatbot reply
    reply['corpus'], similarity = corpus_based(message)

    # default reply
    if similarity < 0.5:
        reply['default'] = 'Sorry but I don`t know what you mean.'

    return reply


def respond(message: Message, conversation: List[Message]):
    return compute_reply(message.message, conversation)


if __name__ == "__main__":
    # define necessary paths
    text_pattern_file = os.path.normpath(os.getcwd() + '/Data/text_patterns.json')

    # initialize necessary objects
    corpus_based = SpacyChatbot()
    patter_based = PatternBasedChatbot(text_pattern_file)

    print("Shall we endeavor to forge a link with other digital conversationalists?")
    print("Affirm with 'yes', and negate with 'no'... a simple enough task, I should think.")
    user_input = input(">>> ").lower().strip()

    if user_input == "yes":
        chatbot = Chatbot(respond, "TyrionBot")

    else:
        print("Very well, you have leave to speak, but choose your words wisely.")
        user_input = input(">>> ").strip()
        while "exit" not in user_input.lower():

            reply = compute_reply(user_input)
            print_ner(user_input)
            for key, value in reply.items():
                print('\t{}: {}'.format(key, value))
                print_ner(value)

            user_input = input(">>> ").strip()
