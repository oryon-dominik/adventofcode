from puzzle_handler import AdventPuzzleHandler, ReadFileAsPureFileMixin


class CustomCustoms(ReadFileAsPureFileMixin, AdventPuzzleHandler):

    puzzle_day = 6
    clean_data = False
    approaches = {
        'count yes': {"func": "process_customs_forms", "datatype": list},
        'count exclusive yes': {"func": "process_customs_forms", "datatype": list},
    }

    def clean_data(self, data):
        return "".join(data).split('\n\n')

    def get_answers(self, group) -> set:
        answers = set()
        for person in group.split('\n'):
            for answer in person:
                answers.add(answer)
        return answers

    def get_exclusive_answers(self, group) -> set:
        common_answers = set("abcdefghijklmnopqrstuvwxyz")
        for person in group.split('\n'):
            common_answers = set(common_answers).intersection(set(answer for answer in person))
        return common_answers

    def count_yes_in_group(self, group):
        if self.approach == "count yes":
            return len(self.get_answers(group))
        if self.approach == "count exclusive yes":
            return len(self.get_exclusive_answers(group))
        assert False, "Appoach not found"

    def process_customs_forms(self):
        return sum([self.count_yes_in_group(group) for group in self.data])


customs = CustomCustoms(approach="count yes", timeit=True)
print(f"{customs.text} | Task1 - count anyone answered yes: {customs.result} - {customs.time}")

customs = CustomCustoms(approach="count exclusive yes", timeit=True)
print(f"{customs.text} | Task2 - count everyone answered yes: {customs.result} - {customs.time}")
