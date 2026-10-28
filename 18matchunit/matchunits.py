"""
this is example of match use and case, for purpose of unit converter 

"""
def convert(value, unit):
    match unit.lower():
        case "km":
            return f"{value} km = {value * 0.621371:.2f} miles"
        case "miles":
            return f"{value} miles = {value / 0.621371:.2f} km"
        case "kg":
            return f"{value} kg = {value * 2.20462:.2f} pounds"
        case "lb":
            return f"{value} pounds = {value / 2.20462:.2f} kg"
        case _:
            return "Unknown unit. Use km, miles, kg, or lb."


while True:
    command = input("Enter value and unit (e.g. 10 km), or q to quit: ")

    if command.lower() == "q":
        break

    try:
        value, unit = command.split()
        value = float(value)
        print(convert(value, unit))
    except ValueError:
        print("Invalid input. Example: 10 km")
