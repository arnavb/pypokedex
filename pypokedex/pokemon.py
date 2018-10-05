from collections import defaultdict

from typing import DefaultDict, List, NamedTuple

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
    level: int


class Pokemon:
    def __init__(self, json_data) -> None:
        # Load pokemon data
        try:
            self.dex = json_data['id']

            for pokemon_info in ['name', 'height', 'weight']:
                setattr(self, pokemon_info, json_data[pokemon_info])

            stat_dict = {}

            for stat in json_data['stats']:
                stat_value = stat['base_stat']
                stat_name = stat['stat']['name']

                if stat_name in ['hp', 'attack', 'defense', 'speed']:
                    stat_dict[stat_name] = stat_value
                elif stat_name == 'special-attack':
                    stat_dict['sp_atk'] = stat_value
                elif stat_name == 'special-defense':  # pragma: no branch
                    stat_dict['sp_def'] = stat_value

            self.base_stats = BaseStats(**stat_dict)

            self.abilities = [Ability(ability['ability']['name'],
                                      ability['is_hidden'])
                              for ability in json_data['abilities']]

            self.types = [type_['type']['name']
                          for type_ in json_data['types']]

            self.moves: DefaultDict[str, List[Move]] = defaultdict(list)

            for move in json_data['moves']:
                move_name = move['move']['name']

                for game_details in move['version_group_details']:
                    learn_level = game_details['level_learned_at']
                    learn_method = game_details['move_learn_method']['name']
                    game_name = game_details['version_group']['name']
                    if learn_level == 0:  # Move not learned by level-up
                        learn_level = None

                    self.moves[game_name].append(Move(move_name, learn_method,
                                                      learn_level))

        except KeyError as error:
            raise PyPokedexError('A required piece of data was not found for'
                                 'the current Pokemon!') from error

    def exists(self, game: str) -> bool:
        return game in self.moves

    def learns(self, move_name: str, game: str) -> bool:
        if not self.exists(game):
            raise PyPokedexError(f'{self.name} is not '  # type: ignore
                                 f'obtainable in {game}!')

        for move in self.moves[game]:
            if move.name == move_name:
                return True
        return False
    
    def __eq__(self, other: Pokemon) -> bool:
        return self.dex == other.dex

    def __lt__(self, other: Pokemon) -> bool:
        return self.dex < other.dex

    def __gt__(self, other: Pokemon) -> bool:
        return self.dex > other.dex

    def __le__(self, other: Pokemon) -> bool:
        return self.dex <= other.dex

    def __ge__(self, other: Pokemon) -> bool:
        return self.dex >= other.dex
