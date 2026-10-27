from pathlib import Path
import pandas as pd
import json 

"""
For reference
{
    "name": "str",
    "capital": "str",
    "population": "int64",
    "area": "float64",
    "region": "str"
}

You can get data from here: https://www.kaggle.com/datasets/krishnanshverma/worldwide-countries-dataset
"""

default_dir = Path(__file__).resolve().parent  # script's folder, not the CWD
df = pd.read_csv(default_dir / "countries.csv") # still using local director 
print(df.head())

print(df.dtypes)

output_path = default_dir / "output.txt" # pick same directory
# first we test txt logfile
with open(output_path, "w") as f:
    s=str(df.dtypes)
    f.write(s)

with open(output_path) as f:
  print("File read")
  print(f.read()) 

schema = {column: str(dtype) for column, dtype in df.dtypes.items()} #maybe json would work better

with open(default_dir / "output.json", "w") as f:
    json.dump(schema, f, indent=4)

task1 = df.loc[df['population'].idxmax(), ['name', 'population']]

maxpop = {
    "description": "Country with biggest population",
    "country": task1["name"],
    "population": int(task1["population"])
}

with open(default_dir / "output.json", "a") as f:
    json.dump(maxpop, f, indent=4)
    f.write("\n")

task2 = df.loc[df['area'].idxmin(), ['name', 'area']]

print(task2)

minarea = {
    "description": "Country with smallest area",
    "country": task2["name"],
    "area": float(task2["area"])
}

with open(default_dir / "output.json", "a") as f:
    json.dump(minarea, f, indent=4)
    f.write("\n")

# largest area per region
# Largest country per region
idx = df.groupby("region")["area"].idxmax()
task3 = df.loc[idx, ["region", "name", "area"]]

print(task3)


maxarearegion = {
    "description": "country with largest area per region",
    "countries": task3.to_dict(orient="records")
}

with open(default_dir / "output.json", "a") as f:
    json.dump(maxarearegion, f, indent=4)
    f.write("\n")

# make density field
df["density"] = df["population"] / df["area"]

task4 = df.loc[df["density"].idxmax(), ["name", "population", "area", "density"]]
task4["density"]=task4["density"].round(1)

print(task4)
# here we define dictionary to dump to json 
density = {
    "description": "Countries with largest density of population",
    "name": task4["name"],
    "population" : float(task4["population"]),
    "area" : float(task4["area"]),
    "density" : float(task4["density"])

    
}

with open(default_dir / "output.json", "a") as f:
    json.dump(density, f, indent=4)
    f.write("\n")
   
# mean population per country in region
task5 = df.groupby("region")["population"].mean().round(2).sort_values(ascending=False)

print(task5)


# task6 print countries but only above 100mln population
task6 = df.loc[df["population"] > 100_000_000, ["name", "population"]]
task6 = task6.sort_values("population", ascending=False)

print(task6)

# task7 5 largest countries in area 
task7 = df.nlargest(5, "area")[["name", "region", "area"]]

print(task7)

# task8 how many countries in each region
task8 = df["region"].value_counts()

print(task8)

# task9 Find the median population of countries in each region.

task9=df.groupby("region")["population"].median().round(2)
print(task9)

task9b = df.groupby("region")[["population", "area"]].agg(["min", "max", "mean", "median"]).round(2) #we can get multiplies at once 
print(task9b)

# we can be sellective. 
task9c = df.groupby("region").agg(
    mean_area=("area", "mean"),
    median_pop=("population", "median")
).round(2)
print(task9c)

# Task 10: Find countries whose population density exceeds the global median density. 
global_den_med=df["density"].median()
print(global_den_med)
task10=df[df["density"]>global_den_med].sort_values("density", ascending=False).round(2)
print(task10.head())

# Task 11: Calculate what percentage of the total population represented by your dataset lives in each region.
#  This introduces a slightly more involved calculation: group totals, divide by the overall total, and multiply by 100.

global_pop = df["population"].sum()

task11 = df.groupby("region")["population"].sum().round(2).reset_index()
task11.columns = ["region", "population"]
task11["pop percent"] = (task11["population"]*100 / global_pop).round(2)

print(task11)
