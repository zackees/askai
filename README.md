# advanced-askai

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)

A chatbot for your terminal. Has api bindings to run in python code.

# Help

```
usage: Ask OpenAI for help with code

positional arguments:
  prompt                Prompt to ask OpenAI

options:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
                        Input file containing prompts
  --json                Print response as json
  --set-key SET_KEY     Set OpenAI key
  --output OUTPUT       Output file
  --advanced            bleeding edge model: gpt-4o
  --model MODEL
  --verbose
  --no-stream
  --assistant-prompt ASSISTANT_PROMPT
  --assistant-prompt-file ASSISTANT_PROMPT_FILE
                        File containing assistant prompt
  --max-tokens MAX_TOKENS
                        Max tokens to return
  --code                Code mode: enables aider mode
  --check               Sends the response back to the chatbot for a second opinion
```

See advanced_askai.api.*

# Develope

To develop software, run `. ./activate.sh`

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.
