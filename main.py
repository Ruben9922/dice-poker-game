import random
from collections import Counter
from typing import List, Callable

import console_utilities as cu


class Category:
    def __init__(self, name: str, condition: Callable[[List[int]], bool], raw_score: Callable[[List[int]], int]):
        self.name = name
        self.__condition = condition
        self.__raw_score = raw_score

    def score(self, dice: List[int]) -> int:
        return self.__raw_score(dice) if self.__condition(dice) else 0


class Player:
    def __init__(self, name: str, score: int, categories: List[Category]):
        self.name = name
        self.score = score
        self.categories = categories


def input_player_names() -> List[str]:
    player_names = []
    finished = False
    while not finished:
        valid = False
        while not valid:
            new_player_name = input(f"Player {len(player_names) + 1}'s name (leave blank for \"Player {len(player_names) + 1}\"): ")
            new_player_name = new_player_name.strip()

            if not new_player_name:
                new_player_name = f"Player {len(player_names) + 1}"

            valid = new_player_name not in player_names
            if valid:
                player_names.append(new_player_name)
                print(f"Player \"{new_player_name}\" added.")
                print()
            else:
                print("Player name already exists. Please enter a different name.")

        finished = not cu.input_boolean("Add another player?", True)

    print("Players: ", end="")
    print(*player_names, sep=", ")
    print()

    return player_names


def create_players(player_names: List[str], categories: List[Category]) -> List[Player]:
    return list(map(lambda player_name: Player(name=player_name, score=0, categories=categories.copy()), player_names))


def play(players: List[Player]) -> None:
    while any(player.categories for player in players):
        current_player = players[0]
        print(f"{current_player.name}'s turn")
        print()

        # todo: maybe merge this into loop below
        print("Roll #1")
        dice = random.sample(range(1, 7), 5)
        print(dice)
        print()

        print("Categories:")
        print(*(category_to_string(category, dice) for category in current_player.categories), sep="\n")
        print()

        max_additional_roll_count = 2
        i = 0
        roll_again = True
        while roll_again:
            if i < max_additional_roll_count:
                roll_again = cu.input_boolean("Roll again?", )
            else:
                roll_again = False
                print(f"No more rolls allowed (max {max_additional_roll_count + 1} per turn).")
                print()

            if roll_again:
                # Select dice to re-roll
                print("Select dice to re-roll")
                selected_dice_indices = cu.input_multiple_option_int(dice, allow_empty=False)
                print()

                # Re-roll selected dice
                for selected_dice_index in selected_dice_indices:
                    dice[selected_dice_index] = random.randint(1, 6)

                print(f"Roll #{i + 2}")
                print(dice)
                print()

                print("Categories:")
                print(*(category_to_string(category, dice) for category in current_player.categories), sep="\n")
                print()

            i += 1

        # Select category
        print("Select category")
        selected_category_index = cu.input_option_int(
            [category_to_string(category, dice) for category in current_player.categories],
        )
        selected_category = current_player.categories.pop(selected_category_index)
        current_player.score += selected_category.score(dice)
        print()

        print(f"{current_player.name}'s score: {current_player.score} (+{selected_category.score(dice)})")
        print()

    players_sorted_by_score = sorted(players, key=lambda player: player.score)
    print("Scores:")
    for player in players_sorted_by_score:
        print(f"{player.name} (score: {player.score})")
    winning_player = players_sorted_by_score[0]
    print(f"{winning_player.name} is the winner!")


def category_to_string(category: Category, dice: List[int]) -> str:
    return f"{category.name} (score: {category.score(dice)})"


def is_full_house(dice: List[int]) -> bool:
    counter = Counter(dice)
    return len(counter) == 1 or (len(counter) == 2 and 2 in counter.values() and 3 in counter.values())


def is_n_of_a_kind(dice: List[int], n: int) -> bool:
    return any(count >= n for count in Counter(dice).values())


def is_straight(dice: List[int], straight_length: int) -> bool:
    return any(set(range(i + 1, straight_length + i + 1)).issubset(dice) for i in range(6 - straight_length + 1))


def calculate_score_for_single_value(dice: List[int], value: int) -> int:
    return len(list(filter(lambda die: die == value, dice))) * value


def main() -> None:
    categories = [
        Category(
            name="Ones",
            condition=lambda _: True,
            raw_score=lambda dice: calculate_score_for_single_value(dice, 1),
        ),
        Category(
            name="Twos",
            condition=lambda _: True,
            raw_score=lambda dice: calculate_score_for_single_value(dice, 2),
        ),
        Category(
            name="Threes",
            condition=lambda _: True,
            raw_score=lambda dice: calculate_score_for_single_value(dice, 3),
        ),
        Category(
            name="Fours",
            condition=lambda _: True,
            raw_score=lambda dice: calculate_score_for_single_value(dice, 4),
        ),
        Category(
            name="Fives",
            condition=lambda _: True,
            raw_score=lambda dice: calculate_score_for_single_value(dice, 5),
        ),
        Category(
            name="Sixes",
            condition=lambda _: True,
            raw_score=lambda dice: calculate_score_for_single_value(dice, 6),
        ),
        Category(
            name="Three of a Kind",
            condition=lambda dice: is_n_of_a_kind(dice, 3),
            raw_score=lambda dice: sum(dice),
        ),
        Category(
            name="Four of a Kind",
            condition=lambda dice: is_n_of_a_kind(dice, 4),
            raw_score=lambda dice: sum(dice),
        ),
        Category(
            name="Full House",
            condition=is_full_house,
            raw_score=lambda _: 25,
        ),
        Category(
            name="Small Straight",
            condition=lambda dice: is_straight(dice, 4),
            raw_score=lambda _: 30,
        ),
        Category(
            name="Large Straight",
            condition=lambda dice: is_straight(dice, 5),
            raw_score=lambda _: 40,
        ),
        Category(
            name="!",
            condition=lambda dice: len(set(dice)) == 1,
            raw_score=lambda _: 50,
        ),
        Category(
            name="Chance",
            condition=lambda _: True,
            raw_score=lambda dice: sum(dice),
        ),
    ]

    player_names = input_player_names()
    players = create_players(player_names, categories)
    play(players)


if __name__ == '__main__':
    main()
