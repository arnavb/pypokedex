import pypokedex

example = pypokedex.get(name='Garchomp')

print(f'Name: {example.name}')
print(f'ID: {example.dex}')
print(f'Types: {example.types}')
print(f'Types: {example.abilities}')
print(f'Stats: {example.base_stats}')
