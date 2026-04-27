import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://aniya:root1234@localhost:5432/netflix_data')

query_rating = "SELECT rating, COUNT(*) as count FROM netflix_movies GROUP BY rating ORDER BY count DESC"
print(pd.read_sql(query_rating, engine))

print("\n" + "="*30 + "\n")


query_category = "SELECT listed_in, COUNT(*) as count FROM netflix_movies GROUP BY listed_in ORDER BY count DESC LIMIT 10"
print(pd.read_sql(query_category, engine))