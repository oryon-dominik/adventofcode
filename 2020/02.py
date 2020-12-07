import functools
import time
from pathlib import Path
import re
from puzzle_handler import AdventPuzzleHandler

class PasswordPhilosophy(AdventPuzzleHandler):

    approaches = {
            'regex': {"func": "regular_expression_solution", "datatype": list},
            'count': {"func": "count_solution", "datatype": list},
            'new_policy': {"func": "new_policy", "datatype": list},
        }
    puzzle_day = 2
    clean_data = False

    def count_solution(self) -> int:
        """we just split and count"""
        matches = 0
        for expression in self.data:
            m, n, char, password = re.split('-| |: ', expression)
            if int(m) <= password.count(char) <= int(n):
                matches += 1
        return matches

    def regular_expression_solution(self) -> int:
        """compile the pattern with regex (suitable for more complex patterns too)"""
        matches = 0
        for expression in self.data:
            m, n, char, password = re.split('-| |: ', expression)
            # TODO: fix the pattern below to match more complex patterns, e.g: [^{char}] (NOT the char)
            # pattern = re.compile(fr"({char}){{{m},{n}}}")
            # if pattern.match(password):
            if len(re.findall(char, password)) in range(int(m), int(n) + 1):
                matches += 1
        return matches

    def new_policy(self) -> int:
        """this solution is sloppy due to the lack of time"""
        matches = 0
        for expression in self.data:
            m, n, char, password = re.split('-| |: ', expression)
            try:
                position_one = password[int(m) - 1]
                position_two = password[int(n) - 1]
                # xor
                if (position_one == char) ^ (position_two == char):
                    matches += 1
            except IndexError:
                # attention! we'll pass silently here, no error handling
                pass

        return matches


philosophy = PasswordPhilosophy(approach='regex', timeit=True)
print(f"{philosophy.text} | Task1 - REGEX valid passwords: {philosophy.result} - {philosophy.time}")

philosophy = PasswordPhilosophy(approach='count', timeit=True)
print(f"{philosophy.text} | Task1 - COUNT valid passwords: {philosophy.result} - {philosophy.time}")

philosophy = PasswordPhilosophy(approach='new_policy', timeit=True)
print(f"{philosophy.text} | Task2 - NEW-POLICY valid passwords: {philosophy.result} - {philosophy.time}")
