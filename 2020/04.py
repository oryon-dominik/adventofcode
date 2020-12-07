import re
import parse

from puzzle_handler import AdventPuzzleHandler, ReadFileAsPureFileMixin


class PassportProcessing(ReadFileAsPureFileMixin, AdventPuzzleHandler):

    # uncomment these filesnames for test-data:
    # filename = "04_test_success.data"
    # filename = "04_test_fail.data"
    pids = []
    puzzle_day = 4
    clean_data = False
    approaches = {
        'automatic passport scanner': {"func": "process_passport", "datatype": str},
        'strict validation regex': {"func": "process_passport", "datatype": str},
        'strict validation parse': {"func": "process_passport", "datatype": str},
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

    def passport_is_valid_parse(self, passport):
        # verify - Birth Year
        # four digits; at least `1920` and at most `2002`.
        byr = parse.search("byr:{:4d}", passport)
        if byr is None or not int(byr[0]) in range(1920, 2002 + 1):
            return False

        # verify - Issue Year
        # four digits; at least `2010` and at most `2020`.
        iyr = parse.search("iyr:{:4d}", passport)
        if iyr is None or not int(iyr[0]) in range(2010, 2020 + 1):
            return False

        # verify - Expiration Year
        # four digits; at least `2020` and at most `2030`.
        eyr = parse.search("eyr:{:4d}", passport)
        if eyr is None or not int(eyr[0]) in range(2020, 2030 + 1):
            return False

        # verify - Height
        # a number followed by either `cm` or `in`:
        # If cm, the number must be at least `150` and at most `193`.
        # If in, the number must be at least `59` and at most `76`.
        hgt_in = parse.search("hgt:{:2d}in", passport)
        hgt_cm = parse.search("hgt:{:3d}cm", passport)
        if hgt_cm is None and hgt_in is None:
            return False
        if hgt_in is not None and not int(hgt_in[0]) in range(59, 76 + 1):
            return False
        if hgt_cm is not None and not int(hgt_cm[0]) in range(150, 193 + 1):
            return False

        # verify - Hair Color
        # a `#` followed by exactly six characters `0`-`9` or `a`-`f`.
        hcl = parse.search("hcl:#{:x}", passport)
        if hcl is None:
            return False

        # verify - Eye Color
        # exactly one of: `amb` `blu` `brn` `gry` `grn` `hzl` `oth`.
        amb = parse.search("ecl:amb", passport)
        blu = parse.search("ecl:blu", passport)
        brn = parse.search("ecl:brn", passport)
        gry = parse.search("ecl:gry", passport)
        grn = parse.search("ecl:grn", passport)
        hzl = parse.search("ecl:hzl", passport)
        oth = parse.search("ecl:oth", passport)
        
        if not any([amb, blu, brn, gry, grn, hzl, oth]):
            return False

        # verify - Passport ID
        # a nine-digit number, including leading zeroes.
        pid = parse.search("pid:{:9w}", passport)
        if pid is None or len(pid[0]) != 9:
            return False

        return True


    def passport_is_valid_regex(self, passport):
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

        return True

    def passport_is_valid(self, passport):
        if self.approach == "automatic passport scanner":
            return True
        elif self.approach == "strict validation regex":
            return self.passport_is_valid_regex(passport)
        elif self.approach == "strict validation parse":
            return self.passport_is_valid_parse(passport)
        assert False, "Approach is not validating passports (yet)"

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

process_passport = PassportProcessing(approach="strict validation regex", timeit=True)
print(f"{process_passport.text} | Task2 - process passports REGEX: {process_passport.result} - {process_passport.time}")
print("This is not the correct solution for part 4 yet, I'm missing something in validation here.\nLet's try the parse module")

process_passport = PassportProcessing(approach="strict validation parse", timeit=True)
print(f"{process_passport.text} | Task2 - process passports PARSE: {process_passport.result} - {process_passport.time}")
print("This is the correct solution! :-)")
