from messaging_client.messaging import Messaging
from time import sleep
from threading import Thread
import sys, readline, os

NAME = input("Username> ")
ADMIN = input("Admin? t/f> ")
if ADMIN.lower() == "t":
    ADMIN = True
elif ADMIN.lower() == "f":
    ADMIN = False
else:
    raise ValueError("Use t or f")

M = Messaging(NAME, ADMIN)
#Number of messages to grab at start
START_MESSAGES = 10

def print_with_input(text):
    """
    Prints around an input prompt

    Thank you jwmullally!
    https://stackoverflow.com/questions/2082387/reading-input-from-raw-input-without-having-the-prompt-overwritten-by-other-th
    """
    sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
    print(text)
    sys.stdout.write('> ' + readline.get_line_buffer())
    sys.stdout.flush()

def print_message(content):
    print_with_input("{}: {}".format(content["n"], content["c"]))

def recieve_messages():
    delay = 1
    while True:
        message = M.poll()
        if message["new"]:
            print_message(message["content"])

        sleep(delay)

def send_messages():
    while True:
        message = input("> ")
        #Forgot where I found this \/ solution, remove the prompt after input
        sys.stdout.write("\033[A                             \033[A \n")
        sys.stdout.flush()
        M.send_message(message)

def start():
    try:
        os.system('clear')
        i = START_MESSAGES
        while i != 0:
            #Grab last x messages
            message = M.get_message(M.last_message_id-i)
            print_message(message)
            i -= 1

        #Start thread to poll for messages
        recieve_thread = Thread(target=recieve_messages)
        recieve_thread.daemon = True
        recieve_thread.start()

        #Start waiting for input
        send_messages()

    except KeyboardInterrupt:
        print("Good Bye!")
        #Fixs buggy behavior when exiting
        os.system("reset")
        sys.exit()

    except:
        e = sys.exc_info()[0]
        print("Unexpected error {}".format(e))
        #Fixs buggy behavior when exiting
        os.system("reset")
        sys.exit()

if __name__ == "__main__":
    start()