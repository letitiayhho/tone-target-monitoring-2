import random

def check_repeat(l):
    for i, item in enumerate(l):
        if i == len(l)-1:
            return tuple(l)
        if l[i] == l[i+1]:
            break

permutations = 1000
no_repeats = set()
conditions = [1, 1, 2, 2, 3, 3]
for i in range(permutations):
    random.shuffle(conditions)
    checked_list = check_repeat(conditions)
    if checked_list:
        no_repeats.add(checked_list)
no_repeats = list(no_repeats)

print(no_repeats)
print(len(no_repeats))