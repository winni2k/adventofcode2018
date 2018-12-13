from collections import defaultdict
from datetime import datetime, timedelta
from itertools import chain, cycle

import pandas as pd


def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


def guard_with_most_minutes_asleep(guards, sleep_times):
    guard_sleep_time = defaultdict(int)
    for date, times in sleep_times.items():
        guard_sleep_time[guards[date]] += sum(t[1] for t in times)
    return sorted(guard_sleep_time.items(), key=lambda kv: kv[1], reverse=True)[0]


lines = open('input.txt').readlines()

guards = {}
dates = defaultdict(list)
for line in lines:
    fields = line.rstrip().split()
    the_dt = datetime.strptime(line[:18], '[%Y-%m-%d %H:%M]')

    if fields[2] == 'Guard':
        if the_dt.time().hour > 0:
            the_dt = the_dt + timedelta(days=1)
        guards[the_dt.date()] = fields[3]
    else:
        assert the_dt.hour == 0
        dates[the_dt.date()].append((the_dt.minute, fields[2]))

sleep_durations = {}
dates = {k: sorted(v) for k, v in dates.items()}
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
    sleep_durations[date] = sleep_lengths

print('Strategy #1')
ls_guard = guard_with_most_minutes_asleep(guards, sleep_durations)
print(f'longest sleeping guard: {ls_guard}')

ls_guard_sleep_durations = flatten(sleep_durations[date] for date, _ in
                                   filter(lambda item: item[1] == ls_guard[0], guards.items()))
minutes_slept = defaultdict(int)
for start_minute, duration in ls_guard_sleep_durations:
    for minute in range(start_minute, start_minute + duration):
        minutes_slept[minute] += 1

most_slept_minute = sorted(minutes_slept.items(), key=lambda pair: pair[1], reverse=True)[0]
print(f'Most slept minute: {most_slept_minute}')

guard_id = int(ls_guard[0].lstrip('#'))
print(f'answer: {guard_id} * {most_slept_minute[0]} = {guard_id*most_slept_minute[0]}')

print('\nStrategy #2')
date_durations = flatten(
    list(zip(cycle([date]), durations)) for date, durations in sleep_durations.items())
date_durations = ((date, duration[0], duration[1]) for date, duration in date_durations)
date_durations = flatten(
    [(date, minute) for minute in range(start, start + duration)] for date, start, duration in
    date_durations)

dd = pd.DataFrame.from_records(date_durations, columns=['date', 'minute'])
dd.set_index(keys='date', inplace=True)

guards = pd.DataFrame.from_records(list(guards.items()), columns=['date', 'guard_id']).set_index(keys='date')
dd = dd.join(guards)

dd = dd.groupby(by='guard_id').apply(lambda x: x.minute.value_counts())#.sort_values(by='count'))
dd = dd.reset_index(name='count')
dd.columns = ['guard_id', 'minute', 'count']
guard_id, minute = dd.iloc[dd['count'].agg('idxmax')][0:2]
print(guard_id, minute, '=', int(guard_id.lstrip('#')) * minute)

