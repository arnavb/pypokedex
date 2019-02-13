from functools import lru_cache

import requests

from pypokedex.exceptions import PyPokedexError, PyPokedexHTTPError
from pypokedex.pokemon import Pokemon

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon"


@lru_cache(maxsize=None)
def get(**kwargs) -> Pokemon:
    if len(kwargs) != 1:
        raise TypeError("pypokedex.get() expects expects only 1 argument!")

    if "dex" in kwargs and isinstance(kwargs["dex"], int):
        subpage = kwargs["dex"]
    elif "name" in kwargs and isinstance(kwargs["name"], str):
        subpage = kwargs["name"].lower()  # type: ignore
    else:
        raise TypeError("Arguments were either of an incorrect type or value!")

    try:
        response = requests.get(f"{POKEAPI_BASE_URL}/{subpage}", timeout=3)
        response.raise_for_status()

    except requests.exceptions.HTTPError as error:
        if response.status_code == 404:
            raise PyPokedexHTTPError(
                "The requested pokemon was not " "found!", 404
            ) from error
        raise PyPokedexHTTPError(
            "An HTTP error occurred! " "(Status code: {response.status_code})",
            response.status_code,
        ) from error

    except requests.exceptions.RequestException as error:
        raise PyPokedexError("An internal requests exception " "occurred!") from error

    return Pokemon(response.json())
