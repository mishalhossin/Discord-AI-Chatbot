import os

def detect_replit():
    return "REPL_OWNER" in os.environ

if __name__ == "__main__":
    if detect_replit():
        print("We are running on replit")