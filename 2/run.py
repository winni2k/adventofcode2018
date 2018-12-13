from collections import defaultdict

lines = [l.rstrip() for l in open('input.txt', 'rt').readlines()]
counts = defaultdict(lambda: 0)
for line in lines:
    word = defaultdict(lambda: 0)
    for letter in line:
        word[letter] += 1
    for count in set(word.values()):
        counts[count] += 1
checksum = 1
for count, count_count in counts.items():
    if count > 1:
        checksum *= count_count
print('checksum: ', checksum)

import numpy as np

dist = np.zeros((len(lines), len(lines)))
for i in range(len(lines)):
    for j in range(i, len(lines)):
        dist[i, j] = sum(l1 != l2 for l1, l2 in zip(lines[i], lines[j]))

row1, row2 = sum(dist == 1).argmax(), sum(dist.transpose() == 1).argmax()
line1, line2 = lines[row1], lines[row2]
letters = []
for l1, l2 in zip(line1, line2):
    if l1 == l2:
        letters.append(l1)
print(''.join(letters))
