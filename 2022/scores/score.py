from pathlib import Path
import pandas as pd
from time import perf_counter
import json
from datetime import datetime
# from collections import defaultdict
# from copy import copy

input_path = Path(f'{__file__}/../score.json').resolve()

with open(input_path, 'r') as f:
    data = json.load(f)

with open(input_path, 'w') as f:
    json.dump(data, f, indent=4)

mem_data = []
day = 3
num_players = 71


def to_timedelta(ts):
    return datetime.utcfromtimestamp(ts) - datetime(year=2022, month=12, day=day, hour=5)


for member in data['members'].values():
    if str(day) not in member['completion_day_level'].keys():
        continue
    if '2' not in member['completion_day_level'][str(day)].keys():
        continue
    d = [
        member['name'],
        member['local_score'],
        to_timedelta(member['completion_day_level'][str(day)]['1']['get_star_ts']),
        to_timedelta(member['completion_day_level'][str(day)]['2']['get_star_ts']),
        # member['completion_day_level']
    ]

    d = [*d, d[3]-d[2]]
    d = [*d[:2], *(str(i) for i in d[2:])]
    mem_data.append(d)

# mem_data = sorted(mem_data, key=lambda x: x[1], reverse=True)
df = pd.DataFrame(mem_data, columns=['Name', 'Score', 'T1', 'T2', 'DeltaT'])
df = df.sort_values(by='T1')
df['P1'] = [*zip(*enumerate(df['T1'], start=1))][0]
df = df.sort_values(by='T2')
df['P2'] = [*zip(*enumerate(df['T2'], start=1))][0]
df['Points'] = 2 * num_players - df['P1'] - df['P2'] + 2
df = df.sort_values(by='Points', ascending=False)
df = df.reset_index(drop=True)

print(df)
