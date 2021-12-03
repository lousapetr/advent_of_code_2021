import pandas as pd

test_df = pd.DataFrame(
    ["00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"],
    columns=['diag']
)


def import_data(input_file):
    df = pd.read_csv(input_file, delimiter=' ', header=None, names=['diag'], dtype=str)
    return df


def split_bits(series: pd.Series):
    # split binary numbers to multiple columns of 0/1
    return series.str.split('', expand=True).iloc[:, 1:-1].astype(int)


def bin2int(binary: str):
    return int(binary, base=2)


def part_1(df):
    df_split = split_bits(df['diag'])
    one_bit_count = df_split.sum()
    gamma = one_bit_count > len(df) / 2  # True = more ones than zeros
    epsilon = one_bit_count < len(df) / 2
    gamma = gamma.astype(int).astype(str).sum()  # convert bools to "0"/"1"
    epsilon = epsilon.astype(int).astype(str).sum()  # convert bools to "0"/"1"
    return bin2int(gamma) * bin2int(epsilon)


def part_2(df):
    df_split = split_bits(df['diag'])

    oxygen_df = df_split.copy()
    while len(oxygen_df) > 1:
        # print(len(oxygen_df))
        start_bit = oxygen_df.iloc[:, 0].sum() >= len(oxygen_df) / 2  # True = more ones than zeros, most common is 1
        mask = oxygen_df.iloc[:, 0] == int(start_bit)
        oxygen_df = oxygen_df.loc[mask].iloc[:, 1:]
    oxygen = oxygen_df.join(df)

    co2_df = df_split.copy()
    while len(co2_df) > 1:
        # print(len(co2_df))
        start_bit = co2_df.iloc[:, 0].sum() < len(co2_df) / 2  # True = more zeros than ones, least common is 1
        mask = co2_df.iloc[:, 0] == int(start_bit)
        co2_df = co2_df.loc[mask].iloc[:, 1:]
    co2 = co2_df.join(df)

    print(oxygen)
    print(co2)

    return bin2int(oxygen.loc[:, 'diag'].iloc[0]) * bin2int(co2.loc[:, 'diag'].iloc[0])


df = import_data('./inputs/03_input.txt')
# print(df)

print('=' * 15)
print("Part 1:")
print(part_1(df))

print('=' * 15)
print("Part 2:")
# print(part_2(test_df))
print(part_2(df))
