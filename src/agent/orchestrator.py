import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.tools import AVAILABLE_TOOLS, TOOL_DEFINITIONS

load_dotenv()


class TaskAgent:
    def __init__(self, api_key: str | None = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY in environment")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"

        self.system_prompt = {
            "role": "system",
            "content": (
                "You are a helpful, reliable, and agentic executive assistant. "
                "Your primary goal is to execute user requests by breaking them down into logical steps. "
                "CRITICAL RULES: "
                "1. Always answer in the same language as the user's most recent message. "
                "2. If a request lacks essential information (e.g., location, date, time preference, budget), you must ask a clear clarifying question before taking action. "
                "3. Use the provided tools to check calendars, search for options, book items, and set reminders. "
                "4. If a tool fails or finds no results, apologize and ask the user how they would like to proceed. "
                "5. Do not add a final summary unless the user explicitly asks for one. Answer directly and concisely."
            ),
        }
        self.conversation_history = [self.system_prompt]

    def _detect_language(self, user_input: str) -> str:
        text = user_input.lower()
        turkish_markers = [
            "ı",
            "ş",
            "ğ",
            "ç",
            "ö",
            "ü",
            " merhaba",
            " nasılsın",
            "randevu",
            "saat",
            "yardım",
            "bana",
            "lütfen",
            "çünkü",
        ]
        if any(marker in text for marker in turkish_markers):
            return "Turkish"
        return "English"

    def _language_instruction(self, language: str) -> str:
        if language == "Turkish":
            return "Respond in Turkish."
        return "Respond in English."

    def _needs_clarification(self, user_input: str) -> str | None:
        text = user_input.lower()
        language = self._detect_language(user_input)

        appointment_keywords = [
            "randevu",
            "appointment",
            "book",
            "booking",
            "schedule",
            "ayarla",
            "rezerve",
            "reserve",
        ]
        search_keywords = ["find", "search", "ara", "bul", "look for"]

        has_appointment_intent = any(keyword in text for keyword in appointment_keywords)
        has_search_intent = any(keyword in text for keyword in search_keywords)

        if has_appointment_intent:
            missing_time = not any(
                keyword in text
                for keyword in [
                    "today",
                    "tomorrow",
                    "next",
                    "morning",
                    "afternoon",
                    "evening",
                    ":",
                    "am",
                    "pm",
                    "saat",
                    "gün",
                    "hafta",
                ]
            )
            missing_location = not any(
                keyword in text
                for keyword in [
                    "istanbul",
                    "ankara",
                    "warsaw",
                    "city",
                    "clinic",
                    "dentist",
                    "doctor",
                    "office",
                ]
            )

            if missing_time or missing_location:
                if language == "Turkish":
                    return (
                        "Yardım edebilirim. Lütfen şunları yaz: 1) tercih ettiğin tarih veya saat, "
                        "2) konum ya da klinik/şehir, 3) zaman tercihin (sabah/öğleden sonra/akşam)."
                    )
                return (
                    "I can help with that. Please tell me: 1) the preferred date or time, "
                    "2) the location or clinic/city, and 3) any time preference (morning/afternoon/evening)."
                )

        if has_search_intent:
            missing_location = not any(
                keyword in text
                for keyword in [
                    "istanbul",
                    "ankara",
                    "warsaw",
                    "paris",
                    "london",
                    "city",
                    "near me",
                ]
            )
            if missing_location:
                if language == "Turkish":
                    return (
                        "Seçenekleri arayabilirim ama önce konuma ihtiyacım var. Lütfen şehir ya da bölgeyi, "
                        "ayrıca varsa bütçe veya tercihlerini yaz."
                    )
                return (
                    "I can search for options, but I need the location first. Please tell me the city or area, "
                    "and any budget or preference you have."
                )

        return None

    def process_input(self, user_input: str) -> str:
        is_first_assistant_reply = not any(
            message.get("role") == "assistant" for message in self.conversation_history
        )
        language = "English" if is_first_assistant_reply else self._detect_language(user_input)
        self.conversation_history.append({"role": "user", "content": user_input})

        clarification = self._needs_clarification(user_input)
        if clarification:
            self.conversation_history.append({"role": "assistant", "content": clarification})
            return clarification

        language_instruction = {
            "role": "system",
            "content": self._language_instruction(language),
        }

        while True:
            messages = self.conversation_history + [language_instruction]
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, tools=TOOL_DEFINITIONS, tool_choice="auto"
            )
            message = response.choices[0].message
            if hasattr(message, "tool_calls") and message.tool_calls:
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
                    self.conversation_history.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": tool_result,
                        }
                    )
            else:
                base_response = message.content
                self.conversation_history.append({"role": "assistant", "content": base_response})
                summary_instruction = {
                    "role": "user",
                    "content": (
                        "Provide a clear final summary in the same language as the user's message. "
                        "Include: 1) What was done, 2) What was booked/found, 3) Remaining blockers. "
                        "Keep it concise and structured."
                    ),
                }
                summary_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history + [language_instruction, summary_instruction],
                )
                summary_content = summary_response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": summary_content})
                return f"{base_response}\n\n{'='*60}\n📋 FINAL SUMMARY:\n{'='*60}\n{summary_content}"
