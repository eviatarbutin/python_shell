Python Eviatar Shell (PETH)

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


PETH usage examples:
    * d: directory
    * f: file
    * ff: unlimited amount of files
    * p: pattern
    * a: anything

        exit                        exits
        exit a                      exits
        dir                         lists the current directory
        dir d                       lists the 'd' directory
        dir > f                     lists the current directory and writes the output to 'f'
        dir >> f                    lists the current directory and appends the output to 'f'
        dir d | find p              prints the lines with the pattern 'p' in the directory listing of 'd'
        dir d | find p > f          writes the lines with the pattern 'p' in the directory listing of 'd' into 'f'
        dir d | find p >> f         appends the lines with the pattern 'p' in the directory listing of 'd' into 'f'
        dir d | find p < ff         prints the lines with the pattern 'p' in the 'ff' files (in each one)
        (*ignores the dir pipeline output the redirection overrides it, simmilar to how it works in windows*)
        dir d | find p < ff > f     writes the lines with the pattern 'p' in the 'ff' files (in each one) into 'f' 
        (*ignores the dir pipeline output the redirection overrides it, simmilar to how it works in windows*)
        dir d | find p < ff >> f    appends the lines with the pattern 'p' in the 'ff' files (in each one) into 'f'
        (*ignores the dir pipeline output the redirection overrides it, simmilar to how it works in windows*)
        find p ff                   works exactly like: "dir d | find p < ff"                   
        find p                      waits for input and echoes the input if it contains the pattern 'p'
        (*as it works in windows if you dont give any input or files*)
        cd                          prints the current working directory
        cd d                        changes a directory to 'd'
        help                        prints this files if it exists in the directory

*There are more but I think its enough for now =)*