import sys
sys.setrecursionlimit(10000)


def match(regex: str, ind: int, string: str) -> bool:
    if regex[ind:] == '':
        return True

    if regex[ind:] == '$' and string == '':
        return True

    if string == '':
        return False

    if regex[ind] == '\\':  # if '\'
        return ((regex[ind + 1] == string[0]) and  # match the symbol after '\' and the first string symbol
                match(regex, ind + 2, string[1:]))  # match the rest

    if len(regex) > ind + 1 and regex[ind + 1] == '?':  # if not the last symbol and next is '?'
        return (match(regex, ind + 2, string) or  # 0 occurrences
                match((regex[0:ind + 1] + regex[ind] + regex[ind + 2:]), ind + 1, string))  # 1 occurrence

    if len(regex) > ind + 1 and regex[ind + 1] == '*':  # if not the last symbol and next is '*'
        return (match(regex, ind + 2, string) or  # 0 occurrences
                match((regex[0:ind + 1] + regex[ind] + regex[ind + 2:]), ind + 1, string) or  # 1 occurrence
                match(regex, ind, string[1:]))  # more than 1 occurrence

    if len(regex) > ind + 1 and regex[ind + 1] == '+':  # if not the last symbol and next is '+'
        return (match((regex[0:ind + 1] + regex[ind] + regex[ind + 2:]), ind + 1, string) or  # 1 occurrence
                match(regex, ind, string[1:]))  # more than 1 occurrence

    return (regex[ind] in '.' or regex[ind] == string[0]) and match(regex, ind + 1, string[1:])


def entry_point(regex: str, string: str) -> bool:
    if regex.startswith('^'):
        return match(regex, 1, string)
    if regex == '':
        return True
    if string == '':
        return False
    return match(regex, 0, string) or entry_point(regex, string[1:])


def main():
    regex, string = input().split('|')
    print(entry_point(regex, string))


if __name__ == '__main__':
    main()
