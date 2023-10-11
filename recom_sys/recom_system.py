# import library
import pandas as pd


# data loading
bli_df = pd.read_csv('../data_engineering/BlibliMas_clean_latest.csv')
bulak_df = pd.read_csv('../data_engineering/BukalapakMas_clean_latest.csv')
tokped_df = pd.read_csv('../data_engineering/TokMas_clean_latest.csv')
gold_price_latest = pd.read_csv('../data_engineering/HargaEmas_clean_latest.csv')

# gabungin data
store_df = pd.concat([bli_df, bulak_df, tokped_df], ignore_index=True)

# data filtering

## drop produk yang bukan antam
idx_to_drop = store_df[(store_df['product_name'].str.contains('ANTAM') == False) & (store_df['product_name'].str.contains('Antam') == False) &
                       (store_df['product_name'].str.contains('antam') == False)].index.tolist()
store_df.drop(index=idx_to_drop, inplace=True)
store_df.reset_index().drop(columns='index', inplace=True)

## filter produk yang bukan 1 gram
store_df = store_df[(store_df['product_name'].str.contains('1') == True) & (store_df['product_name'].str.contains('10') == False) &
                    (store_df['product_name'].str.contains('0.5') == False) & (store_df['product_name'].str.contains('0,5') == False)]

# bikin metric baru
store_df['price_diff'] = store_df['price'] - gold_price_latest['price'][0]
store_df['popularity_score'] = store_df['number_sold'] * store_df['rating']

## filter produk yang selisih harganya positif
store_df = store_df[store_df['price_diff'] >= 0]
store_df['price_diff'].replace(0, 0.1, inplace=True)

# bikin metric final score
store_df['final_score'] = store_df['popularity_score'] / store_df['price_diff']
store_df.sort_values('final_score', ascending=False).head()