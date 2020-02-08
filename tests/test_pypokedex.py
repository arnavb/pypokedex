# pylint: disable=redefined-outer-name

from copy import deepcopy

import pytest
import responses as rsps  # So it can be later redefined as a function
import requests

import pypokedex
from pypokedex.exceptions import PyPokedexError, PyPokedexHTTPError

# Sample pokemon with only essential data included
sample_pokemon = {
    "id": 999,
    "name": "sample",
    "height": 200.2,
    "weight": 201.2,
    "base_experience": 200,
    "types": [{"type": {"name": "type_1"}}, {"type": {"name": "type_2"}}],
    "stats": [
        {"base_stat": 1, "stat": {"name": "hp"}},
        {"base_stat": 2, "stat": {"name": "attack"}},
        {"base_stat": 3, "stat": {"name": "defense"}},
        {"base_stat": 4, "stat": {"name": "special-attack"}},
        {"base_stat": 5, "stat": {"name": "special-defense"}},
        {"base_stat": 6, "stat": {"name": "speed"}},
    ],
    "abilities": [
        {"ability": {"name": "ability_1"}, "is_hidden": True},
        {"ability": {"name": "ability_2"}, "is_hidden": False},
    ],
    "moves": [
        {
            "move": {"name": "move_1"},
            "version_group_details": [
                {
                    "level_learned_at": 0,
                    "move_learn_method": {"name": "tutor"},
                    "version_group": {"name": "game_1"},
                },
                {
                    "level_learned_at": 5,
                    "move_learn_method": {"name": "level-up"},
                    "version_group": {"name": "game_2"},
                },
            ],
        }
    ],
    "sprites": {
        "back_default": "default_back_url",
        "back_female": None,
        "back_shiny": "shiny_back_url",
        "back_shiny_female": None,
        "front_default": "default_front_url",
        "front_female": None,
        "front_shiny": "front_shiny_url",
        "front_shiny_female": None,
    },
}


def _is_properly_initialized_pokemon_object(pokemon: pypokedex.pokemon.Pokemon):
    return (
        pokemon.dex == 999
        and pokemon.name == "sample"
        and pokemon.height == 200.2
        and pokemon.weight == 201.2
        and pokemon.base_experience == 200
        and pokemon.types == ["type_1", "type_2"]
        and pokemon.abilities[0] == pypokedex.pokemon.Ability("ability_1", True)
        and pokemon.abilities[1]  # noqa
        == pypokedex.pokemon.Ability("ability_2", False)
        and pokemon.base_stats.hp == 1  # noqa
        and pokemon.base_stats.attack == 2
        and pokemon.base_stats.defense == 3
        and pokemon.base_stats.sp_atk == 4
        and pokemon.base_stats.sp_def == 5
        and pokemon.base_stats.speed == 6
        and pokemon.moves["game_1"][0]
        == pypokedex.pokemon.Move("move_1", "tutor", None)
        and pokemon.moves["game_2"][0]  # noqa
        == pypokedex.pokemon.Move("move_1", "level-up", 5)
        and pokemon.sprites
        == pypokedex.pokemon.Sprites(
            front={
                "default": "default_front_url",
                "female": None,
                "shiny": "front_shiny_url",
                "shiny_female": None,
            },
            back={
                "default": "default_back_url",
                "female": None,
                "shiny": "shiny_back_url",
                "shiny_female": None,
            },
        )
    )  # noqa


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
        pypokedex.get(a=2, b="many", dex="arguments")


def test_incorrect_get_argument_types():
    with pytest.raises(TypeError):
        pypokedex.get(dex="A STRING")

    with pytest.raises(TypeError):
        pypokedex.get(name=111)


def test_get_pokemon_by_name(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=sample_pokemon,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    assert _is_properly_initialized_pokemon_object(pokemon)


def test_get_pokemon_by_dex(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/999",
        json=sample_pokemon,
        status=200,
    )

    pokemon = pypokedex.get(dex=999)

    assert _is_properly_initialized_pokemon_object(pokemon)


def test_pokemon_existence_in_games(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=sample_pokemon,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    assert pokemon.exists_in("game_1")


def test_pokemon_non_existence_in_games(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=sample_pokemon,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    assert not pokemon.exists_in("some random string")


def test_pokemon_learns_move(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=sample_pokemon,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    assert pokemon.learns("move_1", "game_1")
    assert pokemon.learns("move_1", "game_2")


def test_pokemon_does_not_learn_move(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=sample_pokemon,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    assert not pokemon.learns("random move", "game_1")


def test_pokemon_does_not_learn_move_because_it_is_not_in_the_specified_game(
    responses
):  # noqa
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=sample_pokemon,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    with pytest.raises(PyPokedexError):
        pokemon.learns("random move", "random game")


def test_pokemon_str_function(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=sample_pokemon,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")
    assert str(pokemon) == "Pokemon(dex=999, name='sample')"


def test_pokemon_equality(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=sample_pokemon,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/999",
        json=sample_pokemon,
        status=200,
    )

    first_pokemon = pypokedex.get(name="sample")
    second_pokemon = pypokedex.get(dex=999)
    assert first_pokemon == second_pokemon


def test_pokemon_inequality(responses):
    cloned_sample_pokemon = deepcopy(sample_pokemon)
    cloned_sample_pokemon["id"] = 998
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/998",
        json=cloned_sample_pokemon,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/999",
        json=sample_pokemon,
        status=200,
    )

    first_pokemon = pypokedex.get(dex=998)
    second_pokemon = pypokedex.get(dex=999)
    assert first_pokemon != second_pokemon


def test_pokemon_less_than(responses):
    cloned_sample_pokemon = deepcopy(sample_pokemon)
    cloned_sample_pokemon["id"] = 998
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/998",
        json=cloned_sample_pokemon,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/999",
        json=sample_pokemon,
        status=200,
    )

    first_pokemon = pypokedex.get(dex=998)
    second_pokemon = pypokedex.get(dex=999)
    assert first_pokemon < second_pokemon
    assert not first_pokemon == second_pokemon
    assert not first_pokemon > second_pokemon


def test_pokemon_greater_than(responses):
    cloned_sample_pokemon = deepcopy(sample_pokemon)
    cloned_sample_pokemon["id"] = 998
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/998",
        json=cloned_sample_pokemon,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/999",
        json=sample_pokemon,
        status=200,
    )

    first_pokemon = pypokedex.get(dex=998)
    second_pokemon = pypokedex.get(dex=999)
    assert second_pokemon > first_pokemon
    assert not second_pokemon == first_pokemon
    assert not second_pokemon < first_pokemon


def test_pokemon_less_than_or_equal_to(responses):
    cloned_sample_pokemon = deepcopy(sample_pokemon)
    cloned_sample_pokemon["id"] = 998
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/998",
        json=cloned_sample_pokemon,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/999",
        json=sample_pokemon,
        status=200,
    )

    first_pokemon = pypokedex.get(dex=998)
    second_pokemon = pypokedex.get(dex=999)
    third_pokemon = pypokedex.get(dex=999)
    assert first_pokemon <= second_pokemon
    assert second_pokemon <= third_pokemon
    assert not third_pokemon <= first_pokemon


def test_pokemon_greater_than_or_equal_to(responses):
    cloned_sample_pokemon = deepcopy(sample_pokemon)
    cloned_sample_pokemon["id"] = 998
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/998",
        json=cloned_sample_pokemon,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/999",
        json=sample_pokemon,
        status=200,
    )

    first_pokemon = pypokedex.get(dex=998)
    second_pokemon = pypokedex.get(dex=999)
    third_pokemon = pypokedex.get(dex=999)
    assert second_pokemon >= first_pokemon
    assert third_pokemon >= second_pokemon
    assert not first_pokemon >= third_pokemon


def test_404_pokemon_not_found(responses):
    responses.add(
        responses.GET, "https://pokeapi.co/api/v2/pokemon/sample", json={}, status=404
    )

    with pytest.raises(PyPokedexHTTPError) as not_found:
        pypokedex.get(name="sample")

    assert not_found.value.http_code == 404


def test_other_HTTP_errors(responses):
    responses.add(
        responses.GET, "https://pokeapi.co/api/v2/pokemon/sample", json={}, status=408
    )

    with pytest.raises(PyPokedexHTTPError) as other_http_error:
        pypokedex.get(name="sample")

    assert other_http_error.value.http_code == 408


def test_requests_errors(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        body=requests.exceptions.RequestException("Some error"),
    )

    with pytest.raises(PyPokedexError):
        pypokedex.get(name="sample")


def test_missing_data_keys_for_pokemon(responses):
    cloned_sample_pokemon = deepcopy(sample_pokemon)
    del cloned_sample_pokemon["weight"]
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=cloned_sample_pokemon,
        status=200,
    )

    with pytest.raises(PyPokedexError):
        pypokedex.get(name="sample")


# --------------------------------------------------
# End tests
# --------------------------------------------------
