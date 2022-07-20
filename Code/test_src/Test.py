import os
import sys
sys.stdout.flush()

restart = input("\nDo you want to restart the program? [y/n] > ")
print(restart)
if restart == "y":

    os.execl(sys.executable, os.path.abspath(__file__),os.path.abspath(__file__), *sys.argv)
else:
    print("\nThe program will be closed...")
    sys.exit(0)