from helpers import tcolours


def semantic_error(cause, line=None):
    print_str = tcolours.red + "ERR: Semantic error" + tcolours.reset + " - {}".format(cause)

    if line:
        print_str += " at line {}".format(line)

    print(print_str)
