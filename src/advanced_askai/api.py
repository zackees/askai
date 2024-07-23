from typing import Callable

from advanced_askai.chatgpt import ChatBot
from advanced_askai.interactive_chat_session import (
    internal_interactive_chat_session,
    internal_single_chat_session,
)
from advanced_askai.prompt_input import prompt_input
from advanced_askai.streams import ConsoleStream, Stream


def interactive_chat_session(
    chatbot: ChatBot,
    prompts: list[str] | None = None,
    outstream: Stream | None = None,
    as_json: bool = False,
    no_stream: bool = False,
    check: bool = False,
    status_print_func: Callable[[str], None] = print,
) -> None:
    """Runs a single chat query, throws exceptions if there are issues"""
    prompts = prompts or []
    outstream = outstream or ConsoleStream()
    return internal_interactive_chat_session(
        chatbot=chatbot,
        prompts=prompts,
        outstream=outstream,
        as_json=as_json,
        no_stream=no_stream,
        check=check,
        status_print_func=status_print_func,
        prompt_input_func=prompt_input,
    )


def single_query(
    chatbot: ChatBot,
    prompt: str | list[str],
    outstream: Stream | None = None,
    as_json: bool = False,
    no_stream: bool = False,
    check: bool = False,
    status_print_func: Callable[[str], None] = print,
) -> str:
    """Runs a single chat query, throws exceptions if there are issues"""
    outstream = outstream or ConsoleStream()
    if isinstance(prompt, str):
        prompts = [prompt]
    else:
        prompts = prompt
    return internal_single_chat_session(
        chatbot=chatbot,
        prompts=prompts,
        outstream=outstream,
        as_json=as_json,
        no_stream=no_stream,
        check=check,
        status_print_func=status_print_func,
    )
