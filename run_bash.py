import subprocess
import numpy as np
import os
from colorama import Fore

def bash(command):
    #Run a bash command and return the output.
    try:
        # Run the command and capture the output
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode("utf-8")  # Return the output as a string
    except subprocess.CalledProcessError as e:
        # If the command fails, print the error
        return f"Error executing command: {e.output.decode('utf-8')}"
    
# The eater function from before
def eater(path, size):  # size in MB
    try:
        # Generate random data of the exact size in bytes
        eat = os.urandom(int(abs(size) * 1024 * 1024))

        # Open the file in write mode and write the data
        with open(path, "wb") as f:  # Use "wb" to write bytes directly
            f.write(eat)
    except KeyboardInterrupt:
        print("You have exit using \"Ctrl+C\"")
    except Exception as e:
        # Catch and print the error with a colored message
        print(f"{Fore.RED}There was an error while writing into the path {path} -> {e}{Fore.RESET}")

# Define the distribution methods
def uniform_distribution_fill(size):
    # Uniform distribution (size in MB)
    return np.random.uniform(0, 1) * float(size)

def exponential_distribution_fill(size):
    # Exponential distribution (size in MB)
    return np.random.exponential(1) * float(size)

def standard_normal_distribution_fill(size):
    # Normal distribution (size in MB)
    return np.random.standard_normal() * float(size)

def fill_method(paths):
    print("Choose filling method distribution law: \n")
    print("\t(0) - Uniform Distribution\n ")
    print("\t(1) - Exponential Distribution\n ")
    print("\t(2) - Normal Standard Distribution\n ")
    
    try:
        x = int(input("> "))  # Convert input to integer
    except KeyboardInterrupt:
        print("You have exit using \"Ctrl+C\"")
    except ValueError:
        print("Invalid input. Please enter a valid option (0, 1, or 2).")
        return
    
    if x == 0:
        rand = uniform_distribution_fill
    elif x == 1:
        rand = exponential_distribution_fill
    elif x == 2:
        rand = standard_normal_distribution_fill
    else:
        print("Invalid choice. Exiting.")
        return
    
    # Ask for the size to be used for filling in MB
    try:
        size = int(input("Enter the size (in MB) to fill in each file: "))
    except KeyboardInterrupt:
        print("Exit using \"Ctrl+C\"")
    except ValueError:
        print("Invalid size input. Please enter a valid integer.\n")
        return
    names = 0
    while True:
        try:
            names += 1
            for path in paths:
                p = path + "/" + str(names)
                eater(p, rand(size))
        except KeyboardInterrupt:
            print("Fill was stopped!\n")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
