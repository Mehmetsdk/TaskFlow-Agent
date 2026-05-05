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
- Groq API key

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

### Running the Agent (Popup UI)

```bash
uv run python main.py
```

Or using the virtual environment directly:

```bash
.\.venv\Scripts\python.exe main.py
```

## 📖 Usage

When the app starts, a desktop popup window will open.

Type your request into the input box and press **Enter** or click **Send**.

Examples:

- "Book me a dentist appointment"
- "Find hotels in Warsaw"
- "Check my calendar for next Tuesday afternoon"

Type `q`, `quit`, or `exit` to leave the app.

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
└── src/
   ├── agent/
   │   ├── __init__.py       # Exports TaskAgent
   │   ├── core.py           # Shared agent helpers
   │   └── orchestrator.py   # TaskAgent class with orchestration
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

### Tools (`src/tools.py`)

Implemented tools for task execution:

1. **calendar_check(date_range)** - Check calendar availability
2. **search_service(query)** - Search for services/options
3. **booking_service(option)** - Book/execute selected options
4. **reminder_create(details)** - Create calendar reminders

Each tool includes mock implementations for demonstration.

## 📊 System Prompt Strategy

The agent uses a carefully engineered system prompt that:

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

Run the automated checks locally:

```bash
# Run tests
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

# Run lint checks
.\.venv\Scripts\python.exe -m ruff check .
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

1. **Groq over Gemini**: Uses a fast hosted model with function calling support
2. **Tool Orchestration**: Full loop for multi-step task execution
3. **Language mirroring**: Starts with English on the first reply, then mirrors the user's language
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
uv run python -m unittest discover -s tests -v

# Run lint
uv run python -m ruff check .

# Run the desktop app
uv run python main.py
```

If the popup window does not appear, make sure the application is launched from the project root and that your `GROQ_API_KEY` is set in `.env`.

### Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Push and create a Pull Request

**Built with ❤️ using Python, Groq AI, and uv**
