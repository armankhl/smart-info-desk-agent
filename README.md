# Smart Info-Desk Agent

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![GitHub repo size](https://img.shields.io/github/repo-size/your-username/smart-info-desk-agent)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A conversational AI agent built with Python that leverages the power of Large Language Models (LLMs) and function calling to answer user queries by intelligently interacting with multiple external APIs in real-time.

## 🚀 Demo

Here is an example of the agent's ability to handle a complex, multi-part query by calling two different APIs and synthesizing the results into a single, coherent answer.

```
> What's the weather like in Tokyo and what's the top news headline there?

Agent: Thinking...
Calling tool: get_weather with arguments: {'location': 'Tokyo'}
Calling tool: get_top_news with arguments: {'location': 'JP'}

Agent: The current weather in Tokyo is 15°C with clear skies. 
As for the news, the top headline from Japan is: "Bank of Japan hints at policy shift in upcoming meeting".
```

## ✨ Features

-   **Multi-Tool Capability:** The agent can seamlessly switch between different tools based on the user's request.
-   **Real-time Information:** Fetches up-to-the-minute data for:
    -   ☀️ **Weather:** Current conditions for any city (via OpenWeatherMap).
    -   📰 **News:** Top headlines for any country (via NewsAPI.org).
    -   💰 **Cryptocurrency:** Current prices for major coins (via CoinGecko).
    -   🎬 **Movies:** Quick summaries of popular films (via TMDB).
-   **Information Synthesis:** Can answer complex questions that require multiple data sources (e.g., "What's the weather and news in London?").
-   **Natural Conversation:** If a request doesn't require a tool, the agent can engage in simple conversation.
-   **Secure & Modular:** Uses `.env` for secure API key management and a clean, modular code structure.

## 🧠 Core Concepts Demonstrated

This project is a practical demonstration of key AI engineering principles:

-   **LLM Function Calling / Tool Use:** The core logic of prompting an LLM (Mistral via Together AI) to select the correct function and arguments from a predefined list to fulfill a user's request.
-   **Multi-API Integration:** Writing robust, reusable functions to interact with various third-party REST APIs.
-   **Stateful Conversational Loop:** Building a simple two-step agent loop (Think -> Act) that maintains context for synthesizing final answers.
-   **Secure Credential Handling:** Best practices for managing sensitive API keys outside of version control using environment variables.
-   **Environment Management:** Proper use of Python virtual environments (`venv`) and dependency management (`requirements.txt`) for reproducible builds.

## 🛠️ Technology Stack

-   **LLM Backend:** [Together AI](https://www.together.ai/) (specifically using models like `mistralai/Mixtral-8x7B-Instruct-v0.1`)
-   **Core Language:** Python 3.8+
-   **Key Libraries:**
    -   `together`: The official Python client for the Together AI API.
    -   `requests`: For making HTTP requests to external APIs.
    -   `python-dotenv`: For loading environment variables from the `.env` file.
-   **APIs:**
    -   [OpenWeatherMap API](https://openweathermap.org/api)
    -   [NewsAPI.org](https://newsapi.org/)
    -   [CoinGecko API](https://www.coingecko.com/en/api)
    -   [The Movie Database (TMDB) API](https://developer.themoviedb.org/docs)

## ⚙️ Setup and Installation

Follow these steps to get the agent running on your local machine.

### 1. Prerequisites

-   Python 3.8 or higher
-   Git

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/smart-info-desk-agent.git
cd smart-info-desk-agent
```

### 3. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

The agent requires API keys to function. These are managed in an `.env` file.

**a.** Create a file named `.env` in the root of the project directory. You can do this by copying the example file:

```bash
cp .env.example .env
```

**b.** Open the `.env` file and add your personal API keys. You will need to sign up for the free tiers of the following services:

-   [Together AI](https://www.together.ai/)
-   [OpenWeatherMap](https://openweathermap.org/api)
-   [NewsAPI.org](https://newsapi.org/)
-   [The Movie Database (TMDB)](https://www.themoviedb.org/signup)

Your `.env` file should look like this:

```ini
# .env
TOGETHER_API_KEY="your_together_ai_api_key"
OPENWEATHERMAP_API_KEY="your_openweathermap_api_key"
NEWSAPI_API_KEY="your_newsapi_key"
TMDB_API_KEY="your_tmdb_api_key"
```

> **Note:** The `.env` file is included in `.gitignore` to ensure your secret keys are never committed to version control.

## ▶️ Usage

Once the setup is complete, you can start the agent by running the main script:

```bash
python main.py
```

The application will launch in your terminal, and you can start asking it questions. To exit the conversation, type `quit` or `exit`.

## 📂 Project Structure

```
smart-info-desk-agent/
├── .gitignore          # Tells Git which files to ignore
├── .env.example        # Template for environment variables
├── README.md           # You are here!
├── main.py             # Main application entry point, conversational loop
├── requirements.txt    # List of Python dependencies
└── tools.py            # Contains all functions that call external APIs
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.