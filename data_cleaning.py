
import pandas as pd
import numpy as np

data = {
    'Customer_ID': [
        'C001', 'C002', 'C003', 'C004',
        'C005', 'C001', 'C006', 'C007'
    ],
    'Name': [
        '  Nguyen Van A ', 'Tran Thi B',
        'Le Van C', 'Pham Thi D',
        'Hoang Van E', '  Nguyen Van A ',
        'Vu Thi F', 'Doan Van G'
    ],
    'Age': [25, 30, np.nan, -5, 45, 25, 150, 28],
    'Gender': [
        'Nam', 'Nu', 'male', 'Female',
        'Nam', 'Nam', 'Nữ', 'Nam'
    ],
    'Join_Date': [
        '2023-01-15', '2023/02/20',
        '15-03-2023', '2023-04-01',
        None, '2023-01-15',
        '2023-06-10', '2023-07-05'
    ],
    'Total_Spend': [
        '1000000', '2500000', ' 1500000 ',
        '3000000', 'invalid_amount',
        '1000000', '500000', None
    ]
}

df_raw = pd.DataFrame(data)

df_raw.to_csv(
    'raw_customers.csv',
    index=False,
    encoding='utf-8-sig'
)

df = pd.read_csv('raw_customers.csv')

print("\n--- DU LIEU THO ---")
print(df)

print("\n--- THONG TIN BAN DAU ---")
df.info()


print("\nSo dong trung lap:",
      df.duplicated().sum())

df = df.drop_duplicates()
df = df.reset_index(drop=True)


df['Name'] = df['Name'].str.strip()
df['Total_Spend'] = df['Total_Spend'].str.strip()


df['Gender'] = df['Gender'].replace({
    'Nam': 'Nam',
    'Nu': 'Nữ',
    'male': 'Nam',
    'Female': 'Nữ',
    'Nữ': 'Nữ'
})


df['Total_Spend'] = pd.to_numeric(
    df['Total_Spend'],
    errors='coerce'
)

spend_median = df['Total_Spend'].median()

df['Total_Spend'] = df['Total_Spend'].fillna(
    spend_median
)


df['Age'] = pd.to_numeric(
    df['Age'],
    errors='coerce'
)

df.loc[
    (df['Age'] < 0) | (df['Age'] > 100),
    'Age'
] = np.nan

age_median = df['Age'].median()

df['Age'] = df['Age'].fillna(age_median)
df['Age'] = df['Age'].astype(int)


df['Join_Date'] = pd.to_datetime(
    df['Join_Date'],
    format='mixed',
    dayfirst=True,
    errors='coerce'
)

df['Join_Date'] = df['Join_Date'].ffill()


print("\n--- THONG TIN SAU LAM SACH ---")
df.info()

print("\n--- THONG KE DU LIEU ---")
print(df.describe())

print("\n--- GIA TRI THIEU ---")
print(df.isnull().sum())

print("\n--- DU LIEU SACH HOAN CHINH ---")
print(df.to_string(index=False))

df.to_csv(
    'clean_customers.csv',
    index=False,
    encoding='utf-8-sig',
    date_format='%Y-%m-%d'
)

print("\nDa luu file clean_customers.csv")
