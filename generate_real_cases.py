import random

def generate_test_case(size: int, case_type: str, algorithm: str) -> (str, str):
    random.seed(42)
    base_pattern_length = 15

    if algorithm == 'naive':
        if case_type == 'best':
            pattern = 'a' * base_pattern_length
            text = pattern + ''.join(random.choices('bcdefghijklmnopqrstuvwxyz', k=size - len(pattern)))
        elif case_type == 'worst':
            pattern = 'a' * (base_pattern_length - 1) + 'b'
            text = 'a' * size

    elif algorithm == 'kmp':
        if case_type == 'best':
            pattern = 'a' * base_pattern_length
            text = pattern + 'b' + 'x' * (size - len(pattern) - 1)
        elif case_type == 'worst':
            pattern = 'a' * (base_pattern_length // 2) + 'b' + 'a' * (base_pattern_length // 2)
            text = ('a' * (base_pattern_length // 2) + 'c') * (size // (base_pattern_length // 2 + 1))

    elif algorithm == 'boyer_moore':
        if case_type == 'best':
            pattern = 'z' + 'y' * (base_pattern_length - 1)
            text = 'x' * (size - base_pattern_length) + pattern
        elif case_type == 'worst':
            pattern = 'a' * (base_pattern_length // 3) + 'b' * (base_pattern_length // 3 * 2)
            text = (('a' * (base_pattern_length // 3)) + ('c' * (base_pattern_length // 3)))
            text *= (size // (base_pattern_length // 3 * 2))

    elif algorithm == 'rabin_karp':
        if case_type == 'best':
            pattern = 'a' * base_pattern_length
            text = pattern + ''.join(random.choices('bcdefghijklmnopqrstuvwxyz', k=size - len(pattern)))
        elif case_type == 'worst':
            pattern = 'a' * base_pattern_length
            text = ('a' * (base_pattern_length - 1) + 'b') * (size // base_pattern_length)

    if case_type == 'random':
        pattern = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=base_pattern_length))
        text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=size))

    return text, pattern