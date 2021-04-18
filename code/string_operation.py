# string_operation.py
"""
strip()  will remove end line i.e. n
strip('"') will remove "
replace('"','_') will replace " with _ 
split(",") will make list for data with separator ','
"""
total_price = 0
with open('test.csv', 'r') as f:  # open the file as f
    header = next(f)  # skip line 1 as a header
    for line in f:
        line = line.strip()  # remove \n
        columns = line.split(',')
        columns[0] = columns[0].strip('"')
        columns[2] = float(columns[2])
        columns[3] = float(columns[3])
        columns[4] = int(columns[4])
        columns[1] = columns[1].strip('"')
        total_price += columns[2]*columns[3]

print("Total price = ", total_price)
