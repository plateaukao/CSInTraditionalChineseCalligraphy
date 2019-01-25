import random

index_combine_set = set()

while True:
    if len(index_combine_set) >= 81:
        break
    index_list = []
    for i in range(4):
        index_list.append(random.randint(1, 3))
    index_combine_set.add(tuple(index_list))


print(index_combine_set)
print(len(index_combine_set))
