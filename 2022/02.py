from handler import Puzzle, approach
from functools import cache


class RockPaperScissors(Puzzle):

    @cache
    def points_for_hand(self) -> dict:
        return {'rock': 1, 'paper': 2, 'scissors': 3}

    @cache
    def points_for_results(self) -> dict:
        return {"lose": 0, "draw": 3, "win": 6}

    @cache
    def hands(self) -> dict:
        return {
            "A": "rock",
            "B": "paper",
            "C": "scissors",
            "X": "rock",
            "Y": "paper",
            "Z": "scissors",
        }

    @cache
    def predict_outcome(self) -> dict:
        return {
            "X": "lose",
            "Y": "draw",
            "Z": "win",
        }

    def play(self, opponent: str, reaction: str) -> str:
        match opponent, reaction:
            case 'rock', 'scissors':
                return "lose"
            case 'rock', 'paper':
                return "win"
            case 'rock', 'rock':
                return 'draw'
            case 'paper', 'rock':
                return "lose"
            case 'paper', 'scissors':
                return "win"
            case 'paper', 'paper':
                return 'draw'
            case 'scissors', 'paper':
                return "lose"
            case 'scissors', 'rock':
                return "win"
            case 'scissors', 'scissors':
                return 'draw'
            case _:
                raise ValueError("Invalid move")

    def points(self, hand: str, outcome: str) -> int:
        return self.points_for_hand().get(hand, 0) + self.points_for_results().get(outcome, 0)

    @approach
    def first_winning_score(self):
        score = 0
        for strategy in self.data:
            opponent, hand = [self.hands().get(move, "invalid") for move in strategy.split()]
            outcome = self.play(opponent=opponent, reaction=hand)
            score += self.points(hand, outcome)
        return score

    @approach
    def second_winning_score(self):
        score = 0
        for strategy in self.data:
            opponent, reaction = strategy.split()
            wished_outcome = self.predict_outcome().get(reaction)
            for hand in ["rock", "paper", "scissors"]:
                outcome = self.play(opponent=self.hands().get(opponent, "invalid"), reaction=hand)
                if wished_outcome == outcome:
                    score += self.points(hand, outcome)
                    break
        return score


RockPaperScissors(day=2).info()
