import pandas as pd

# Excelファイルを読み込む
df = pd.read_excel('create_ddl.xlsx', sheet_name='テーブル定義')

# テーブル名を取得する
table_name = df.columns[0]

# 列名、データ型、長さ、主キー、複合キー、必須チェック、コメントを取得し、DDLを生成する
ddl = f"CREATE TABLE {table_name} (\n"
for row in df.iterrows():
    print(df)
    exit()
    col_name = row[1][0]
    data_type = row[1][1]
    length = row[1][2]
    pk = row[1][3]
    fk = row[1][4]
    not_null = row[1][5]
    comment = row[1][6]
    if pd.isna(length):
        ddl += f"    {col_name} {data_type},\n"
    else:
        ddl += f"    {col_name} {data_type}({length}),\n"
    if pk == 'PK':
        ddl += f"    PRIMARY KEY ({col_name}),\n"
    if fk:
        ddl += f"    FOREIGN KEY ({col_name}) REFERENCES {fk},\n"
    if not_null == 'NOT NULL':
        ddl = ddl[:-2] + " NOT NULL,\n"
    if comment:
        ddl += f"    COMMENT '{comment}',\n"
ddl = ddl[:-2] + ");"

# COLLATIONは「utf8mb4_general_ci」固定
ddl += 'ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci'

print(ddl)