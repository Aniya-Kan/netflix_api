import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('netflix.csv')
print(df)

df['show_id'] = df['show_id'].astype(str)
print(df)

df['listed_in'] = df['listed_in'].str.strip()
df['rating'] = df['rating'].str.strip()

df['rating'] = df['rating'].fillna('Unrated')


engine = create_engine('postgresql://aniya:root1234@localhost:5432/netflix_data')
df.to_sql('netflix_movies', engine, if_exists = 'replace', index = False)

print("Прочитали csv файл, поменяли тип данных индексов на строковой тип чтобы избежать ошибок при работе с числовыми типами данных, создали движок который создает постгре БД в докере, перенесли данные в нашу БД")
print(f"Уникальные рейтинги - {df['rating'].nunique()}")

