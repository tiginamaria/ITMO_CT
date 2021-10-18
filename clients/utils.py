import re

from typing import Callable

camel_pattern = re.compile(r'([A-Z])')
underscore_pattern = re.compile(r'_([a-z])')
int_pattern = re.compile(r'^[+-]?[0-9]+$')
float_pattern = re.compile(r'^[+-]?[0-9]+\.[0-9]+$')


def preprocess_json(json, key_rule: Callable[[str], str], value_rule: Callable[[str], str]):
    if isinstance(json, dict):
        return {key_rule(key): preprocess_json(value, key_rule, value_rule) for key, value in json.items()}
    if isinstance(json, list):
        preprocessed_list = []
        for d in json:
            if isinstance(d, dict):
                preprocessed_list.append(preprocess_json(d, key_rule, value_rule))
            else:
                preprocessed_list.append(value_rule(d))
        return preprocessed_list
    return value_rule(json)


def str_to_number(value: str):
    if int_pattern.match(value):
        return int(value)
    if float_pattern.match(value):
        return float(value)
    return value


def camel_to_underscore(key: str):
    return camel_pattern.sub(lambda x: '_' + x.group(1).lower(), key[0].lower() + key[1:])


def underscore_to_camel(key: str):
    return underscore_pattern.sub(lambda x: x.group(1).upper(), key)
