# coding=utf-8


def distance_between(string_1, string_2):
    n, m = len(string_1), len(string_2)
    if n > m:
        string_1, string_2 = string_2, string_1
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if string_1[j - 1] != string_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]
