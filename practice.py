from random import choices


population = list('abcdefghijklmnop')
weights = [10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

sample = choices(population=population, weights=weights, k=15)

print(sample)