import pandas as pd


def import_data(input_file):
    df = pd.read_csv(input_file, delimiter=' ', header=None, names=['direction', 'length'])
    return df


def part_1(df):
    result_dict = df.groupby('direction').sum()['length'].to_dict()
    result = result_dict['forward'] * (result_dict['down'] - result_dict['up'])
    return result


def part_2(df):
    df['signed_dir'] = df['direction'].replace({'down': 1, 'up': -1, 'forward': 0})
    df['aim_change'] = df['signed_dir'] * df['length']
    df['aim'] = df['aim_change'].cumsum()
    # df_moving = df.loc[df['direction'] == 'forward', :]
    moving_mask = df['direction'] == 'forward'
    df.loc[:, 'position_horizontal'] = df.loc[moving_mask, 'length'].cumsum()
    df.loc[:, 'position_vertical'] = (df.loc[moving_mask, 'length'] * df.loc[moving_mask, 'aim']).cumsum()
    df_final = df.loc[moving_mask, :].tail(1)
    result = df_final['position_horizontal'] * df_final['position_vertical']
    # return df
    return int(result.iloc[0])


df = import_data('02_input.txt')
print(part_1(df))
print(part_2(df))
