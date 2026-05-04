import unittest

from src.agent.orchestrator import TaskAgent


class DummyMessage:
    def __init__(self, content=None, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls


class DummyChoice:
    def __init__(self, message):
        self.message = message


class DummyResponse:
    def __init__(self, text=None, function_calls=None):
        self.text = text
        self.function_calls = function_calls or []
        self.candidates = [DummyCandidate(DummyMessage(content=text))]


class DummyCandidate:
    def __init__(self, content):
        self.content = content


class DummyCompletions:
    def __init__(self, messages):
        self._messages = messages

    def generate_content(self, **kwargs):
        self._messages.append(kwargs)
        if len(self._messages) == 1:
            return DummyResponse(text="Hello there")
        return DummyResponse(text="Final summary")


class DummyModels:
    def __init__(self, messages):
        self.generate_content = DummyCompletions(messages).generate_content


class DummyClient:
    def __init__(self):
        self.calls = []
        self.models = DummyModels(self.calls)


class AgentTest(unittest.TestCase):
    def _build_agent(self) -> TaskAgent:
        agent = TaskAgent.__new__(TaskAgent)
        agent.client = DummyClient()
        agent.model = "gemini-2.5-flash"
        agent.base_system_instruction = "stub"
        agent.tool_declarations = []
        agent.tool_config = None
        agent.conversation_history = []
        agent.has_produced_assistant_reply = False
        return agent

    def test_clarification_is_turkish(self):
        agent = self._build_agent()
        response = agent.process_input("Bana bir dişçi randevusu ayarla")
        self.assertIn("tarih veya saat", response)
        self.assertNotIn("FINAL SUMMARY", response)

    def test_english_reply_has_no_summary(self):
        agent = self._build_agent()
        response = agent.process_input("hi")
        self.assertIn("Hello there", response)
        self.assertIn("FINAL SUMMARY", response)

    def test_first_reply_defaults_to_english(self):
        agent = self._build_agent()
        response = agent.process_input("Merhaba")
        self.assertIn("Hello there", response)
        self.assertIn("Respond in English.", agent.client.calls[0]["config"].system_instruction)


if __name__ == "__main__":
    unittest.main()
