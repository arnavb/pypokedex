from copy import deepcopy

import pytest
import responses as rsps  # So it can be later redefined as a function
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


def _is_valid_sample_pokemon(pokemon: pypokedex.pokemon.Pokemon):
    return (pokemon.dex == 999 and
            pokemon.name == 'sample' and
            pokemon.height == 200.2 and
            pokemon.weight == 201.2 and
            pokemon.types == ('type_1', 'type_2') and
            pokemon.abilities[0] == pypokedex.pokemon.Ability('ability_1', True) and  # noqa
            pokemon.abilities[1] == pypokedex.pokemon.Ability('ability_2', False) and  # noqa
            pokemon.base_stats.hp == 1 and
            pokemon.base_stats.attack == 2 and
            pokemon.base_stats.defense == 3 and
            pokemon.base_stats.sp_atk == 4 and
            pokemon.base_stats.sp_def == 5 and
            pokemon.base_stats.speed == 6 and
            pokemon.moves['move_1']['game_1'] == pypokedex.pokemon.Move('tutor', None) and  # noqa
            pokemon.moves['move_1']['game_2'] == pypokedex.pokemon.Move('level-up', 5))  # noqa


def setup_function():
    pypokedex.get.cache_clear()


@pytest.fixture
def responses():
    pypokedex.get.cache_clear()
    with rsps.RequestsMock() as requests_mock:
        yield requests_mock

# --------------------------------------------------
# Begin tests
# --------------------------------------------------


def test_too_few_get_arguments():
    with pytest.raises(TypeError):
        pypokedex.get()


def test_too_many_get_arguments():
    with pytest.raises(TypeError):
        pypokedex.get(a=2, b='many', dex='arguments')


def test_incorrect_get_argument_types():
    with pytest.raises(TypeError):
        pypokedex.get(dex='A STRING')

    with pytest.raises(TypeError):
        pypokedex.get(name=111)


def test_get_sample_pokemon_by_name(responses):
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  json=sample_pokemon, status=200)

    pokemon = pypokedex.get(name='sample')

    assert _is_valid_sample_pokemon(pokemon)


def test_get_sample_pokemon_by_dex(responses):
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/999',
                  json=sample_pokemon, status=200)

    pokemon = pypokedex.get(dex=999)

    assert _is_valid_sample_pokemon(pokemon)


def test_404_pokemon_not_found(responses):
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  json={}, status=404)

    with pytest.raises(PyPokedexHTTPError) as not_found:
        pypokedex.get(name='sample')

    assert not_found.value.http_code == 404


def test_other_HTTP_errors(responses):
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  json={}, status=408)

    with pytest.raises(PyPokedexHTTPError) as other_http_error:
        pypokedex.get(name='sample')

    assert other_http_error.value.http_code == 408


def test_requests_errors(responses):
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  body=requests.exceptions.RequestException('Some error'))

    with pytest.raises(PyPokedexError):
        pypokedex.get(name='sample')


def test_missing_data_keys_for_pokemon(responses):
    cloned_sample_pokemon = deepcopy(sample_pokemon)
    del cloned_sample_pokemon['weight']
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  json=cloned_sample_pokemon, status=200)

    with pytest.raises(PyPokedexError):
        pypokedex.get(name='sample')


def test_pokemon_immutability(responses):
    responses.add(responses.GET, 'https://pokeapi.co/api/v2/pokemon/sample',
                  json=sample_pokemon, status=200)

    pokemon = pypokedex.get(name='sample')

    for attribute in ['name', 'height', 'weight', 'moves', 'base_stats',
                      'abilities', 'types', 'moves']:
        with pytest.raises(TypeError):
            setattr(pokemon, attribute, None)
    # TODO: Figure out to prevent in-place modification of mutable values
    # like dicts.

# --------------------------------------------------
# End tests
# --------------------------------------------------
