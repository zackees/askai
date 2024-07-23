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
) -> str:
    """Runs a single chat query, throws exceptions if there are issues"""
    output_stream: OutStream = OutStream(output)
    if check:
        # if we're checking, we need to use a null output stream
        output_stream.close()
        output_stream = NullOutStream()
    prompts = [prompt]
    try:
        response_text = run_chat_query(
            chatbot=chatbot,
            prompts=prompts,
            output_stream=output_stream,
            as_json=as_json,
            no_stream=no_stream,
            output=output,
            print_status=True,
        )
        if not check:
            return response_text
        prompts.append(response_text)
        output_stream.close()
        output_stream = OutStream(output)
        check_prompt = AI_ASSISTANT_CHECKER_PROMPT + "\n\n" + prompt
        prompts.append(check_prompt)
        print("\n############ CHECKING RESPONSE")
        response_text = run_chat_query(
            chatbot=chatbot,
            prompts=prompts,
            output_stream=output_stream,
            as_json=as_json,
            no_stream=no_stream,
            output=output,
            print_status=False,
        )
        output_stream.close()
        return response_text
    finally:
        output_stream.close()


def interactive_chat_session(
    chatbot: ChatBot,
    prompts: list[str],
    prompt: Optional[str],
    output: Optional[str],
    as_json: bool,
    no_stream: bool,
    check: bool,
    prompt_input_func: Callable[[], str],
    status_print_func: Callable[[str], None] = print,
) -> None:
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
            status_print_func(f"Command exited and returned {rtn}")
            next_prompt = prompt_input_func()
            prompts.append(next_prompt)
            continue
        elif new_cmd == "exit":
            status_print_func("Exited due to 'exit' command")
            return

        response_text = single_chat_session(
            chatbot=chatbot,
            prompt="\n".join(prompts),
            output=output,
            as_json=as_json,
            no_stream=no_stream,
            check=check,
        )
        prompts.append(response_text)

        if not interactive:
            return

        # next loop.
        prompts.append(prompt_input_func())
