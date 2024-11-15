from run_bash import *
from monitor import *
import threading

threads = []
paths = get_user_input_paths()
for path in paths:
    print(paths)

try:
    # Start the filling process in separate threads for each path
    """"""
    thread = threading.Thread(target=fill_method, args=(paths, ))
    threads.append(thread)
    thread.start()
    for path in paths:
        try:
            thread = threading.Thread(target=usage, args=(path, ))
            threads.append(thread)
            thread.start()
        except KeyboardInterrupt:
            print("you have exit\n")
    # Wait for threads to complete
    for thread in threads:
        thread.join()
except KeyboardInterrupt:
    print("Process interrupted by user.\n")
finally:
    print("Exiting program.")

command = "echo end"  # Example bash command
output = bash(command)
print(output)
