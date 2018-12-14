from collections import OrderedDict


def react(poly):
    mask = set()
    while True:
        prev = None
        for k, v in poly.items():
            if prev is None:
                prev = (k, v)
                continue
            a, b = prev[1], v
            if a.islower() != b.islower() and a.lower() == b.lower():
                mask.add(k)
                mask.add(prev[0])
                prev = None
            else:
                prev = (k, v)
        if len(mask) == 0:
            break
        for idx in mask:
            del poly[idx]
        mask.clear()

    return poly


polymer = open('input.txt').read().rstrip()

poly = OrderedDict((i, l) for i, l in enumerate(polymer))

print('#1')
print(len(react(poly.copy())))

print('#2')
all_letters = {l.lower() for l in set(polymer)}

results = []
for letter in sorted(all_letters):
    letters = {l for l in [letter, letter.upper()]}
    poly_copy = OrderedDict((k, v) for k, v in poly.items() if v not in letters)
    res = (letter, len(react(poly_copy)))
    print(res)
    results.append(res)

print('Best letter to remove: ', sorted(results, key=lambda item: item[1])[0])
