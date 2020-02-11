from collections import defaultdict
from typing import DefaultDict, List, NamedTuple, Dict, Optional

from pypokedex.exceptions import PyPokedexError


class Ability(NamedTuple):
    name: str
    is_hidden: bool


class BaseStats(NamedTuple):
    hp: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int


class Move(NamedTuple):
    name: str
    learn_method: str
    level: Optional[int]


class Sprites(NamedTuple):
    front: Dict[str, Optional[str]]
    back: Dict[str, Optional[str]]


class Pokemon:
    dex: int
    name: str
    height: int
    weight: int
    base_experience: int
    base_stats: BaseStats
    abilities: List[Ability]
    types: List[str]
    moves: DefaultDict[str, List[Move]]
    sprites: Sprites

    def __init__(self, json_data) -> None:
        """Loads and stores required pokemon data"""

        # pylint: disable=too-many-locals
        try:
            self.dex = json_data["id"]

            for pokemon_info in ["name", "height", "weight", "base_experience"]:
                setattr(self, pokemon_info, json_data[pokemon_info])

            stat_dict = {}

            for stat in json_data["stats"]:
                stat_value = stat["base_stat"]
                stat_name = stat["stat"]["name"]

                if stat_name in ["hp", "attack", "defense", "speed"]:
                    stat_dict[stat_name] = stat_value
                elif stat_name == "special-attack":
                    stat_dict["sp_atk"] = stat_value
                elif stat_name == "special-defense":  # pragma: no branch
                    stat_dict["sp_def"] = stat_value

            self.base_stats = BaseStats(**stat_dict)

            self.abilities = [
                Ability(ability["ability"]["name"], ability["is_hidden"])
                for ability in json_data["abilities"]
            ]

            self.types = [type_["type"]["name"] for type_ in json_data["types"]]

            self.moves = defaultdict(list)

            for move in json_data["moves"]:
                move_name = move["move"]["name"]

                for game_details in move["version_group_details"]:
                    learn_level = game_details["level_learned_at"]
                    learn_method = game_details["move_learn_method"]["name"]
                    game_name = game_details["version_group"]["name"]
                    if learn_level == 0:  # Move not learned by level-up
                        learn_level = None

                    self.moves[game_name].append(
                        Move(move_name, learn_method, learn_level)
                    )

            self.sprites = Sprites(front={}, back={})
            for sprite, url in json_data["sprites"].items():
                sprite_direction, sprite_type = sprite.split("_", 1)

                if sprite_direction == "front":
                    self.sprites.front[sprite_type] = url
                else:
                    self.sprites.back[sprite_type] = url

        except KeyError as error:
            raise PyPokedexError(
                "A required piece of data was not found for the current Pokemon!"
            ) from error

    def exists_in(self, game: str) -> bool:
        """Checks whether the current Pokemon exists in the specified game."""
        return game in self.moves

    def learns(self, move_name: str, game: str) -> bool:
        """Checks whether the current Pokemon learn the specified move
        in the specified game."""
        if not self.exists_in(game):
            raise PyPokedexError(f"{self.name} is not obtainable in {game}!")

        for move in self.moves[game]:
            if move.name == move_name:
                return True

        return False

    def __str__(self) -> str:
        """Returns a human-readable representation of the current Pokemon."""
        return f"Pokemon(dex={self.dex}, name='{self.name}')"

    def __eq__(self, other) -> bool:
        return self.dex == other.dex

    def __lt__(self, other) -> bool:
        return self.dex < other.dex

    def __gt__(self, other) -> bool:
        return self.dex > other.dex

    def __le__(self, other) -> bool:
        return self.dex <= other.dex

    def __ge__(self, other) -> bool:
        return self.dex >= other.dex
