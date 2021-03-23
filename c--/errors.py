from helpers import tcolours


def semantic_error(cause, line=None):
    print_str = tcolours.red + "ERR: Semantic error" + tcolours.reset + " - {}".format(cause)

    if not (line is None):
        print_str += " at line {}".format(line)

    print(print_str)


def runtime_error(cause, line=None):
    print_str = tcolours.red + "ERR: Runtime error" + tcolours.reset + " - {}".format(cause)

    if not (line is None):
        print_str += " at line {}".format(line)

    print(print_str)