#-----------------------------------------------------------------------------
# This script converts txt doc storing excel column data into JS array
#-----------------------------------------------------------------------------

with open("categories.txt", "r") as file:
    cities = [line.strip() for line in file if line.strip()]

js_array = "[" + ", ".join(['"' + city + '"' for city in cities]) + "]"

print(js_array)