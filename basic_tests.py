import unittest
from algorithms import naive_search, kmp_search, boyer_moore_search, rabin_karp_search

ALGORITHMS = {
    'Naive': naive_search,
    'KMP': kmp_search,
    'BoyerMoore': boyer_moore_search,
    'RabinKarp': rabin_karp_search
}


class TestSubstringSearch(unittest.TestCase):
    def _run_test_case(self, text, pattern, expected):
        for name, func in ALGORITHMS.items():
            with self.subTest(algorithm=name):
                result = func(text, pattern)
                self.assertEqual(result, expected, msg=f'{name} failed on {text=} {pattern=}')

    def test_simple_match(self):
        self._run_test_case('abcdef', 'cd', 2)

    def test_no_match(self):
        self._run_test_case('abcdef', 'gh', -1)

    def test_match_at_start(self):
        self._run_test_case('abcdef', 'ab', 0)

    def test_match_at_end(self):
        self._run_test_case('abcdef', 'ef', 4)

    def test_full_match(self):
        self._run_test_case('abcdef', 'abcdef', 0)

    def test_single_char_match(self):
        self._run_test_case('abcdef', 'd', 3)

    def test_empty_pattern(self):
        self._run_test_case('abcdef', '', 0)

    def test_empty_text_and_pattern(self):
        self._run_test_case('', '', 0)

    def test_empty_text(self):
        self._run_test_case('', 'a', -1)

    def test_repeated_pattern(self):
        self._run_test_case('aaaaaa', 'aaa', 0)

    def test_pattern_longer_than_text(self):
        self._run_test_case('abc', 'abcd', -1)

    def test_large_input_match(self):
        text = 'a' * 10_000 + 'b'
        pattern = 'a' * 9999 + 'b'
        self._run_test_case(text, pattern, 1)


if __name__ == '__main__':
    unittest.main()
