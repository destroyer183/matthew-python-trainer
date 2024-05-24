import json

temp = []
formatted = []

with open('testing.txt', 'r') as f:

    for line in f:

        line = line.strip()

        temp.append(line)



for data in temp:

    print(f"old data: {data}\ntype: {type(data)}\n")

    data = json.loads(data)

    formatted.append(data)


for data in formatted:

    print(f"new data: {data}")