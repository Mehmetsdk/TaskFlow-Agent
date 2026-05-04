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
    def __init__(self, message):
        self.choices = [DummyChoice(message)]


class DummyCompletions:
    def __init__(self, messages):
        self._messages = messages

    def create(self, **kwargs):
        self._messages.append(kwargs)
        return DummyResponse(DummyMessage(content="Hello there"))


class DummyChat:
    def __init__(self, messages):
        self.completions = DummyCompletions(messages)


class DummyClient:
    def __init__(self):
        self.calls = []
        self.chat = DummyChat(self.calls)


class AgentTest(unittest.TestCase):
    def _build_agent(self) -> TaskAgent:
        agent = TaskAgent.__new__(TaskAgent)
        agent.client = DummyClient()
        agent.model = "llama-3.3-70b-versatile"
        agent.system_prompt = {"role": "system", "content": "stub"}
        agent.conversation_history = [agent.system_prompt]
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
        self.assertIn("Respond in English.", str(agent.client.calls[0]["messages"]))


if __name__ == "__main__":
    unittest.main()
