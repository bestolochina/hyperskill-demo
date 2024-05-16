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


def binary_search(array, value):
    low = 0
    high = len(array) - 1
    while low <= high:
        middle = int((low+high)/2)
        if array[middle].rating == value:
            return middle
        elif array[middle].rating > value:
            high = middle - 1
        else:
            low = middle + 1
    return -1


Movie = namedtuple('Movie', ['title', 'rating'])
movies: list = []
path = r'C:\Users\T480\Downloads\movies.csv'
with open(path, 'r', encoding='utf-8') as csv_file:
    csvreader = csv.reader(csv_file)

    for title, rating in csvreader:
        m = Movie(title, float(rating))
        movies.append(m)

sorted_movies = bubble_sort(movies)

movie_6_index = binary_search(sorted_movies, 6)
left_index = movie_6_index
while sorted_movies[left_index - 1].rating == 6:
    left_index -= 1

right_index = movie_6_index
while sorted_movies[right_index + 1].rating == 6:
    right_index += 1

for i in range(left_index, right_index + 1):
    print(f'{sorted_movies[i].title} - {sorted_movies[i].rating}')
