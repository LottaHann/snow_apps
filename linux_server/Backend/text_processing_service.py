
def splitWords(textinput):
    """
    Split the input text into words.
    
    :param textinput: The input text to be split.
    :return: A list of words.
    """
    return textinput.split()  # Dela upp texten i ord


def text_exit_match(userInput):
    """
    Check if the user's input contains an exit command.
    
    :param userInput: The user's input text.
    :return: True if an exit command is found, False otherwise.
    """
    exit_list = ["out", "end", "exit", "bye", "goodbye", "stop", "close", "off"]
    userInput = splitWords(userInput)

    for attempt in exit_list:
        if attempt in userInput:
            print(f"Exit command detected: {attempt}")
            return True  # Avslutningsord har hittats
    return False

