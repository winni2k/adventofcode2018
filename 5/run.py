polymer = open('input.txt').read().rstrip()


def find_first_match(polymer):
    for i in range(len(polymer) - 1):
        a, b = polymer[i], polymer[i + 1]
        if a.islower() != b.islower() and a.lower() == b.lower():
            return i
    return None


while True:
    print(len(polymer))
    match_idx = find_first_match(polymer)
    if match_idx is None:
        break
    polymer = polymer[:match_idx] + polymer[match_idx + 2:]
print(f'result: {len(polymer)}')

