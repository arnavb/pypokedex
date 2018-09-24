import pypokedex

example = pypokedex.get(dex=1)

print(f'Name: {example.name}')
print(f'ID: {example.dex}')
print(f'Types: {example.types}')
print(f'Types: {example.abilities}')
