import os
from typing import Callable, Optional

from advanced_askai.chatgpt import ChatBot
from advanced_askai.constants import AI_ASSISTANT_CHECKER_PROMPT
from advanced_askai.run_chat_query import run_chat_query
from advanced_askai.streams import NullOutStream, OutStream


def single_chat_session(
    chatbot: ChatBot,
    prompt: str,
    output: Optional[str],
    as_json: bool,
    no_stream: bool,
    check: bool,
) -> int:
    """Runs a single chat query, throws exceptions if there are issues"""
    output_stream: OutStream = OutStream(output)
    rtn: Optional[int] = None
    if check:
        # if we're checking, we need to use a null output stream
        output_stream.close()
        output_stream = NullOutStream()

    try:
        rtn = run_chat_query(
            chatbot=chatbot,
            prompts=[prompt],
            output_stream=output_stream,
            as_json=as_json,
            no_stream=no_stream,
            output=output,
            print_status=True,
        )
        if rtn is not None:
            return rtn

        if check:
            output_stream.close()
            output_stream = OutStream(output)
            check_prompt = AI_ASSISTANT_CHECKER_PROMPT + "\n\n" + prompt
            print("\n############ CHECKING RESPONSE")
            rtn = run_chat_query(
                chatbot=chatbot,
                prompts=[check_prompt],
                output_stream=output_stream,
                as_json=as_json,
                no_stream=no_stream,
                output=output,
                print_status=False,
            )
            output_stream.close()
            if rtn is not None:
                return rtn
    finally:
        output_stream.close()
    return 0


def interactive_chat_session(
    chatbot: ChatBot,
    prompts: list[str],
    prompt: Optional[str],
    output: Optional[str],
    as_json: bool,
    no_stream: bool,
    check: bool,
    prompt_input_func: Callable[[], str],
) -> int:
    """Runs a chat query, throws exceptions if there are issues"""
    interactive = not prompt
    if interactive:
        print(
            "\nInteractive mode - press return three times to submit your code to OpenAI"
        )
    while True:
        new_cmd = prompts[-1].strip().replace("()", "")
        if new_cmd.startswith("!"):
            prompts = prompts[0:-1]
            new_cmd = new_cmd[1:]
            rtn = os.system(new_cmd)
            print(f"Command exited and returned {rtn}")
            prompts.append(prompt_input_func())
            continue
        elif new_cmd == "exit":
            print("Exited due to 'exit' command")
            return 0

        rtn = single_chat_session(
            chatbot=chatbot,
            prompt="\n".join(prompts),
            output=output,
            as_json=as_json,
            no_stream=no_stream,
            check=check,
        )

        if rtn != 0:
            return rtn

        if not interactive:
            return 0

        # next loop.
        prompts.append(prompt_input_func())
