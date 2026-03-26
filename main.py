from agents.hr_agent import run_hr_agent
from core.config import ACCESS_TOKEN
token= ACCESS_TOKEN
if __name__ == "__main__":

    while True:
        user_input = input("\n💬 You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = run_hr_agent(user_input,token)

        print("\n🤖 Agent:", response)