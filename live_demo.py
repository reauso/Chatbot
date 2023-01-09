from model.spacy_chatbot import SpacyChatbot

if __name__ == "__main__":
    model = SpacyChatbot()

    user_input = input(">>>")
    while "exit" not in user_input.lower():
        print(model(user_input))
        user_input = input(">>>")
