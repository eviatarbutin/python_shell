"""Python Eviatar Shell (PETH)

This script allows the user to create a shell that allows him:
    changing directories,
    listing directories,
    finding a pattern in a file/other input,
    using redirection,
    piping STDIN to STDOUT,
    exiting the shell safely. 

This script requires that python3 be installed with some of its common
default libraries: os, sys.

This file has also an instruction file with cool and useful features you can use.
The file also contains the following functions:

    * exit - function that exits from the program safely.
    * dir - function similar to dir in windows and ls in unix like systems.
    * cd - function similar to cd in windows and unix like systems.
    * find - function similar to file in windows and grep in unix like systems.
    * print_to_output - prints the output of the other functions to files and stdout.
    * main - the main function of the script that contains
             most of the input and shell handelling
"""

import os
import sys

g_append = False


def exit():
    """
        Function that exits from the program safely.
    """
    print("Thanks for using pesh")
    sys.exit(0)


def dir(input_: str, output: str, piped: bool) -> str:
    """Function similar to dir in windows and ls in unix like systems.

    Parameters
    ----------
    input_ : str
        The command and the path of the directory we are listing.
    output : str
        The path of the file we are sending the output into
        if equals "" the output is intended to stdin.
    piped : bool
        A flag used to figure if the print_to_output
        function should output the output to stdout
        or save it for the next command in the pipe.

    Returns
    -------
    str
        a list of files and directories for pipelining
    """
    input_ = input_.split()
    if len(input_) > 1:
        for dir in input_[1:]:
            if os.path.exists(dir):
                input_ = str(dir) + ":\n" + ", ".join(os.listdir(dir)) + "\n"
            else:
                print(f"dir: Cannot access '{dir}': No such file or directory")
                return ""
    else:
        input_ = ", ".join(os.listdir("."))

    print_to_output(input_, output, piped)
    return input_


def cd(input_: str):
    """Function similar to cd in windows and unix like systems.

    Parameters
    ----------
    input_ : str
        The command and the path of the directory we want to switch to.
    """
    input_ = input_.split()
    if len(input_) < 2:
        print(os.path.curdir)
    elif os.path.isdir(input_[1]):
        print(os.path.abspath(input_[1]))
        os.chdir(input_[1])
    else:
        print(f"cd: {input_[1]}: no such file or directory")


def find(input_: str, output: str, piped: bool) -> str:
    """Function similar to find in windows and grep in unix like systems.

    Parameters
    ----------
    input_ : str
        The command the word we are looking for and the string/files
        where we are looking for the word.
    output : str
        The path of the file we are sending the output into
        if equals "" the output is intended to stdin.
    piped : bool
        A flag used to figure if the print_to_output
        function should output the output to stdout
        or save it for the next command in the pipe.

    Returns
    -------
    str
        A list of lines where we found the searched word for pipelining.
    """
    # a special sign for a redirection or pipelined input
    if input_.endswith(".."):
        input_ = input_[:input_.find("..")-1].split() + [input_[input_.find("..")+2:]]
    else:
        input_ = input_.split()
    temp_input = ""
    # invalid input
    if len(input_) < 2:
        print("not enough arguments")
        return
    # waits for the output from the stdin and echoes if the pattern searched is in there
    # (exactly how the command behaves in windows)
    if len(input_) < 3:
        while True:
            try:
                temp = input()
                if input_[1] in temp:
                    print(temp)
            except KeyboardInterrupt:
                print("\n")
                return
    # looking for the pattern in the input sent from:
    # redirection, piping or/and multiple files
    elif len(input_) >= 3:
        flag = len(input_)
        if input_[-1].endswith(".."):
            temp_input += "piped input scan:\n"
            for line in input_[-1].split("\n"):
                if input_[1] in line:
                    temp_input += line + "\n"
            flag = -1
        for file_name in input_[2:flag]:
            if os.path.isfile(file_name):
                file = open(file_name, "r")
                content = file.read()
                temp_input += f"{file_name} scan:\n"
                for line in content.split("\n"):
                    if input_[1] in line:
                        temp_input += line + "\n"
                file.close()
            else:
                print("{} no such file".format(file_name))

    print_to_output(temp_input, output, piped)
    return temp_input


def print_to_output(input_: str, output: str, piped: bool):
    """Prints the output of the other functions to files and stdout.

    Parameters
    ----------
    input_ : str
        The contents the function need to write.
    output : str
        The path of the file we are sending the output into
        if equals "" the output is intended to stdin.
    piped : bool
        A flag used to figure if the print_to_output
        function should output the output to stdout
        or save it for the next command in the pipe.
    """
    output = output.replace(" ", "")
    if output == "":
        if not piped:
            print(input_)
    else:
        global g_append
        if g_append:
            file = open(output, "a+")
            g_append = False
        else:
            if os.path.exists(output):
                os.remove(output)
            file = open(output, "w+")
        file.write(input_)
        file.close()


def main():
    """
        Controls the shell the input and the redirection with the pipelining.
    """
    global g_append
    print("Welcome to pesh!")

    while True:
        # asking for a command
        first_input = input(os.path.abspath(os.path.curdir) + "=>")
        # first check of the input validity
        if len(first_input) > 0:
            if first_input.replace(' ', '')[0] in '|<>':
                print(f"pesh: Syntax error near unexpected token `{first_input.replace(' ', '')[0]}`")
                continue
        else:
            continue
        # spliting the input into different commands for pipeline controlling
        commands = first_input.split('|')
        input_ = ""
        output = ""
        # going through each command in the pipeline
        for command_index in range(len(commands)):
            # handeling redirections and setting inputs and outputs
            if '<' in commands[command_index]:
                temp = commands[command_index].split('<')
                if '>>' in temp[1]:
                    if os.path.isfile("".join("".join(temp[1]).replace(" ", "").split('>>')[0])):
                        with open("".join("".join(temp[1]).replace(" ", "").split('>>')[0]), "r") as file:
                            input_ = temp[0] + " .." + file.read() + ".."
                    else:
                        print("{} no such file".format(temp[1].replace(" ", "")))
                        continue
                    output = "".join(temp).split('>>')[1]
                    g_append = True
                elif '>' in temp[1]:
                    if os.path.isfile("".join(temp[1]).split('>>')[0]):
                        with open("".join(temp[1]).split('>>')[0], "r") as file:
                            input_ = temp[0] + " .." + file.read() + ".."
                    else:
                        print("{} no such file".format(temp[1].replace(" ", "")))
                        continue
                    output = "".join(temp).split('>')[1]
                else:
                    if os.path.isfile(temp[1].replace(" ", "")):
                        with open(temp[1].replace(" ", ""), "r") as file:
                            input_ = temp[0] + " .." + file.read() + ".."
                    else:
                        print("{} no such file".format(temp[1].replace(" ", "")))
                        continue
                    output = ""
            elif '>>' in commands[command_index]:
                temp = commands[command_index].split('>>')
                g_append = True
                input_ = temp[0]
                if output != "":
                    input_ = input_ + " " + ".." + "".join(output) + ".."
                output = temp[1]
            elif '>' in commands[command_index]:
                temp = commands[command_index].split('>')
                input_ = temp[0]
                if output != "":
                    input_ = input_ + " " + ".." + "".join(output) + ".."
                output = temp[1]
            else:
                if output == "":
                    input_ = commands[command_index]
                else:
                    input_ = commands[command_index] + " " + ".." + "".join(output) + ".."
                output = ""

            # performing the command
            if commands[command_index].split()[0] == "dir":         # has output
                output = dir(input_, output, (True if command_index < len(commands) - 1 else False) or output != "")
            elif commands[command_index].split()[0] == "cd":        # has no input no output
                cd(input_)
            elif commands[command_index].split()[0] == "find":      # has input and output
                output = find(input_, output, (True if command_index < len(commands) - 1 else False) or output != "")
            elif commands[command_index].split()[0] == "exit":      # has no input no output
                exit()
            elif commands[command_index].split()[0] == "help":      # has no input no output
                if os.path.isfile("README.md"):
                    with open("README.md", "r") as file:
                        print(file.read())
                else:
                    print("You should check the README file for more information about how to use the program.")
            else:
                print(f"Unknown command {commands[0]}")


if __name__ == "__main__":
    main()
