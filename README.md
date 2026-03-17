# 🤖 CODEX: The Synthesis Agent
**Advanced Personal Assistant & Autonomous Blockchain Operator**

CODEX is a high-level, predictive AI assistant built for **The Synthesis Hackathon 2026**. It leverages a unique Dual-Engine architecture to bridge the gap between local system control and real-time global intelligence.

## 🚀 Key Features
* **Dual-Engine Reasoning:** Uses a **Fast Path Interceptor** for instant system commands and a **Chain-of-Thought LLM** for complex synthesis.
* **Blockchain Integration:** Integrated Web3 capabilities allow CODEX to check ETH prices, monitor wallet balances on Base and Sepolia, and execute transactions via voice or text.
* **Real-Time Knowledge Synthesis:** Automatically identifies when it lacks data and triggers a **SmartSearch** to gather and summarize live information from the web.
* **J.A.R.V.I.S. Specification UI:** A Matrix-inspired terminal interface with non-blocking processing and multi-threaded animations.
* **Full PC Automation:** Control volume, capture screenshots, manage applications, and access global news/weather without external APIs.

## 🏗️ Architecture
CODEX operates on a three-layer Thinking loop:
1.  **The Interceptor:** Analyzes input length and keywords to determine if the request is a local command or a knowledge topic.
2.  **The Brain:** If complex, the **Qwen 2.5 Coder 3B** model generates a JSON-based Thought and Tool Call plan.
3.  **The Synthesizer:** Aggregates data from tools and presents a grounded, professional response.

## 🛠️ Installation & Setup
1.  **Clone the Repo:**
    ```bash
    git clone https://github.com/Adithya17-star/codex-agent.git
    cd codex-agent
    ```
2.  **Install Dependencies:**
    ```bash
    pip install requests beautifulsoup4 ddgs pywin32 psutil pyautogui web3 python-dotenv
    ```
3.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```env
    CODEX_WALLET_ADDRESS=your_0x_address
    CODEX_PRIVATE_KEY=your_private_key
    ```
4.  **Launch CODEX:**
    ```bash
    python codex.py
    ```

## 🎥 Demo Script
1.  **System Control:** Type `open notepad` to demonstrate instant PC interaction.
2.  **Knowledge Synthesis:** Type `machine learning` or `IBM` to show the agent gathering and summarizing live web data.
3.  **Blockchain Mastery:** Type `my crypto balance` to show real-time interaction with the Base Mainnet and Sepolia Testnet.
