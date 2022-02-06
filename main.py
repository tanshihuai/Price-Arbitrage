import time
import os

sleep_for = 10
iter = 1

if __name__ == '__main__':
    while True:
        print(f"Iteration {iter}")
        os.system("python application.py")
        print(f"Wating for {sleep_for} seconds...")
        print("---------------------------\n")
        time.sleep(sleep_for)
        iter += 1
