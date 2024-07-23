"""
Unit test file.
"""

import unittest
from typing import Callable

from advanced_askai.chatgpt import ChatBot
from advanced_askai.constants import FAST_MODEL
from advanced_askai.interactive_chat_session import interactive_chat_session
from advanced_askai.streams import NullOutStream
from advanced_askai.util import authentication_exists, get_authentication

IS_AUTHENTICATED = authentication_exists()


def _fake_prompt_generator(return_values: list[str]) -> Callable[[], str]:
    idx = 0

    def func() -> str:
        nonlocal return_values
        nonlocal idx
        out = return_values[idx % len(return_values)]
        idx += 1
        assert idx <= len(return_values)
        return out

    return func


class InteractiveSessionTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skipUnless(
        IS_AUTHENTICATED, "Authentication required to run this unit test"
    )
    def test_api(self) -> None:
        """Test command line interface (CLI)."""
        # rtn = os.system(COMMAND)
        # self.assertEqual(0, rtn)
        openai_key = get_authentication()
        assert openai_key is not None

        chatbot = ChatBot(
            openai_key=openai_key,
            max_tokens=1024,
            model=FAST_MODEL,
            ai_assistant_prompt="You are a helpful assistant that always returns 'EXPECTED-MESSAGE', and nothing else",
            force_color=False,
        )
        interactive_chat_session(
            chatbot=chatbot,
            prompts=[],
            outstream=NullOutStream(),
            as_json=False,
            no_stream=True,
            check=False,
            prompt_input_func=_fake_prompt_generator(
                ["just respond with 'ok'", "just respond with 'no'", "exit"]
            ),
            status_print_func=print,
        )


if __name__ == "__main__":
    unittest.main()
