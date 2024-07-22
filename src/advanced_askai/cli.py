"""askai - ask openai for help"""

import argparse
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


def _get_max_tokens(model: str) -> int:
    if model == ADVANCED_MODEL:
        return 4096
    return 16384


def _get_model_max_tokens(args: argparse.Namespace) -> tuple[str, int]:
    max_tokens = args.max_tokens
    model: str
    if args.model is None:
        if args.advanced:
            model = ADVANCED_MODEL
        else:
            model = FAST_MODEL
    else:
        model = args.model

    if max_tokens is None:
        max_tokens = _get_max_tokens(model)
    return model, max_tokens


def _load_or_prompt_for_api_key_and_return_config(args: argparse.Namespace) -> dict:
    config = create_or_load_config()
    if args.set_key:
        config["openai_key"] = args.set_key
        save_config(config)
        config = create_or_load_config()
    elif "openai_key" not in config:
        key = input("No OpenAi key found, please enter one now: ")
        config["openai_key"] = key
        save_config(config)
    return config


def _run_interactive_chat_session(
    chatbot: ChatBot, prompts: list[str], args: argparse.Namespace
) -> int:
    interactive = not args.prompt
    if interactive:
        print(
            "\nInteractive mode - press return three times to submit your code to OpenAI"
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


def cli() -> int:
    args = parse_args()
    config = create_or_load_config()
    if args.input_file:
        with open(args.input_file, "r") as file:
            args.prompt = file.read().strip()
    model: str
    max_tokens: int
    model, max_tokens = _get_model_max_tokens(args)

    config = _load_or_prompt_for_api_key_and_return_config(args)
    key = config["openai_key"]

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

    chatbot = ChatBot(
        openai_key=key,
        max_tokens=max_tokens,
        model=model,
        ai_assistant_prompt=ai_assistant_prompt,
        force_color=args.color,
    )

    rtn: int = _run_interactive_chat_session(
        chatbot=chatbot, prompts=prompts, args=args
    )
    return rtn


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
