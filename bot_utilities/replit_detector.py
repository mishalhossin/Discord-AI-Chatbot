import os

def detect_replit():
    if "REPL_OWNER" in os.environ:
        return True
    return False

if __name__ == "__main__":
    if detect_replit():
        print("We are running on replit")