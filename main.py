# main.py
import unicodedata
from agent import run_agent

if __name__ == "__main__":
    while True:
        user_input = input("🗣️ Ne yapmak istersiniz? > ")
        user_input = unicodedata.normalize('NFKD', user_input).encode('ascii', 'ignore').decode('ascii')
        run_agent(user_input)
