import csv

dct = {'Name': 'John', 'Age': '23', 'Country': ['USA',"USB"]}

"""with open('dct.csv', 'w') as f:
    writer = csv.writer(f)
    for k, v in dct.items():
        if(type(v) in [tuple, list, set]):
            writeIn = [k] + v
            writer.writerow(writeIn)
        else:
            writer.writerow([k])"""

with open('dct.csv',"w") as f:
    writer = csv.writer(f)
    writer.writerow(["CHINA","111"])
