import psutil
import time
import subprocess

def get_user_input_paths():
    paths = []
    while True:
        try:
            # Ask the user to input a mount path or type 'exit' to finish
            user_input = input("Enter the mount path (or type 'exit' to finish): ").strip()

            # Exit condition if user types 'exit'
            if user_input.lower() == 'exit':
                break
            
            # Add the valid input to the paths list
            if user_input:
                paths.append(user_input)
            else:
                print("Invalid input. Please enter a valid path.")
        except KeyboardInterrupt:
            print("Ctrl+C\n")
            break
    return paths

def get_lv_path(mount_point):
    """Return the LV path based on the mount point."""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if partition.mountpoint == mount_point:
            return partition.device
    return None

def bash(command):
    # Run a bash command and return the output.
    try:
        # Run the command and capture the output
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode("utf-8")  # Return the output as a string
    except KeyboardInterrupt:
        print("Ctrl+C\n")
    except subprocess.CalledProcessError as e:
        # If the command fails, print the error
        return f"Error executing command: {e.output.decode('utf-8')}"


def usage(path):
    try:
        while True:
            try:
                usage = psutil.disk_usage(path)
                #print(f"{path} Usage: {usage.percent}%", end='\r')

                # Check if usage exceeds 80%
                if usage.percent > 10:
                    print("\nUsage exceeded 80%, extending LV...")

                    # Get the LV path based on the mount point
                    lv_path = get_lv_path(path)
                    print(lv_path)
                    if lv_path:
                        # Extend the LV by 500 MB (you can adjust the size as needed)
                        print("run first extend")
                        bash(f"sudo lvextend -L +500M {lv_path}")
                        print("echo extending...")
                         # LV path used here
                        bash(f"sudo resize2fs {lv_path}")
                        print("echo resizing the filesystem...") 
                         # Resize the filesystem (for ext4 or similar filesystems)
                        print(f"{path} was extened\n")
                    else:
                        print(f"LV path not found for mount point {path}.")
                        break
            
                time.sleep(1)  # Update every second
            except KeyboardInterrupt:
                print("Exiting...\n")

    except FileNotFoundError:
        print(f"\nThe path {path} is not mounted or doesn't exist.")
    except KeyboardInterrupt:
        print("\nStopped monitoring.")


"""
def usage(path):
    try:
        while True:
            usage = psutil.disk_usage(path)
            print(f"{path} Usage: {usage.percent}%", end='\r')
            if usage.percent > 80:
                print("\nUsage exceeded 80%, extending LV...")
                bash(f"sudo lvextend -L500 {path}")  # Extend the LV by 1 GB
                bash(f"sudo resize2fs {path}")  # Resize the filesystem (for ext4 or similar filesystems)
            time.sleep(1)  # Update every second
    except FileNotFoundError:
        print(f"\nThe path {path} is not mounted or doesn't exist.")
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

"""