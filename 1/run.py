total = 0
seen = set()
lines = open('input', 'rt').readlines()
while True:
    for line in lines:
        line = line.rstrip()
        op = line[0]
        val = int(line[1:])
        if op == '+':
            total += val
        else:
            total -= val
        if total in seen:
            print(total)
            exit()
        seen.add(total)
        
