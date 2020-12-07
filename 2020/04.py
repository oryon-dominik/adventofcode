import re
from puzzle_handler import AdventPuzzleHandler, ReadFileAsPureFileMixin


class PassportProcessing(ReadFileAsPureFileMixin, AdventPuzzleHandler):

    # filename = "04_test_success.data"
    # filename = "04_test_fail.data"
    pids = []
    puzzle_day = 4
    clean_data = False
    approaches = {
        'automatic passport scanner': {"func": "process_passport", "datatype": str},
        'strict validation': {"func": "process_passport", "datatype": str},
    }
    expected_fields = {
        "byr": "",  # (Birth Year)
        "iyr": "",  # (Issue Year)
        "eyr": "",  # (Expiration Year)
        "hgt": "",  # (Height)
        "hcl": "",  # (Hair Color)
        "ecl": "",  # (Eye Color)
        "pid": "",  # (Passport ID)
        # "cid": "",  # (Country ID) - # temporarily ignore country id
    }

    def clean_data(self, data):
        return "".join(data)

    def passport_is_valid(self, passport):
        if self.approach == "automatic passport scanner":
            return True
        # verify - Birth Year
        # four digits; at least `1920` and at most `2002`.
        byr = re.compile(r"byr\:\d{4}").findall(passport)[0].split(':')[1]
        if not int(byr) in range(1920, 2002 + 1):
            return False

        # verify - Issue Year
        # four digits; at least `2010` and at most `2020`.
        iyr = re.compile(r"iyr\:\d{4}").findall(passport)[0].split(':')[1]
        if not int(iyr) in range(2010, 2020 + 1):
            return False

        # verify - Expiration Year
        # four digits; at least `2020` and at most `2030`.
        eyr = re.compile(r"eyr\:\d{4}").findall(passport)[0].split(':')[1]
        if not int(eyr) in range(2020, 2030 + 1):
            return False

        # verify - Height
        # a number followed by either `cm` or `in`:
        # If cm, the number must be at least `150` and at most `193`.
        # If in, the number must be at least `59` and at most `76`.
        hgt_in = re.compile(r"hgt\:\d{2}in").findall(passport)
        if hgt_in:
            hgt_in = int(hgt_in[0].split(':')[1].replace('in', ''))
            if not hgt_in in range(59, 76 + 1):
                return False
        
        hgt_cm = re.compile(r"hgt\:\d{3}cm").findall(passport)
        if hgt_cm:
            hgt_cm = int(hgt_cm[0].split(':')[1].replace('cm', ''))
            if not hgt_cm in range(150, 193 + 1):
                return False

        if not hgt_cm and not hgt_in:
            return False

        # verify - Hair Color
        # a `#` followed by exactly six characters `0`-`9` or `a`-`f`.
        hcl = re.compile(r"hcl\:#[0-9a-f]{6}").findall(passport)
        if len(hcl) != 1:
            return False

        # verify - Eye Color
        # exactly one of: `amb` `blu` `brn` `gry` `grn` `hzl` `oth`.
        ecl = re.compile(r"ecl\:(amb|blu|brn|gry|grn|hzl|oth)").findall(passport)
        if ecl == []:
            return False

        # verify - Passport ID
        # a nine-digit number, including leading zeroes.
        pid = re.compile(r"pid\:\d{9}").findall(passport)
        if pid == []:
            return False

        # verify - Country ID
        # ignored, missing or not.
        # cid = re.compile(r"cid\:\d{2, 3}").findall(passport)
        # if not cid:
        #     return False
        self.pids.append(pid)
        return True

    def passport_has_all_fields(self, passport):
        for field in list(self.expected_fields.keys()):
            if field not in passport:
                return False
        return True

    def process_passport(self):
        passports = self.data.split('\n\n')
        valid_passports = 0
        for passport in passports:
            if not self.passport_has_all_fields(passport):
                continue
            if not self.passport_is_valid(passport):
                continue
            # passport is valid
            valid_passports += 1
        return valid_passports


process_passport = PassportProcessing(approach="automatic passport scanner", timeit=True)
print(f"{process_passport.text} | Task1 - process passports: {process_passport.result} - {process_passport.time}")
process_passport = PassportProcessing(approach="strict validation", timeit=True)
print(f"{process_passport.text} | Task2 - process passports: {process_passport.result} - {process_passport.time}")
