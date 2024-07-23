"""askai - ask openai for help"""

import sys

from advanced_askai.chatgpt import (
    ChatBot,
    ChatGPTAuthenticationError,
    ChatGPTConnectionError,
    ChatGPTRateLimitError,
)
from advanced_askai.interactive_chat_session import interactive_chat_session
from advanced_askai.openaicfg import create_or_load_config, save_config
from advanced_askai.parse_args import parse_args
from advanced_askai.prompt_input import prompt_input
from advanced_askai.util import (
    get_model_max_tokens,
    load_or_prompt_for_api_key_and_return_config,
)


def cli() -> int:
    args = parse_args()
    config = create_or_load_config()
    if args.input_file:
        with open(args.input_file, "r") as file:
            args.prompt = file.read().strip()
    model: str
    max_tokens: int
    model, max_tokens = get_model_max_tokens(args)

    config = load_or_prompt_for_api_key_and_return_config(args)
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

    try:
        interactive_chat_session(
            chatbot=chatbot,
            prompt=prompt,
            prompts=prompts,
            output=args.output,
            as_json=args.json,
            no_stream=args.no_stream,
            check=args.check,
            prompt_input_func=prompt_input,
            status_print_func=print,
        )
    except ChatGPTConnectionError as err:
        print(err)
        return 1
    except ChatGPTAuthenticationError as e:
        print(
            "Error authenticating with OpenAI, deleting password from config and exiting."
        )
        print(e)
        save_config({})
        return 1
    except ChatGPTRateLimitError:
        print("Rate limit exceeded, set a new key with --set-key")
        return 1
    return 0


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
