from typing import Dict, List, NamedTuple

from pypokedex.exceptions import PyPokedexError

class PokemonBaseStats(NamedTuple):
    HP: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int

class Pokemon:
    def __init__(self, json_data):
        # Load pokemon data
        try:
            self.dex = json_data['id']

            for pokemon_info in ['name', 'weight', 'height']:
                setattr(self, pokemon_info, json_data[pokemon_info])
            
            self.abilities = tuple((ability['ability']['name'],
                                     ability['is_hidden'])
                                    for ability in json_data['abilities'])

            self.types = tuple(type_['type']['name']
                               for type_ in json_data['types'])

            # TODO: Add base stats and moves by game            

        except KeyError as error:
            raise PyPokedexError('A required piece of data was not found for'
                                 'the current Pokemon!') from error
    
    def get_moves_for_game(name: str):
        # TODO: Return moves for pokemon by name of game
        pass
    
    # Method to make all attributes const
    def __setattr__(self, name: str, value: str):
        if hasattr(self, name):
            raise TypeError('Constant attributes may not be modified!')

        self.__dict__[name] = value
