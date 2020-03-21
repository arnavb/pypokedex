from functools import lru_cache
from typing import Union

import requests

from pypokedex.exceptions import PyPokedexError, PyPokedexHTTPError
from pypokedex.pokemon import Pokemon

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon"


@lru_cache(maxsize=None)
def get(**kwargs) -> Pokemon:
    """Get a Pokemon object based on exactly ONE of the criteria specified
    in the keyword argument ``kwargs``

    :key name: The name of the Pokemon
    :type name: str:

    :key dex: The national Pokedex number of the Pokemon
    :type name: int:

    :raises TypeError: if exactly one argument isn't passed, ``dex`` or ``name``
        are of the wrong types, or if they aren't prresent
    :raises PyPokedexHTTPError: if an non-success HTTP status code is returned
        from PokeAPI while retrieving Pokemon data
    :raises PyPokedexError: if an unexpected HTTP error occurs while retrieving
        Pokemon data

    :return: An instance of a :class:`Pokemon` fitting the passed criteria
        if no errors occurred
    """

    if len(kwargs) != 1:
        raise TypeError("pypokedex.get() expects expects only 1 argument!")

    subpage: Union[int, str]

    if "dex" in kwargs and isinstance(kwargs["dex"], int):
        subpage = kwargs["dex"]
    elif "name" in kwargs and isinstance(kwargs["name"], str):
        subpage = kwargs["name"].lower()
    else:
        raise TypeError("Arguments were either of an incorrect type or value!")

    try:
        response = requests.get(f"{POKEAPI_BASE_URL}/{subpage}", timeout=3)
        response.raise_for_status()

    except requests.exceptions.HTTPError as error:
        if response.status_code == 404:
            raise PyPokedexHTTPError(
                f"The requested pokemon was not found!", 404
            ) from error
        raise PyPokedexHTTPError(
            f"An HTTP error occurred! (Status code: {response.status_code})",
            response.status_code,
        ) from error

    except requests.exceptions.RequestException as error:
        raise PyPokedexError("An internal requests exception occurred!") from error

    return Pokemon(response.json())
