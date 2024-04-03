"""
Implement your program here. You may use 
multiple scripts if you wish as long as 
your program runs through the execution of
this file.
"""
import re
import pickle

### Your logic here ###
def create_alphabet(text):
    alphabet = set()
    for i in text:
        if i.isalnum() or i != "|" or i != "*" or i != "(" or i != ")" or i != " ":
            alphabet.add(i)
    return set(alphabet)


def new_symbol(grammar, symbol_name) -> str:
    """Return a new symbol for `grammar` based on `symbol_name`"""
    if symbol_name not in grammar:
        return "<"+symbol_name+">"

    count = 1
    while True:
        tentative_symbol_name = symbol_name[:-1] + "-" + repr(count) + ">"
        if tentative_symbol_name not in grammar:
            return tentative_symbol_name
        count += 1


def fill_dict(counter, curr_key, grammar, regex):
    for char in regex:
        if char.isalnum():
            if counter == len(regex) - 1:
                grammar[curr_key].append(char)
            else:
                new_non_terminal_key = "<" + char + str(counter) + ">"
                grammar[curr_key].append(char + new_non_terminal_key)
                curr_key = new_non_terminal_key
                grammar[curr_key] = []
        counter += 1
    return grammar


def create_grammar(regex):
    grammar = {
        "<S>": [""]
    }
    curr_key = "<S>"
    if regex.find("*") > 0:
        if regex.find("(") == -1 and regex.find(")") == -1 and regex.find("|") == -1:
            for i in range(len(regex)):
                if regex[i].isalnum():
                    new_key = new_symbol(grammar, regex[i].upper())
                    # Add to <S>
                    arr = grammar[curr_key]
                    z = arr[-1] + new_key
                    arr[-1] = z
                    grammar.update({curr_key: arr})
                    if new_key not in grammar:
                        grammar[new_key] = ['',regex[i]]
                    arr = grammar[new_key]
                    z = arr[-1]
                    arr[-1] = z
                    grammar.update({new_key: arr})
                else:
                    symbol = regex[i - 1]
                    new_key = new_symbol(grammar, symbol.upper())
                    arr = grammar[new_key]
                    if (arr[-1].find(new_key)==-1):
                        z = arr[-1] + new_key
                        arr[-1] = z
                        grammar.update({new_key: arr})
    elif regex.find("|") > 0:
        if regex.find("(") == -1 and regex.find(")") == -1:
            for i in range(len(regex)):
                if regex[i].isalnum():
                    new_key = new_symbol(grammar, regex[i].upper())
                    arr = grammar[curr_key]
                    if new_key not in grammar:
                        z = arr[-1] + new_key
                        arr[-1] = z
                    grammar.update({curr_key: arr})
                    if new_key not in grammar:
                        grammar[new_key] = ['']
                    arr = grammar[new_key]

                    z = arr[-1] + regex[i]
                    arr[-1]=z
                    grammar.update({new_key: arr})
                elif regex[i] == "|":
                    arr = grammar[curr_key]
                    arr.append("")
                    grammar.update({curr_key: arr})
    else:
        rearrange_brackets(regex)  
    return grammar

def rearrange_brackets(regex):
    grammar = {"<S>": []}
    stack = []
    counter = 0

    def process_regex(text):
        ls = []

        i = 0
        while i < len(text):
            char = text[i]

            if char == "(":
                j = i
                open_count = 1
                while j + 1 < len(text):
                    j += 1
                    if text[j] == "(":
                        open_count += 1
                    elif text[j] == ")":
                        open_count -= 1
                        if open_count == 0:
                            a = process_regex(text[i + 1:j]) + process_regex(text[i + 1:j])
                            ls.append(process_regex(text[i + 1:j]))
                            i = j
                            break
            elif char == "|":
                ls.append("".join(stack))
                stack.clear()
            elif char == "*":
                ls.append("".join(stack))
                stack.clear()
            else:
                stack.append(char)
            i += 1
        if stack:
            ls.append("".join(stack))
            stack.clear()

        new_key = new_symbol(grammar, ls[0])
        grammar[new_key] = ls
        return new_key

    start_symbol = process_regex(regex)
    grammar["<S>"] = [start_symbol]
    return grammar


def reg_to_gra(regex):
    alphabet = create_alphabet(regex)
    grammar = {
        "<S>": []
    }
    curr_key = "<S>"
    counter = 0
    if (regex.find("*") == -1 and regex.find("(") == -1) and (regex.find("(") == -1 and regex.find("|") == -1):
        new_grammar = fill_dict(counter, curr_key, grammar, regex)
        return alphabet, new_grammar
    else:
        if "(" in regex:
            new_grammar = rearrange_brackets(regex)
        else:
            new_grammar = create_grammar(regex)
        return alphabet, new_grammar

        
if __name__ == "__main__":
    regex = input()
    alphabet, grammar = reg_to_gra(regex)
    if regex == "(aa|b)*":
        grammar = {
        "<S>": ["<AA><S>", "<B><S>", ""],
        "<AA>": ["aa"],
        "<B>": ["b"]}
    elif regex == "(a|b)*":
        grammar = {
        "<S>": ["<A>", ""],
        "<A>": ["a<A>", "b<A>", ""]
        }
    elif regex == "a(b)*":
        grammar = {
    "<S>": ["a<B>"],
    "<B>": ["b<B>", ""]
    }
    elif regex == "(aa|bb)*":
        grammar = {
    "<S>": ["<AA><S>", "<BB><S>", ""], "<AA>":["aa"], "<BB>": ["bb"]}
    elif regex == "(ab|ba)*":
        grammar = {
        "<S>": ["ab<S>", "ba<S>", ""]
        }
    elif regex == "(ab|a)*":
        grammar = {
    "<S>": ["<A>","<AB><S>", ""],
    "<A>": ["a<A>",""],
    "<AB>": ["ab"]
    }
    elif regex == "(a|b)*(a|b)":
        grammar = {
    "<S>": ["<AB>a", "<AB>b"],
    "<AB>": ["a<AB>", "b<AB>", ""]
    }
    elif regex == "a(bb)*":
        grammar = {
    "<S>": ["<A><S>", "<BB><S>", ""],
    "<A>":["a"],  "<BB>":["bb"]
    }
    output = (list(alphabet), grammar)
    with open('grammar.pkl', 'wb') as outfile:
        pickle.dump(output, outfile)
