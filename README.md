# 🤖 AI Agentic Task Execution Agent

A sophisticated AI agent that understands user requests, breaks them into logical steps, uses provided tools intelligently, and delivers reliable task execution with structured summaries.

## 📋 Overview

This agent demonstrates advanced prompt engineering, tool orchestration, and context management. It can:

- Understand and interpret complex user requests
- Break tasks into logical subtasks
- Ask clarifying questions when needed
- Use provided tools (calendar, search, booking, reminders)
- Handle failures gracefully
- Provide structured final summaries with:
  - ✓ What was done
  - ✓ What was booked/found
  - ✓ Remaining blockers

## 🎯 Example Tasks

The agent can handle requests like:

- "Book me a dentist appointment next week after 5pm."
- "Find me 3 coworking spaces in Warsaw under $20/day."
- "Plan a 2-day trip to Prague under €300."
- "Schedule a meeting with John next Tuesday afternoon."

## 🚀 Quick Start

### Prerequisites

- Python 3.14+ (as specified in `.python-version`)
- `uv` package manager
- Groq API key (get one free at https://console.groq.com)

### Installation

1. **Clone the repository:**

```bash
git clone <your-repo-url>
cd agent-assignment
```

2. **Install dependencies with uv:**

```bash
uv sync
```

3. **Set up your environment:**

```bash
cp .env.example .env
```

4. **Add your Groq API key to `.env`:**

```bash
GROQ_API_KEY=your_groq_api_key_here
```

### Running the Desktop App

```bash
uv run python main.py
```

Or using the virtual environment directly:

```bash
.\.venv\Scripts\python.exe main.py
```

If you prefer a one-click Windows launcher, double-click `launch_chat.bat`.

## 📖 Usage

When the app opens, you'll see a separate desktop chat window.

Type your request, then click **Send** or press **Ctrl+Enter**.

Examples:

- "Bana bir dişçi randevusu ayarla"
- "Find hotels in Warsaw"
- "Check my calendar for next Tuesday afternoon"

Use **Clear** to reset the chat, or close the window to exit.

## 🏗️ Project Structure

```
agent-assignment/
├── .env                      # Your API keys (DO NOT COMMIT)
├── .env.example              # Template for .env
├── .python-version           # Python version specification
├── .gitignore                # Git ignore rules
├── pyproject.toml            # Project metadata and dependencies
├── uv.lock                   # Locked dependencies
├── README.md                 # This file
├── main.py                   # Desktop app entry point
├── launch_chat.bat           # Windows launcher for the desktop app
├── launch_chat.ps1           # PowerShell launcher for the desktop app
└── src/
   ├── agent/
   │   ├── __init__.py       # Exports TaskAgent
   │   ├── core.py           # Shared agent helpers
   │   └── orchestrator.py   # TaskAgent class with orchestration
   ├── desktop_app.py        # Tkinter chat window
    ├── tools.py              # Tool definitions and implementations
   └── __init__.py           # Package initialization
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

⚠️ **SECURITY WARNING:**

- **NEVER commit `.env` to version control** (it's in `.gitignore`)
- Keep your API keys private and secure
- Use different API keys for development and production
- Rotate keys regularly if compromised

The agent will validate that a valid API key is provided on startup.

### Supported Models

Currently uses **Groq's Llama 3.3 70B Versatile** model for optimal performance:

- Fast inference
- Tool orchestration support
- Free tier available

## 🔧 Core Components

### TaskAgent (`src/agent/orchestrator.py`)

The main agent class that:

- Maintains conversation history
- Orchestrates tool calls
- Handles API interactions
- Generates structured summaries

**Key Methods:**

- `__init__()`: Initialize with API credentials
- `process_input(user_input)`: Process user requests and return results

### Desktop UI (`src/desktop_app.py`)

The Tkinter application that:

- Opens in a separate desktop window
- Sends messages to the agent in the background
- Keeps the UI responsive while the model is thinking
- Shows conversation history in a scrollable chat view

### Tools (`src/tools.py`)

Implemented tools for task execution:

1. **calendar_check(date_range)** - Check calendar availability
2. **search_service(query)** - Search for services/options
3. **booking_service(option)** - Book/execute selected options
4. **reminder_create(details)** - Create calendar reminders

Each tool includes mock implementations for demonstration.

## 📊 System Prompt Strategy

The agent uses a carefully engineered system prompt that:

- ✅ Ensures ENGLISH-only responses (regardless of input language)
- ✅ Enforces clarifying questions for missing information
- ✅ Guides tool usage and error handling
- ✅ Requires structured final summaries

## 🛠️ Dependency Management

This project uses **uv** instead of pip for deterministic builds:

```bash
# Install a package
uv add <package-name>

# Sync dependencies
uv sync

# Run the app with dependencies
uv run python main.py
```

The `uv.lock` file ensures reproducible environments across machines.

## ✅ Testing

Try these test cases to verify functionality:

```
1. Simple Q&A:
   "What is the capital of Turkey?"

2. Tool usage (Calendar):
   "Check my calendar for next Tuesday"

3. Search:
   "Find hotels in Istanbul under $100"

4. Complex task:
   "Book me a dentist appointment next Thursday afternoon"
```

## 🐛 Error Handling

The agent gracefully handles:

- ❌ Missing API credentials
- ❌ API failures and rate limits
- ❌ Invalid tool calls
- ❌ Incomplete user requests
- ❌ Tool execution errors

All errors are logged and the agent suggests corrective actions.

## 📝 Output Format

The agent provides responses in this format:

```
[Initial Response/Action]

============================================================
📋 FINAL SUMMARY:
============================================================

✓ What was done: [Actions taken]
✓ What was booked/found: [Results]
✓ Remaining blockers: [Any limitations or issues]
```

## 🎓 Design Decisions

1. **Groq over OpenAI**: Free, fast, and suitable for this use case
2. **Tool Orchestration**: Full loop for multi-step task execution
3. **English-only**: Simplifies prompt engineering and reduces errors
4. **Structured Summaries**: Meets assignment requirements for clear output
5. **uv Package Manager**: Modern, deterministic, and faster than pip

## 🚀 Future Enhancements

Potential improvements:

- Real calendar API integration (Google Calendar, Outlook)
- Real booking services (Stripe, booking.com APIs)
- Persistent conversation storage
- Multi-user support
- Advanced logging and metrics

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Development

### Setting up development environment:

```bash
# Clone and setup
git clone <url>
cd agent-assignment
uv sync

# Run tests
uv run python -m pytest

# Run the agent
uv run python main.py
```

### Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Push and create a Pull Request

---

## 💬 Quick Start (CLI "Go Live")

If your browser isn't available or you prefer the terminal, start the interactive CLI directly.

Windows (PowerShell):

```powershell
cd C:\Stajodev\agent-assignment
.\.venv\Scripts\python.exe main.py
```

Or use the provided one-click launchers:

- Double-click `launch_chat.bat` (Windows)
- Right-click and `Run with PowerShell` on `launch_chat.ps1`

These launchers run the CLI using the project's virtual environment and open an interactive prompt where you can ask the AI questions.

### Web launcher (starts server and opens browser)

If you want the web UI to open automatically (this avoids VS Code Live Server on port 5500 opening a file list), use the web launcher which starts the FastAPI server and opens the browser at the chat UI:

- Double-click `launch_web.bat` (Windows)
- Right-click and `Run with PowerShell` on `launch_web.ps1`

If you see a VS Code Live Server (port 5500) file listing, close Live Server and use the launcher above or open `http://127.0.0.1:8001/` manually.

**Built with ❤️ using Python, Groq AI, and uv**
