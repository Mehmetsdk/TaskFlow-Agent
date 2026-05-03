import os
import json
import logging
from typing import Any
from dotenv import load_dotenv
from groq import Groq
from src.tools import TOOL_DEFINITIONS, AVAILABLE_TOOLS

load_dotenv()
logger = logging.getLogger(__name__)

class TaskAgent:
    def __init__(self, api_key: str | None = None):
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in environment")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

        self.system_prompt = {
            "role": "system",
            "content": (
                "YOU MUST RESPOND ONLY IN ENGLISH. NO OTHER LANGUAGE. "
                "You are a helpful, reliable, and agentic executive assistant. "
                "Your primary goal is to execute user requests by breaking them down into logical steps. "
                "CRITICAL RULES: "
                "1. ALWAYS respond in English, even if the user asks in Turkish or any other language. Translate and respond in English only. "
                "2. If a request lacks essential information (e.g., location, date, time preference, budget), YOU MUST ASK a clear clarifying question before taking action. "
                "3. Use the provided tools to check calendars, search for options, book items, and set reminders. "
                "4. If a tool fails or finds no results, apologize and ask the user how they would like to proceed. "
                "5. Once the task is fully complete, provide a structured final summary stating: What was done, what was booked/found, and any remaining blockers."
            )
        }
        self.conversation_history = [self.system_prompt]

    def process_input(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto"
            )
            message = response.choices[0].message
            if hasattr(message, 'tool_calls') and message.tool_calls:
                self.conversation_history.append(message)
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args_str = tool_call.function.arguments
                    try:
                        function_args = json.loads(function_args_str)
                    except json.JSONDecodeError:
                        function_args = {}
                    if function_name in AVAILABLE_TOOLS:
                        tool_to_call = AVAILABLE_TOOLS[function_name]
                        tool_result = tool_to_call(**function_args)
                    else:
                        tool_result = json.dumps({"error": f"Unknown tool: {function_name}"})
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": tool_result
                    })
            else:
                base_response = message.content
                self.conversation_history.append({"role": "assistant", "content": base_response})
                self.conversation_history.append({
                    "role": "user",
                    "content": "Please provide a structured final summary with: 1) What was done, 2) What was booked/found, 3) Any remaining blockers. Format it clearly."
                })
                summary_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                )
                summary_content = summary_response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": summary_content})
                return f"{base_response}\n\n{'='*60}\n📋 FINAL SUMMARY:\n{'='*60}\n{summary_content}"
