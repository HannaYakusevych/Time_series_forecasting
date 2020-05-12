from pandas import read_csv

import pandas as pd

from statsmodels.tsa.stattools import adfuller

p1 = read_csv('ics_data/06_Smart_Meter_45/P1.csv', squeeze=True, index_col=0)
p2 = read_csv('ics_data/06_Smart_Meter_45/P2.csv', squeeze=True, index_col=0)
p3 = read_csv('ics_data/06_Smart_Meter_45/P3.csv', squeeze=True, index_col=0)
q1 = read_csv('ics_data/06_Smart_Meter_45/Q1.csv', squeeze=True, index_col=0)
q2 = read_csv('ics_data/06_Smart_Meter_45/Q2.csv', squeeze=True, index_col=0)
q3 = read_csv('ics_data/06_Smart_Meter_45/Q3.csv', squeeze=True, index_col=0)
u1 = read_csv('ics_data/06_Smart_Meter_45/U1.csv', squeeze=True, index_col=0)
u2 = read_csv('ics_data/06_Smart_Meter_45/U2.csv', squeeze=True, index_col=0)
u3 = read_csv('ics_data/06_Smart_Meter_45/U3.csv', squeeze=True, index_col=0)


def mul_values(dataframe, num):
    new_dataframe = dataframe.copy()
    for (data_index, index) in enumerate(dataframe.index):
        if index > num:
            break
        else:
            new_dataframe.values[data_index] *= 18
    return new_dataframe


corner_value = 1560434439432

p1 = mul_values(p1, corner_value)
p2 = mul_values(p2, corner_value)
p3 = mul_values(p3, corner_value)
q1 = mul_values(q1, corner_value)
q2 = mul_values(q2, corner_value)
q3 = mul_values(q3, corner_value)


def convert_timestamps(df):
    df.index = pd.to_datetime(df.index, unit='ms')
    return df


p1 = convert_timestamps(p1)
p2 = convert_timestamps(p2)
p3 = convert_timestamps(p3)
q1 = convert_timestamps(q1)
q2 = convert_timestamps(q2)
q3 = convert_timestamps(q3)
u1 = convert_timestamps(u1)
u2 = convert_timestamps(u2)
u3 = convert_timestamps(u3)


def fix_timestamps(dataframes):
    # check input
    if len(dataframes) <= 0:
        return
    new_dataframes = []

    # get a full list of indices
    indices = dataframes[0].index
    for dataframe in dataframes:
        indices = indices.union(dataframe.index)
    print("Got all indices")

    for (data_index, dataframe) in enumerate(dataframes):
        dataframe = dataframe.reindex(indices, copy=True).fillna(method='ffill').fillna(method='bfill')
        new_dataframes.append(dataframe)
        print("dataframe", data_index + 1, "is fixed")

    return new_dataframes


data_list = fix_timestamps([p1, p2, p3, q1, q2, q3, u1, u2, u3])
p1 = data_list[0]
p2 = data_list[1]
p3 = data_list[2]
q1 = data_list[3]
q2 = data_list[4]
q3 = data_list[5]
u1 = data_list[6]
u2 = data_list[7]
u3 = data_list[8]

month_numbers = ['05', '06', '07', '08', '09', '10', '11']

# months_p2 = [p2.loc['2019-' + i] for i in month_numbers]
# months_q2 = [q2.loc['2019-' + i] for i in month_numbers]
# months_q3 = [q3.loc['2019-' + i] for i in month_numbers]
# months_u1 = [u1.loc['2019-' + i] for i in month_numbers]
months_u2 = [u2.loc['2019-' + i] for i in month_numbers]
months_u3 = [u3.loc['2019-' + i] for i in month_numbers]

print("Months are ready \n")


def run_adfuller(dataframe):
    result = adfuller(dataframe)
    print('adf: ', result[0])
    print('p-value: ', result[1])
    print('Critical values: ', result[4])
    if result[0] > result[4]['5%']:
        print('есть единичные корни, ряд не стационарен \n \n')
    else:
        print('единичных корней нет, ряд стационарен \n \n')


# run_adfuller(months_p2[2])
# run_adfuller(months_p2[3])
# run_adfuller(months_q2[1])
# run_adfuller(months_q2[2])
# run_adfuller(months_q3[2])
# run_adfuller(months_u1[1])
# run_adfuller(months_u1[2])
# run_adfuller(months_u2[1])
# run_adfuller(months_u2[2])
# run_adfuller(months_u3[1])
# run_adfuller(months_u3[2])
run_adfuller(months_u3[3])
run_adfuller(months_u3[4])
run_adfuller(months_u3[5])
run_adfuller(months_u3[6])
