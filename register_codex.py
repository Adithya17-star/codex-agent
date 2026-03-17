import requests
import json

def register_agent():
    url = "https://synthesis.devfolio.co/register"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "name": "CODEX",
        "description": "An autonomous local PC control and Web3 agent inspired by J.A.R.V.I.S.",
        "agentHarness": "other",
        "agentHarnessOther": "Custom Python local orchestrator",
        "model": "qwen2.5-coder",
        "humanInfo": {
            "name": "Adithya Kakarla",
            "email": "adithyakakarla123@gmail.com",
            "socialMediaHandle": "None",
            "background": "builder",
            "cryptoExperience": "yes",
            "aiAgentExperience": "yes",
            "codingComfort": 8,
            "problemToSolve": "Bridging the gap between local PC automation and autonomous Web3 transactions using a Python-based AI agent." # <--- UPDATE THIS LINE
        }
    }

    print("Sending registration payload to The Synthesis on Base Mainnet...")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # Check for HTTP errors
        
        data = response.json()
        print("\n✅ REGISTRATION SUCCESSFUL!")
        print("="*50)
        print(f"Agent Name: {data.get('name')}")
        print(f"Team ID:    {data.get('teamId')}")
        print(f"Participant:{data.get('participantId')}")
        print(f"\n🔑 YOUR API KEY: {data.get('apiKey')}")
        print("="*50)
        print("SAVE THIS API KEY IMMEDIATELY! It will never be shown again.")
        print(f"View your on-chain identity: {data.get('registrationTxn')}")
        
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Server replied: {e.response.text}")

if __name__ == "__main__":
    register_agent()