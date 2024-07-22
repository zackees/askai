import argparse

from advanced_askai.constants import ADVANCED_MODEL, FAST_MODEL
from advanced_askai.openaicfg import create_or_load_config, save_config


def _get_max_tokens(model: str) -> int:
    if model == ADVANCED_MODEL:
        return 4096
    return 16384


def load_or_prompt_for_api_key_and_return_config(args: argparse.Namespace) -> dict:
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


def get_model_max_tokens(args: argparse.Namespace) -> tuple[str, int]:
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


def authentication_exists() -> bool:
    config = create_or_load_config()
    return "openai_key" in config
