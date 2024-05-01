import sys
from sympy import sympify

class Interpreter:
    
    def __init__(self):
        self.memory = {}

    #region print
    def print_message(self, message):
        if isinstance(message, int) or isinstance(message, float):
            print(message)
        elif message.startswith("$"):
            try:
                print(self.memory[message.replace("$", "")])
            except KeyError:
                print(f"Error: variable {message[1:]} is undefined!")
        else:
            print(message)
    #endregion

    #region calc
    @staticmethod
    def calc(expression):
        try:
            result = sympify(expression)
            if result.is_integer:
                return int(result)
            else:
                return result
        except (SyntaxError, ValueError):
            return None
    #endregion

    #region assign_value
    def assign_value(self, var_name, var_value):
        var_name.strip()  # Remove leading and trailing spaces
        self.memory[var_name] = var_value
    #endregion


class Run:
    def lexerize(self, line):
        command_mapping = {
            "print": interpreter.print_message,
            "calc": interpreter.calc,
            "equ": interpreter.assign_value
        }
        if line.startswith("//"):
            return  # Skip comments
        else:
            parts = line.strip().split("(")
            command_name = parts[0].strip()
            if len(parts) == 1:
                command_mapping[command_name]()
            else:
                args = "(".join(parts[1:]).rstrip(");").strip()
                if args == "":
                    print(f"Invalid {command_name} command format:", line)
                    return
                if "(" in args:
                    nested_parts = args.split("(")
                    nested_command_name = nested_parts[0].strip()
                    nested_args = [nested_parts[1].rstrip(")").strip()]
                    result = command_mapping[nested_command_name](*nested_args)
                    command_mapping["print"](result)
                else:
                    # Split the arguments based on commas
                    args = args.split(",")
                    # Strip each argument
                    args = [arg.strip() for arg in args]
                    # If it's an assignment command, split into var_name and var_value
                    if command_name == "equ":
                        var_name, var_value = args[0].replace(" ", ""), args[1]
                        interpreter.assign_value(var_name, var_value)
                    else:
                        command_mapping[command_name](*args)

#region run
import time

if __name__ == "__main__":
    start_time = time.perf_counter()  # Record the start time
    interpreterRun = Run()
    if len(sys.argv) != 2:
        print("Usage: python fir.py <file_name>")
    else:
        file_name = sys.argv[1]
        try:
            interpreter = Interpreter()
            with open(file_name, 'r') as file:
                for line in file:
                    interpreterRun.lexerize(line)
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")
    end_time = time.perf_counter()  # Record the end time

    # Calculate the execution time
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
#endregion