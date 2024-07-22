"""
Unit test file.
"""

import subprocess
import sys
import unittest

from advanced_askai.cli import cli
from advanced_askai.util import authentication_exists

IS_AUTHENTICATED = authentication_exists()


class SinglePromptTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skipUnless(
        IS_AUTHENTICATED, "Authentication required to run this unit test"
    )
    def test_api(self) -> None:
        """Test command line interface (CLI)."""
        # rtn = os.system(COMMAND)
        # self.assertEqual(0, rtn)
        sys.argv.extend(
            [
                "Respond with HELLO",
            ]
        )
        result = cli()
        self.assertEqual(0, result)

    @unittest.skipUnless(
        IS_AUTHENTICATED, "Authentication required to run this unit test"
    )
    def test_cli(self) -> None:
        command = 'askai "Respond with HELLO"'
        output = subprocess.check_output(command, shell=True, text=True)
        self.assertIn("HELLO", output)

    @unittest.skipUnless(
        IS_AUTHENTICATED, "Authentication required to run this unit test"
    )
    def test_cli_advanced(self) -> None:
        command = 'askai "Respond with HELLO" --advanced'
        output = subprocess.check_output(command, shell=True, text=True)
        self.assertIn("HELLO", output)


if __name__ == "__main__":
    unittest.main()
