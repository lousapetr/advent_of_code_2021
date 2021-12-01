import pandas as pd

df = pd.read_csv('01_input.txt', header=None, names=['depth'])

df['lag'] = df['depth'].shift(-1)
df['larger'] = df['lag'] > df['depth']

print('Part One:', df['larger'].sum())

df['window'] = df['depth'].rolling(window=3).sum()
df['win_lag'] = df['window'].shift(-1)
df['win_larger'] = df['win_lag'] > df['window']

print('Part Two:', df['win_larger'].sum())
