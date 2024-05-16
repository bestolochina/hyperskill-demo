import copy
import csv
from collections import namedtuple


def bubble_sort(unsorted: list) -> list:
    sorted_list = copy.deepcopy(unsorted)
    for i in range(len(sorted_list) - 1):
        for j in range(len(sorted_list) - i - 1):
            if sorted_list[j].rating > sorted_list[j + 1].rating:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
    return sorted_list


Movie = namedtuple('Movie', ['title', 'rating'])
movies: list = []
path = r'C:\Users\T480\Downloads\movies.csv'
with open(path, 'r', encoding='utf-8') as csv_file:
    csvreader = csv.reader(csv_file)

    for title, rating in csvreader:
        m = Movie(title, float(rating))
        movies.append(m)

sorted_movies = bubble_sort(movies)

for movie in sorted_movies:
    print(f'{movie.title} - {movie.rating}')
