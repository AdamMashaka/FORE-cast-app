
import pandas as pd
import numpy as np


def preprocess_raw_dataset(upload_path):
    pc_dataframes = []
    uc_dataframes = []
    years = ['2020','2021','2022','2023']

    for idx in range(len(years)):
        year = years[idx]
        df = pd.read_excel(upload_path, sheet_name=year)
        df.columns = df.iloc[0].values
        df = df.iloc[2:]
        columns = list(df.columns)
        for col in range(len(columns)):
            columns[col] = str(columns[col])
            if columns[col] == 'nan' and col>1:
                columns[col] = columns[col-1]+"-"+year
        df.columns = columns
        df.rename(columns={df.columns[0]: "Label"}, inplace=True)
        col_names = df.columns[df.columns.str.contains('-'+year,case = False)]
        col_names = ['Label'] + col_names.tolist()
        df_sum_of_uc = df[col_names]
        df_sum_of_uc.drop(df_sum_of_uc.index[0], inplace=True)

        col_names = df.columns[~df.columns.str.contains('-'+year,case = False)]
        df_sum_of_pc = df[col_names]
        df_sum_of_pc.drop(df_sum_of_pc.index[0], inplace=True)
        df_sum_of_pc.columns = df_sum_of_pc.columns.astype(str) + '-'+year
        df_sum_of_pc.rename(columns={df_sum_of_pc.columns[0]: "Label"}, inplace=True)

        pc_dataframes.append(df_sum_of_pc)
        uc_dataframes.append(df_sum_of_uc)



    # merge all dataframes into one
    pc_merged = pc_dataframes[0]
    for df in pc_dataframes[1:]:
        pc_merged = pc_merged.merge(df, on='Label')

    uc_merged = uc_dataframes[0]
    for df in uc_dataframes[1:]:
        uc_merged = uc_merged.merge(df, on='Label')


    pc_merged.index = pc_merged['Label']
    pc_merged = pc_merged.drop(columns=["Label"])
    pc_merged = pc_merged.T

    pc_merged.index = pd.to_datetime(pc_merged.index)
    missing_dates = pd.date_range(start=pc_merged.index[0], end=pc_merged.index[-1])
    pc_merged = pc_merged.reindex(missing_dates, fill_value=0)
    pc_merged = pc_merged.fillna(0)


    # drop all columns with names with more than 12 characters
    uc_merged = uc_merged.loc[:, uc_merged.columns.str.len() <= 12]
    uc_merged.index = uc_merged['Label']
    uc_merged.drop(columns=["Label"], inplace=True)
    uc_merged = uc_merged.T

    uc_merged.index = pd.to_datetime(uc_merged.index)
    missing_dates = pd.date_range(start=uc_merged.index[0], end=uc_merged.index[-1])
    uc_merged = uc_merged.reindex(missing_dates, fill_value=0)
    uc_merged = uc_merged.fillna(0)


    # save to csv
    pc_merged.to_csv('data/processed/pc_sums.csv')
    uc_merged.to_csv('data/processed/uc_sums.csv')

    return pc_merged, uc_merged