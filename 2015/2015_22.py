
# 22-Advent of Code 2015

from itertools import cycle


class Character():
    def __init__(self, hitpoints, mana):
        self.hitpoints = hitpoints
        self.mana = mana
        self.damage = 0
        self.armor = 0
        self.active_spells = []
        self.rotation = cycle(["idle"])

        self.spells = {
            "missile":{
                "mana_cost": 53,
                "mana_add": 0,
                "damage": 4,
                "armor": 0,
                "heal": 0,
                "rounds": 1,
                "text": "casts a mighty missile",
                },
            "drain":{
                "mana_cost": 73,
                "mana_add": 0,
                "damage": 2,
                "armor": 0,
                "heal": 2,
                "rounds": 1,
                "text": "drains life with vampiric attitude",
                },
            "shield":{
                "mana_cost": 113,
                "mana_add": 0,
                "damage": 0,
                "armor": 7,
                "heal": 0,
                "rounds": 6,
                "text": "shields herself",
                },
            "poison": {
                "mana_cost": 173,
                "mana_add": 101,
                "damage": 3,
                "armor": 0,
                "heal": 0,
                "rounds": 6,
                "text": "throws a flask of poison",
                },
            "recharge": {
                "mana_cost": 229,
                "mana_add": 101,
                "damage": 0,
                "armor": 0,
                "heal": 0,
                "rounds": 5,
                "text": "recharges mana",
                },
            "boss": {
                "mana_cost": 0,
                "mana_add": 0,
                "damage": 8,
                "armor": 0,
                "heal": 0,
                "rounds": 1,
                "text": "executes a boss attack",
                },
            "idle": {
                "mana_cost": 0,
                "mana_add": 0,
                "damage": 0,
                "armor": 0,
                "heal": 0,
                "rounds": 1,
                "text": "idles around, doing nothing",
                },
            }

    def deal_damage(self):
        return sum ([s['damage'] for s in self.active_spells])

    def spell_rotation(self):
        return "idle"

    def cast(self):
        cast = self.spell_rotation()
        spell = self.spells[cast]
        print(cast)
        self.mana -= spell['mana_cost']
        if cast != "boss" and spell in self.active_spells:
            print("CASTED A SPELL THAT IS ALREADY ON THE CUE")
        self.active_spells.append(self.spells[cast])
        return cast


    def spell_rotation(self):
        return next(self.rotation)


    def next_round(self):
        self.active_spells = [s for s in self.active_spells if s['rounds'] > 0]

        for s in self.active_spells:
            s['rounds'] -= 1
            self.mana += s['mana_add']
            self.hitpoints += s['heal']

class Boss(Character):
    def __init__(self):
        super().__init__(55, 0)
        self.damage += 8
        self.rotation = cycle(['boss'])

class Wizard(Character):
    def __init__(self):
        super().__init__(50, 500)
        self.rotation = cycle(["shield", "recharge", "poison", "missile", "drain", "missile"])


def calc_round():
    cast = wizard.cast()
    if wizard.mana < 0:
        return f"OOM.\nYou lost in round {game_round} with {wizard.hitpoints} / {wizard.mana} Mana, Boss has {boss.hitpoints} HP"
    boss.hitpoints -= wizard.deal_damage()

    if boss.hitpoints > 0:
        boss.cast()
        wizard.hitpoints = wizard.hitpoints - (boss.deal_damage() + wizard.armor)
    else:
        return f"Victory!\nYou Won in round {game_round} with {wizard.hitpoints} HP / {wizard.mana} Mana, Boss has {boss.hitpoints} HP"
    if wizard.hitpoints < 1:
        return f"Dead.\nYou lost in round {game_round} with {wizard.hitpoints}  HP/ {wizard.mana} Mana, Boss has {boss.hitpoints} HP"

    wizard.next_round()
    boss.next_round()
    return f"Spell Cast: {cast} Hitpoints: {wizard.hitpoints} Mana: {wizard.mana} Boss-hp: {boss.hitpoints}"

wizard = Wizard()
boss = Boss()

game_round = 0
while game_round < 25:
    result = calc_round()
    print(result)
    if "Won" in result or "lost" in result:
        break

    game_round += 1
