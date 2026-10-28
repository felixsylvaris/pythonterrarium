
"""
This is little script to load csv into local ide, establish sqllite server with sql alchemy, do some query, and quick log it into txt file. 
quick log is more terminal dump than structure. 

"""


from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
import os

# Find the folder containing this script
folder = Path(__file__).resolve().parent

# Load the CSV into pandas
df = pd.read_csv(folder / "countries.csv")

# Create a local SQLite database file
engine = create_engine(
    f"sqlite:///{folder / 'countries.db'}"
)

# Write the DataFrame into a database table
df.to_sql(
    "countries",
    engine,
    if_exists="replace",
    index=False
)


default_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(default_dir, "outputalch.txt")

# Query the database using SQL
with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT region, COUNT(*) AS country_count,
                   SUM(population) AS total_population
            FROM countries
            GROUP BY region
            ORDER BY total_population DESC
        """)
    )
    query1 = result.fetchall() # we store our results 

    for row in query1:
        print(row)

    with open(output_path, "w", encoding="utf-8") as f:
        for row in query1:
            f.write(str(row) + "\n")
    





