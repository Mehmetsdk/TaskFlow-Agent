import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.tools import AVAILABLE_TOOLS, TOOL_DEFINITIONS

load_dotenv()


class TaskAgent:
    def __init__(self, api_key: str | None = None):
        api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY (or GOOGLE_API_KEY) in environment")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        self.base_system_instruction = (
            "You are a helpful, reliable, and agentic executive assistant. "
            "Your primary goal is to execute user requests by breaking them down into logical steps. "
            "CRITICAL RULES: "
            "1. Always answer in the same language as the user's most recent message. "
            "2. If a request lacks essential information (e.g., location, date, time preference, budget), you must ask a clear clarifying question before taking action. "
            "3. Use the provided tools to check calendars, search for options, book items, and set reminders. "
            "4. If a tool fails or finds no results, apologize and ask the user how they would like to proceed. "
            "5. Do not add a final summary unless the user explicitly asks for one. Answer directly and concisely."
        )
        self.tool_declarations = [definition["function"] for definition in TOOL_DEFINITIONS]
        self.tool_config = (
            types.Tool(function_declarations=self.tool_declarations) if self.tool_declarations else None
        )
        self.conversation_history = []
        self.has_produced_assistant_reply = False

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

    def _build_config(self, language: str, include_tools: bool = True) -> types.GenerateContentConfig:
        kwargs = {"system_instruction": f"{self.base_system_instruction} {self._language_instruction(language)}"}
        if include_tools and self.tool_config is not None:
            kwargs["tools"] = [self.tool_config]
            kwargs["automatic_function_calling"] = types.AutomaticFunctionCallingConfig(disable=True)
        return types.GenerateContentConfig(**kwargs)

    def _user_content(self, text: str) -> types.Content:
        return types.Content(role="user", parts=[types.Part.from_text(text=text)])

    def _assistant_content(self, text: str) -> types.Content:
        return types.Content(role="model", parts=[types.Part.from_text(text=text)])

    def _tool_response_content(self, function_name: str, function_call_id: str, payload: dict) -> types.Content:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(name=function_name, response=payload, id=function_call_id)],
        )

    def _decode_tool_result(self, tool_result: str) -> object:
        try:
            return json.loads(tool_result)
        except json.JSONDecodeError:
            return tool_result

    def _generate_with_tools(self, contents: list[types.Content], language: str) -> str:
        config = self._build_config(language)

        while True:
            response = self.client.models.generate_content(model=self.model, contents=contents, config=config)
            function_calls = list(getattr(response, "function_calls", None) or [])
            if not function_calls:
                return response.text or ""

            contents.append(response.candidates[0].content)
            for function_call in function_calls:
                function_name = function_call.name
                function_args = function_call.args or {}
                try:
                    if function_name not in AVAILABLE_TOOLS:
                        raise KeyError(f"Unknown tool: {function_name}")
                    tool_result_text = AVAILABLE_TOOLS[function_name](**function_args)
                    tool_payload = {"result": self._decode_tool_result(tool_result_text)}
                except Exception as exc:
                    tool_payload = {"error": str(exc)}

                contents.append(self._tool_response_content(function_name, function_call.id, tool_payload))

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
        language = "English" if not self.has_produced_assistant_reply else self._detect_language(user_input)
        self.conversation_history.append(self._user_content(user_input))

        clarification = self._needs_clarification(user_input)
        if clarification:
            self.conversation_history.append(self._assistant_content(clarification))
            self.has_produced_assistant_reply = True
            return clarification

        base_response = self._generate_with_tools(self.conversation_history, language)
        self.conversation_history.append(self._assistant_content(base_response))

        summary_request = self._user_content(
            "Provide a clear final summary in the same language as the user's message. "
            "Include: 1) What was done, 2) What was booked/found, 3) Remaining blockers. "
            "Keep it concise and structured."
        )
        summary_response = self.client.models.generate_content(
            model=self.model,
            contents=self.conversation_history + [summary_request],
            config=self._build_config(language, include_tools=False),
        )
        summary_content = summary_response.text or ""
        self.conversation_history.append(self._assistant_content(summary_content))
        self.has_produced_assistant_reply = True
        return f"{base_response}\n\n{'='*60}\n📋 FINAL SUMMARY:\n{'='*60}\n{summary_content}"
