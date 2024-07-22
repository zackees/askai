"""askai - ask openai for help"""

import os
import sys
from typing import Optional

from advanced_askai.chatgpt import ChatBot
from advanced_askai.constants import (
    ADVANCED_MODEL,
    AI_ASSISTANT_CHECKER_PROMPT,
    FAST_MODEL,
)
from advanced_askai.openaicfg import create_or_load_config, save_config
from advanced_askai.parse_args import parse_args
from advanced_askai.prompt_input import prompt_input
from advanced_askai.run_chat_query import run_chat_query
from advanced_askai.streams import NullOutStream, OutStream


def cli() -> int:
    args = parse_args()
    config = create_or_load_config()
    max_tokens = args.max_tokens
    if args.fast:
        args.model = FAST_MODEL
        max_tokens = 16384
    if args.input_file:
        with open(args.input_file, "r") as file:
            args.prompt = file.read().strip()
    if args.model is None:
        if args.advanced:
            model = ADVANCED_MODEL
            max_tokens = 4096
        else:
            model = FAST_MODEL
            max_tokens = 16384
    else:
        model = args.model

    if args.code:
        return os.system("aicode")

    if args.set_key:
        config["openai_key"] = args.set_key
        save_config(config)
        config = create_or_load_config()
    elif "openai_key" not in config:
        key = input("No OpenAi key found, please enter one now: ")
        config["openai_key"] = key
        save_config(config)
    key = config["openai_key"]
    interactive = not args.prompt
    if interactive:
        print(
            "\nInteractive mode - press return three times to submit your code to OpenAI"
        )
    prompt = args.prompt or prompt_input()

    def log(*pargs, **kwargs):
        if not args.verbose:
            return
        print(*pargs, **kwargs)

    if args.assistant_prompt_file:
        with open(args.assistant_prompt_file, "r") as f:
            ai_assistant_prompt = f.read().strip()
    else:
        ai_assistant_prompt = args.assistant_prompt

    log(prompt)
    prompts = [prompt]

    force_color = args.color
    if force_color is None:
        force_color = False

    chatbot = ChatBot(
        openai_key=key,
        max_tokens=max_tokens,
        model=model,
        ai_assistant_prompt=ai_assistant_prompt,
        force_color=force_color,
    )

    while True:
        try:
            rtn: Optional[int] = None
            output_stream: OutStream = OutStream(
                args.output
            )  # needs to be created every time.
            if args.check:
                # if we're checking, we need to use a null output stream
                output_stream = NullOutStream()
            new_cmd = prompts[-1].strip().replace("()", "")
            if new_cmd.startswith("!"):
                prompts = prompts[0:-1]
                new_cmd = new_cmd[1:]
                rtn = os.system(new_cmd)
                print(f"Command exited and returned {rtn}")
                prompts.append(prompt_input())
                continue
            elif new_cmd == "exit":
                print("Exited due to 'exit' command")
                return 0
            rtn = run_chat_query(
                chatbot, prompts, output_stream, args, print_status=True
            )
            if rtn is not None:
                return rtn

            if args.check:
                output_stream = OutStream(
                    args.output
                )  # needs to be created every time.
                check_prompt = AI_ASSISTANT_CHECKER_PROMPT + "\n\n" + prompts[-1]
                prompts.append(check_prompt)
                print("\n############ CHECKING RESPONSE")
                rtn = run_chat_query(
                    chatbot, prompts, output_stream, args, print_status=False
                )
                if rtn is not None:
                    return rtn

            if not interactive:
                return 0

            # next loop.
            prompts.append(prompt_input())
        finally:
            output_stream.close()


def main() -> int:
    try:
        return cli()
    except KeyboardInterrupt:
        return 1
    except SystemExit as e:
        if isinstance(e.code, int):
            return e.code
        return 1


if __name__ == "__main__":
    sys.exit(main())
