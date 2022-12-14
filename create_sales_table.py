# this script creates synthetic data using faker library

import pandas as pd
from faker import Faker
import random
from typing import List
from datetime import datetime


fake:Faker = Faker()

FAKE_PRODUCTS:List[str] = [
    'laptop',
    'earphones',
    'keyboard'
    ]


CUSTOMER_TABLE_SIZE:int = 30
SALES_TABLE_SIZE:int = 10000


def create_customer_table(row_number:int) -> pd.DataFrame:
    df:pd.DataFrame = pd.DataFrame()
    for i in range(row_number):
        df.loc[i, 'customer_id'] = i + 1
        df.loc[i, 'customer_name'] = fake.name()
        df.loc[i, 'customer_country'] = fake.country()

    return df


def create_product_table(
    fake_products:List[str]
    ):
    df:pd.DataFrame = pd.DataFrame()
    for i, product in enumerate(fake_products):
        df.loc[i, 'product_id'] = i + 1
        df.loc[i, 'product_name'] = product
        df.loc[i, 'product_price'] = random.randint(1, 100)
        df.loc[i, 'product_brand'] = fake.company()
    return df


def create_sales_table(
    customer_table:pd.DataFrame,
    product_table:pd.DataFrame,
    number_of_rows:int):
    all_dfs:List[pd.DataFrame] = []
    for i in range(number_of_rows):
        customer_sample = customer_table.sample(1).reset_index(drop=True)
        product_sample = product_table.sample(1).reset_index(drop=True)
        concated_df = pd.concat(
            [customer_sample, product_sample],
            axis=1
            )
        concated_df['quantity'] = random.randint(1, 10)
        concated_df['date'] = fake.date_between_dates(
            date_start = datetime(2022, 9, 1),
            date_end = datetime(2022,9, 15)
        )
        concated_df['transaction_id'] = i + 1
        all_dfs.append(concated_df)
    return pd.concat(all_dfs)



def main():
    customer_table:pd.DataFrame = create_customer_table(CUSTOMER_TABLE_SIZE)
    customer_table.to_csv('customer.csv', index=False)
    product_table:pd.DataFrame = create_product_table(FAKE_PRODUCTS)
    product_table.to_csv('product.csv', index=False)
    sales_table:pd.DataFrame = create_sales_table(
        customer_table=customer_table,
        product_table=product_table,
        number_of_rows=SALES_TABLE_SIZE
        )

    columns_selected:List[str] = [
    'transaction_id',
    'date',
    'customer_id',
    'customer_name',
    'customer_country',
    'product_id',
    'product_name',
    'product_brand',
    'product_price',
    'quantity',
    ]

    sales_table = sales_table[columns_selected]
    sales_table.to_csv(
        'sales_table.csv',
        index=False
        )


if __name__ == '__main__':
    main()
