<p align='center'>
    <img src='https://raw.githubusercontent.com/arnavb/pypokedex/master/assets/logo.png'/>
</p>

[![Travis Build Status](https://travis-ci.org/arnavb/pypokedex.svg?branch=master)](https://travis-ci.com/arnavb/pypokedex)
[![Appveyor Build status](https://ci.appveyor.com/api/projects/status/wpbab6ojfvoe1eg2/branch/master?svg=true)](https://ci.appveyor.com/project/arnavb/pypokedex/branch/master)
[![Codecov](https://img.shields.io/codecov/c/github/arnavb/pypokedex.svg)](https://codecov.io/gh/arnavb/pypokedex)
[![PyPI](https://img.shields.io/pypi/v/pypokedex.svg)](https://pypi.org/project/pypokedex/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypokedex.svg)
[![License](https://img.shields.io/github/license/arnavb/pypokedex.svg)](https://github.com/arnavb/pypokedex/blob/master/LICENSE)

PyPokedex is a minimal pokedex library for Python that uses [PokeAPI](https://pokeapi.co/) internally to get Pokemon data. A simple example:

<p align='center'>
    <img src='https://raw.githubusercontent.com/arnavb/pypokedex/master/assets/example-usage.png'/>
</p>

## Requirements

- Python 3.6+

## Installing

Use:

```bash
$ pip install pypokedex
```

to get the latest stable release, or:

```bash
$ pip install git+https://github.com/arnavb/pypokedex.git@master
```

to get the latest commit on master.

## Documentation

This package (`pypokedex`) only provides one function through the
public API—`get`. It can be used as follows:

```python
import pypokedex

pokemon = pypokedex.get(dex=DEX)  # DEX must be a valid _national_ pokedex
                                  # number
pokemon2 = pypokedex.get(name=NAME)  # NAME must be a valid name of a pokemon
```

In addition to the above function, the following classes are provided as part of the public API:
 
 - `Pokemon` (returned by `get`),
 - `BaseStats`,
 - `Ability`,
 - `Sprites`,
 - and `Move`
 
Note that these classes shouldn't be initialized through client code; their purpose is mainly for type annotations.

### Possible Exceptions

- A `TypeError` will be raised if the wrong number of arguments or the wrong
  type of arguments are passed.
- A `PyPokedexHTTPError` will be raised with an HTTP code of 404 if the Pokemon
  requested is not found. **Note**: The `name` parameter to `get` is _case-insensitive_.
- A `PyPokedexHTTPError` will be raised with the proper HTTP code if another type
  of HTTP error occurs.
- A `PyPokedexError` will be raised if a [requests exception](http://docs.python-requests.org/en/master/_modules/requests/exceptions/)
  occurs (with the exception of `requests.exceptions.HTTPError`, handled in the
  previous two bullet points).
- A `PyPokedexError` will be raised if data is missing when parsing the returned
  JSON from PokeAPI (usually this indicates an API change).

Once a valid `pypokedex.pokemon.Pokemon` object is returned, the following
members are provided for its consumption:

### Member Variables

- `dex` (`int`): Contains the _national_ Pokedex number of the current Pokemon.
- `name` (`str`): Contains the name of the current Pokemon.
- `height` (`int`): Contains the height of the current Pokemon in decimeters (see [veekun/pokedex#249](https://github.com/veekun/pokedex/issues/249)).
- `weight` (`int`): Contains the weight of the current Pokemon in hectograms (see [veekun/pokedex#249](https://github.com/veekun/pokedex/issues/249)).
- `base_experience` (`intt`): Contains the base experience yield of the current Pokemon.
- `types` (`List[str]`): Contains a list of strings with the name of the current
  Pokemon's types.
- `abilities` (`List[Ability]`): Contains a list of named tuples called `Ability`.
  Each `Ability` has the following members:
  - `name` (`str`): The name of the current ability.
  - `is_hidden` (`bool`): Whether the current ability is a hidden ability or not.
- `base_stats` (`BaseStats`): Contains a named tuple with the current
  Pokemon's base stats stored as follows (all `int`s):
  - `hp`: The base HP of the current Pokemon.
  - `atk`: The base attack of the current Pokemon.
  - `def`: The base defense of the current Pokemon.
  - `sp_atk`: The base special attack of the current Pokemon.
  - `sp_def`: The base special defense of the current Pokemon.
  - `speed`: The base speed of the current Pokemon.
- `moves` (`DefaultDict[str, List[Move]]`): Contains a dictionary of game names
  (according to PokeAPI) to a list of named tuples called `Move` representing the
  moves the current Pokemon learns in the respective game. The `Move` named tuple
  contains the following members:
  - `name` (`str`): The name of the current move.
  - `learn_method` (`str`): The method the current Pokemon uses to learn the
    current move (according to PokeAPI).
  - `level` (`int`): The level the current Pokemon learns the current move if
    `learn_method` is `level-up`, `None` otherwise.
- `sprites` (`Sprites`): Contains two dictionaries, `front` and `back` representing the respective
  sprites of the current Pokemon. The keys in the dictionary are [Pokeapi sprite keys](https://pokeapi.co/docs/v2.html#pokemonsprites) without the direction prefix (e.g `back_default` is just `default` in the `back` dictionary).

### Member Functions

- `def exists_in(self, game: str) -> bool`: Method to check whether the current
  Pokemon exists in a specific game.
- `def learns(self, move_name: str, game: str) -> bool`: Method to check
  whether the current Pokemon learns a specific move in a specific game.
- `def __str__(self) -> str`: Method to get a string represenation of the
  current Pokemon. This string is of the form: `Pokemon(dex={self.dex}, name='{self.name}')`.
- `__eq__, __lt__, __gt__, __le__, __ge__`: Methods that implement various
  comparison operators for Pokemon objects in terms of their Pokedex number.

#### Possible Exceptions

- `learns` will raise a `PyPokedexError` if the current Pokemon does not exist
  in the game specified.

## License

This library is licensed under the [MIT License](https://github.com/arnavb/pypokedex/blob/master/LICENSE).

### Dependency Licenses

This library depends on [requests](https://github.com/requests/requests), which is licensed under the [Apache 2.0 License](https://github.com/requests/requests/blob/master/LICENSE).
