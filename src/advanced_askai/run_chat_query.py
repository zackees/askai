"""askai - ask openai for help"""

import argparse
from typing import Optional

from advanced_askai.chatgpt import (
    ChatBot,
    ChatGPTAuthenticationError,
    ChatGPTConnectionError,
    ChatGPTRateLimitError,
    ChatStream,
)
from advanced_askai.openaicfg import save_config
from advanced_askai.streams import OutStream


def run_chat_query(
    chatbot: ChatBot,
    prompts: list[str],
    output_stream: OutStream,
    args: argparse.Namespace,
    print_status: bool,
) -> Optional[int]:
    # allow exit() and exit to exit the app
    as_json = args.json
    if not as_json:
        if print_status:
            print("############ OPEN-AI QUERY")
    try:
        chat_stream: ChatStream = chatbot.query(prompts, no_stream=args.no_stream)
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
    if as_json:
        print(chat_stream)
        return 0
    if chat_stream is None or not chat_stream.success():
        print("No error response received from OpenAI, response was:")
        output_stream.write(str(chat_stream.response()))
        return 1
    if not args.output:
        if print_status:
            print("############ OPEN-AI RESPONSE\n")
    response_text = ""
    for text in chat_stream:
        if text is None:
            break
        response_text += text
        output_stream.write(response_text)
    output_stream.write(response_text + "\n")
    prompts.append(response_text)
    return None
