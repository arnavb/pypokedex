from copy import deepcopy

import pytest
import responses
import requests

import pypokedex
from pypokedex.exceptions import PyPokedexError, PyPokedexHTTPError

# Sample pokemon with only essential data included
sample_pokemon = {
    'id': 999,
    'name': 'sample',
    'height': 200.2,
    'weight': 201.2,
    'types': [
        {
            'type': {
                'name': 'type_1'
            }
        },
        {
            'type': {
                'name': 'type_2'
            }
        }
    ],
    
    'stats': [
        {
            'base_stat': 1,
            'stat': {
                'name': 'hp'
            }
        },
        {
            'base_stat': 2,
            'stat': {
                'name': 'attack'
            }
        },
        {
            'base_stat': 3,
            'stat': {
                'name': 'defense'
            }
        },
        {
            'base_stat': 4,
            'stat': {
                'name': 'special-attack'
            }
        },
        {
            'base_stat': 5,
            'stat': {
                'name': 'special-defense'
            }
        },
        {
            'base_stat': 6,
            'stat': {
                'name': 'speed'
            }
        }
    ],
    
    'abilities': [
        {
            'ability': {
                'name': 'ability_1'
            },
            'is_hidden': True
        },
        {
            'ability': {
                'name': 'ability_2'
            },
            'is_hidden': False
        }
    ],
    
    'moves': [
        {
            'move': {
                'name': 'move_1'
            },
            'version_group_details': [
                {
                    'level_learned_at': 0,
                    'move_learn_method': {
                        'name': 'tutor'
                    },
                    'version_group': {
                        'name': 'game_1'
                    }
                },
                {
                    'level_learned_at': 5,
                    'move_learn_method': {
                        'name': 'level-up'
                    },
                    'version_group': {
                        'name': 'game_2'
                    }
                }
            ]
        }
    ]
}

def test_wrong_number_of_arguments():
    with pytest.raises(TypeError):
         pypokedex.get()

    with pytest.raises(TypeError):
        pypokedex.get(a=2, b='many', dex='arguments')

def test_incorrect_argument_types():
    with pytest.raises(TypeError):
        pypokedex.get(dex='A STRING')
    
    with pytest.raises(TypeError):
        pypokedex.get(name=111)

def _is_valid_sample_pokemon(pokemon: pypokedex.Pokemon):
    return pokemon.dex == 999 and \
        pokemon.name == 'sample' and \
        pokemon.height == 200.2 and \
        pokemon.weight == 201.2 and \
        pokemon.types == ('type_1', 'type_2') and \
        pokemon.abilities == (('ability_1', True), ('ability_2', False)) and \
        pokemon.base_stats.hp == 1 and \
        pokemon.base_stats.attack == 2 and \
        pokemon.base_stats.defense == 3 and \
        pokemon.base_stats.sp_atk == 4 and \
        pokemon.base_stats.sp_def == 5 and \
        pokemon.base_stats.speed == 6 and \
        pokemon.moves[0] == ('move_1', (('game_1', 'tutor'),
                                        ('game_2', 'level-up', 5)))

@responses.activate
def test_get_sample_pokemon():
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  json=sample_pokemon, status=200)
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/999',
                  json=sample_pokemon, status=200)
    
    pypokedex.get.cache_clear()
    
    pokemon = pypokedex.get(name='sample')
    
    assert _is_valid_sample_pokemon(pokemon)
    
    pypokedex.get.cache_clear()
    
    pokemon = pypokedex.get(dex=999)
    
    assert _is_valid_sample_pokemon(pokemon)

@responses.activate
def test_invalid_http_status():
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  json={}, status=404)
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  json={}, status=408)
    
    pypokedex.get.cache_clear()
    
    with pytest.raises(PyPokedexHTTPError) as not_found:
        pypokedex.get(name='sample')
    
    assert 'not found' in str(not_found.value)
    assert not_found.value.http_code == 404
    
    pypokedex.get.cache_clear()
    
    with pytest.raises(PyPokedexHTTPError) as other_http_error:
        pypokedex.get(name='sample')

    assert other_http_error.value.http_code == 408

@responses.activate
def test_other_errors():
    cloned_sample_pokemon = deepcopy(sample_pokemon)
    del cloned_sample_pokemon['weight']
    
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  body=requests.exceptions.RequestException('Some error'))
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  json=cloned_sample_pokemon, status=200)
    
    pypokedex.get.cache_clear()
    
    with pytest.raises(PyPokedexError) as requests_error:
        pokemon = pypokedex.get(name='sample')
        print(pokemon.types)
    
    assert 'requests' in str(requests_error.value)
    
    pypokedex.get.cache_clear()
    
    with pytest.raises(PyPokedexError) as data_not_found:
        pypokedex.get(name='sample')
    
    assert 'data was not found' in str(data_not_found.value)
