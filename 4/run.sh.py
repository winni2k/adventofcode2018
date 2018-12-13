from collections import defaultdict

lines = open('input.txt').readlines()

guards = {}
dates = defaultdict(list)
for line in lines:
    fields = line.rstrip().split()
    fields[0] = fields[0].lstrip('[')
    fields[1] = int(fields[1].rstrip(']').rpartition(':')[2])
    if fields[2] == 'Guard':
        guards[fields[0]] = fields[3]
    else:
        dates[fields[0]].append(fields[1:3])
dates = {k: sorted(v) for k, v in dates.items()}

sleep_times = {}
for date, state_changes in dates.items():
    sleep_lengths = []
    awake = True
    prev_timepoint = 0
    for timepoint, state in state_changes:
        if awake:
            assert state == 'falls'
            awake = False
            prev_timepoint = timepoint
        else:
            assert state == 'wakes'
            awake = True
            sleep_lengths.append((prev_timepoint, timepoint - prev_timepoint))
    sleep_times[date] = sleep_lengths
print(dates)
print(sleep_times)
