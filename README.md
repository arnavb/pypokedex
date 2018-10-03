<p align='center'>
    <img src='https://raw.githubusercontent.com/arnavb/pypokedex/master/assets/logo.png'/>
</p>

[![Travis Build Status](https://travis-ci.org/arnavb/pypokedex.svg?branch=master)](https://travis-ci.org/arnavb/pypokedex)
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

### The Basics

This package (`pypokedex`) only provides one function through the
public API- `get`. It can be used as follows:

```python
import pypokedex

pokemon = pypokedex.get(dex=DEX)  # DEX must be a valid _national_ pokedex
                                  # number
pokemon2 = pypokedex.get(name=NAME)  # NAME must be a valid name of a pokemon
```

#### Possible errors

If `get` is called with an incorrect signature (e.g too many arguments), then
a `TypeError` will be raised with details about the problem. If the pokemon is
not found, then a `pypokedex.exceptions.PyPokedexHTTPError` will be raised with
a status code of 404. For more details, see the section on [exceptions](#exceptions)

## Exceptions



## License

This library is licensed under the [MIT License](https://github.com/arnavb/pypokedex/blob/master/LICENSE).
