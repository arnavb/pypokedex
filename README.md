<p align='center'>
    <img src='https://raw.githubusercontent.com/arnavb/pypokedex/master/assets/logo.png'/>
</p>

[![Build Status](https://travis-ci.org/arnavb/pypokedex.svg?branch=master)](https://travis-ci.org/arnavb/pypokedex)
[![Codecov](https://img.shields.io/codecov/c/github/arnavb/pypokedex.svg)](https://codecov.io/gh/arnavb/pypokedex)

PyPokedex is a minimal pokedex library for Python. Usage of the library can be 
summarized as follows:

```
>>> import pypokedex
>>> p = pypokedex.get(dex=445) # Or pypokedex.get(name='Garchomp')
>>> p.name
'garchomp'
>>> p.dex
445
>>> p.weight
950
>>> p.height
19
>>> p.types
['ground', 'dragon']
>>> p.base_stats
BaseStats(hp=108, attack=130, defense=95, sp_atk=80, sp_def=85, speed=102)
>>> [move.name for move in p.moves['sun-moon']] # Garchomp's Sun/Moon move names
['swords-dance', 'sand-attack', 'sand-attack', 'tackle', ...]
>>> p.abilities
[Ability(name='rough-skin', is_hidden=True), Ability(name='sand-veil', is_hidden=False)]
```
