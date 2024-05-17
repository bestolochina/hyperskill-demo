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


def merge(arr, left, medium, right):
    n1 = medium + 1 - left
    n2 = right - medium

    left_arr = arr[left: medium + 1]
    right_arr = arr[medium + 1: right + 1]

    # Merge the temp arrays back into arr[l...r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = left  # Initial index of merged subarray

    while i < n1 and j < n2:
        if left_arr[i].rating <= right_arr[j].rating:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1

    # Copy the remaining elements of left_arr[], if there are any
    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1

    # Copy the remaining elements of right_arr[], if there are any
    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1


def merge_sort(arr, left, right):
    if left < right:
        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        medium = left + (right - left) // 2

        # Sort first and second halves
        merge_sort(arr, left, medium)
        merge_sort(arr, medium + 1, right)
        merge(arr, left, medium, right)


Movie = namedtuple('Movie', ['title', 'rating'])
movies: list = []
path = r'C:\Users\aaa\Downloads\movies.csv'
with open(path, 'r', encoding='utf-8') as csv_file:
    csvreader = csv.reader(csv_file)

    for title, rating in csvreader:
        m = Movie(title, float(rating))
        movies.append(m)

# sorted_movies = bubble_sort(movies)
sorted_movies = copy.deepcopy(movies)
merge_sort(sorted_movies, 0, len(sorted_movies) - 1)

movie_6_index = binary_search(sorted_movies, 6)
left_index = movie_6_index
while sorted_movies[left_index - 1].rating == 6:
    left_index -= 1

right_index = movie_6_index
while sorted_movies[right_index + 1].rating == 6:
    right_index += 1

for i in range(left_index, right_index + 1):
    print(f'{sorted_movies[i].title} - {sorted_movies[i].rating}')
