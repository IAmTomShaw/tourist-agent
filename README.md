# Tourist Agent

I travel a lot for work, and one of the most frustrating parts is trying to find things to do during my free time when I'm in another country. It's not the biggest problem in the world, but it does make me feel like I'm missing out on experiences, especially when someone else has paid for the trip (might as well take advantage of it, right?).

So I've built this Python Streamlit app prototype to test a travel research agent that can help users discover things to do that fit around their schedule.

I think maybe some other features like an interests profile or budget constraints could be useful, but for now this is a simple demo to show how an agent could assist in travel planning. Hope you like it!

## Use case

- Quickly prototype a travel-recommendation UI for human-in-the-loop workflows.
- Demo agent progress and results in real-time for usability testing.
- Integrate with external services (OpenAI for LLMs, Google Calendar for scheduling) to automate parts of the travel workflow.

## Features

- Run Agent button to start an agent research session
- Real-time status updates while the agent runs
- Results grid displaying travel packages/options
- Select an option and start a new search

## Prerequisites

- Python 3.8+
- Google Cloud account (for Calendar API access)
- OpenAI account and API key (if using LLM features)
- Internet connection for API calls and Streamlit

## Quick start — local

1. Clone:

   ```bash
   git clone https://github.com/IAmTomShaw/tourist-agent.git
   cd tourist-agent
   ```

2. Create Python virtual environment and install:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. Environment variables

   - Create a `.env` file (optional) or export variables in your shell:

     ```bash
      OPENAI_API_KEY=sk-...
      OPENAI_MODEL=gpt-4o-mini
     ```

  Alternaitvely, you can copy the example.env file and modify it:

  ```bash
  cp example.env .env
  ```


4. Run:

   ```bash
   streamlit run app.py
   ```

Open http://localhost:8501 in your browser if Streamlit doesn't open it automatically.

## OpenAI API setup

1. Sign up at https://platform.openai.com/ and generate an API key.
2. Store the key in an environment variable:

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

   or add to your `.env` file and load it in your environment.
3. The app expects the key in process environment variable OPENAI_API_KEY. Replace usage in code if you use a different variable.

## Google Calendar API (GCP) setup

### Part 1. OAuth 2.0 Setup

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create or select a project.
3. Enable the Google Calendar API (APIs & Services > Library > Calendar API).
4. Configure OAuth consent screen (external/internal as required).
5. Create credentials > OAuth client ID > Desktop app (or Web app if you implement redirect).
6. Download the credentials JSON (commonly named `credentials.json`) and place it in your project directory or a secure location.
7. Use an OAuth flow (installed app) to obtain tokens. Many libraries (google-auth, google-auth-oauthlib) provide helpers for local authorization.

### Part 2. OAuth 2.0 Login

When running the app for the first time, it will prompt you to log in to your Google account and authorize access. This will generate and store the necessary tokens inside of a file (e.g., `tokens/gcal.json`) for subsequent API calls. You shouldn't need to do anything further after the initial login. If there are issues, check to see if the token file was created correctly.

## Usage

- Start the app and click "Run Agent" to emulate an agent research session.
- Watch the status feed for progress updates.
- Browse results in the grid;
- Click "Start New Search" to reset the UI and begin again.

## Troubleshooting

- Missing OPENAI_API_KEY: set the environment variable and restart Streamlit.
- Google Calendar auth errors: ensure API is enabled in GCP and your credentials are correct. For OAuth, verify redirect URIs and consent screen config.
- Streamlit port conflict: run `streamlit run app.py --server.port 8502` (choose an open port).

## Security reminders

- Never commit API keys or JSON credential files to Git.
- Use minimal IAM scopes needed for Calendar access.
- Rotate keys periodically and remove unused credentials.

## Contributing

- Open pull requests for UI improvements or agent integrations.
- Add tests and document new env vars or credential expectations.

## 📝 License

This project is licensed under the MIT License.

---

Built with ❤️ by [Tom Shaw](https://tomshaw.dev)