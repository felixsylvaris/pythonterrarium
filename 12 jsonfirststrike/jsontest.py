import json


starter="Hello, World!"
print("first instance")
print(starter)
# write to file
with open("sample.json", "w") as f:
    json.dump(starter, f)

# Read from file and parse JSON
with open("sample.json", "r") as f:
    data = json.load(f)
print("second instance")
print(data)
print(type(data))
