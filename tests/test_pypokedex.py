# pylint: disable=redefined-outer-name

from copy import deepcopy

import pytest
import requests

import pypokedex
from pypokedex.pokemon import Ability, BaseStats, Move, Pokemon, Sprites
from pypokedex.exceptions import PyPokedexError, PyPokedexHTTPError

from tests.sample_pokemon import SAMPLE_POKEMON
from tests.fixtures import responses


def _is_properly_initialized_pokemon(pokemon: Pokemon):
    return (
        pokemon.dex == 999
        and pokemon.name == "sample"
        and pokemon.height == 200.2
        and pokemon.weight == 201.2
        and pokemon.base_experience == 200
        and pokemon.types == ["type_1", "type_2"]
        and pokemon.abilities
        == [Ability("ability_1", True), Ability("ability_2", False)]
        and pokemon.base_stats
        == BaseStats(hp=1, attack=2, defense=3, sp_atk=4, sp_def=5, speed=6)
        and pokemon.moves
        == {
            "game_1": [Move("move_1", "tutor", None)],
            "game_2": [Move("move_1", "level-up", 5)],
        }
        and pokemon.sprites
        == Sprites(
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
        json=SAMPLE_POKEMON,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    assert _is_properly_initialized_pokemon(pokemon)


def test_get_pokemon_by_dex(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/999",
        json=SAMPLE_POKEMON,
        status=200,
    )

    pokemon = pypokedex.get(dex=999)

    assert _is_properly_initialized_pokemon(pokemon)


def test_pokemon_existence_in_games(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=SAMPLE_POKEMON,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    assert pokemon.exists_in("game_1")


def test_pokemon_non_existence_in_games(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=SAMPLE_POKEMON,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    assert not pokemon.exists_in("some random string")


def test_pokemon_learns_move(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=SAMPLE_POKEMON,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    assert pokemon.learns("move_1", "game_1")
    assert pokemon.learns("move_1", "game_2")


def test_pokemon_does_not_learn_move(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=SAMPLE_POKEMON,
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
        json=SAMPLE_POKEMON,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")

    with pytest.raises(PyPokedexError):
        pokemon.learns("random move", "random game")


def test_pokemon_str_function(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=SAMPLE_POKEMON,
        status=200,
    )

    pokemon = pypokedex.get(name="sample")
    assert str(pokemon) == "Pokemon(dex=999, name='sample')"


def test_pokemon_equality(responses):
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=SAMPLE_POKEMON,
        status=200,
    )
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/999",
        json=SAMPLE_POKEMON,
        status=200,
    )

    first_pokemon = pypokedex.get(name="sample")
    second_pokemon = pypokedex.get(dex=999)
    assert first_pokemon == second_pokemon


def test_pokemon_inequality(responses):
    cloned_sample_pokemon = deepcopy(SAMPLE_POKEMON)
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
        json=SAMPLE_POKEMON,
        status=200,
    )

    first_pokemon = pypokedex.get(dex=998)
    second_pokemon = pypokedex.get(dex=999)
    assert first_pokemon != second_pokemon


def test_pokemon_less_than(responses):
    cloned_sample_pokemon = deepcopy(SAMPLE_POKEMON)
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
        json=SAMPLE_POKEMON,
        status=200,
    )

    first_pokemon = pypokedex.get(dex=998)
    second_pokemon = pypokedex.get(dex=999)
    assert first_pokemon < second_pokemon
    assert not first_pokemon == second_pokemon
    assert not first_pokemon > second_pokemon


def test_pokemon_greater_than(responses):
    cloned_sample_pokemon = deepcopy(SAMPLE_POKEMON)
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
        json=SAMPLE_POKEMON,
        status=200,
    )

    first_pokemon = pypokedex.get(dex=998)
    second_pokemon = pypokedex.get(dex=999)
    assert second_pokemon > first_pokemon
    assert not second_pokemon == first_pokemon
    assert not second_pokemon < first_pokemon


def test_pokemon_less_than_or_equal_to(responses):
    cloned_sample_pokemon = deepcopy(SAMPLE_POKEMON)
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
        json=SAMPLE_POKEMON,
        status=200,
    )

    first_pokemon = pypokedex.get(dex=998)
    second_pokemon = pypokedex.get(dex=999)
    third_pokemon = pypokedex.get(dex=999)
    assert first_pokemon <= second_pokemon
    assert second_pokemon <= third_pokemon
    assert not third_pokemon <= first_pokemon


def test_pokemon_greater_than_or_equal_to(responses):
    cloned_sample_pokemon = deepcopy(SAMPLE_POKEMON)
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
        json=SAMPLE_POKEMON,
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
    cloned_sample_pokemon = deepcopy(SAMPLE_POKEMON)
    del cloned_sample_pokemon["weight"]
    responses.add(
        responses.GET,
        "https://pokeapi.co/api/v2/pokemon/sample",
        json=cloned_sample_pokemon,
        status=200,
    )

    with pytest.raises(PyPokedexError):
        pypokedex.get(name="sample")
