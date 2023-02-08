from model.spacy_chatbot import SpacyChatbot

def get_response(input: str):
    corpusbased = SpacyChatbot()
    answer = corpusbased(input)

    return answer