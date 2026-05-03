import unittest
from src import tools

class ToolsTest(unittest.TestCase):
    def test_calendar_check(self):
        res = tools.calendar_check("next week")
        self.assertIn('status', res)

if __name__ == '__main__':
    unittest.main()
