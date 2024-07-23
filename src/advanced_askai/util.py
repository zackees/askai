import argparse
from getpass import getpass

from advanced_askai.openaicfg import create_or_load_config, save_config


def load_or_prompt_for_api_key_and_return_config(args: argparse.Namespace) -> dict:
    config = create_or_load_config()
    if args.set_key:
        config["openai_key"] = args.set_key
        save_config(config)
        config = create_or_load_config()
    elif "openai_key" not in config:
        key = getpass(
            "No OpenAI key found, please enter one now (input will be hidden): "
        )
        config["openai_key"] = key
        save_config(config)
    return config


def authentication_exists() -> bool:
    config = create_or_load_config()
    return "openai_key" in config


def get_authentication() -> str | None:
    config = create_or_load_config()
    key = config.get("openai_key")
    key = key or None
    return key
