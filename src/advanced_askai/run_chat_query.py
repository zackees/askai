"""askai - ask openai for help"""

from typing import Optional

from advanced_askai.chatgpt import ChatBot, ChatStream
from advanced_askai.streams import OutStream


def run_chat_query(
    chatbot: ChatBot,
    prompts: list[str],
    output_stream: OutStream,
    as_json: bool,
    no_stream: bool,
    print_status: bool,
    output: Optional[str],
) -> str:
    """Runs a chat query, throws exceptions if there are issues. Returns the response text."""
    if not as_json:
        if print_status:
            print("############ OPEN-AI QUERY")
    chat_stream: ChatStream = chatbot.query(prompts, no_stream=no_stream)
    if as_json:
        return str(chat_stream)

    if chat_stream is None or not chat_stream.success():
        print("No error response received from OpenAI, response was:")
        output_stream.write(str(chat_stream.response()))
        raise Exception("No response from OpenAI")
    if not output:
        if print_status:
            print("############ OPEN-AI RESPONSE\n")
    response_text = ""
    for text in chat_stream:
        if text is None:
            break
        response_text += text
        output_stream.write(response_text)
    output_stream.write(response_text + "\n")

    # return None
    return response_text
