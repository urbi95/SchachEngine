class Logger(object):
    def __init__(self):
        pass

    @staticmethod
    def log(string_message):
        print(string_message, end="")

    @staticmethod
    def enquire_use_nn():
        input_w = input("Use neural network for white? (y/n)")
        input_b = input("Use neural network for black? (y/n)")

        return get_bool_from_user_input(input_w), get_bool_from_user_input(input_b)


def get_bool_from_user_input(string):
    if string.lower() not in ["y", "yes", "n", "no"]:
        print("Invalid input. Interpreted as 'no'.")

    return string.lower() in ["y", "yes"]
