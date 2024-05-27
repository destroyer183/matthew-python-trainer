import json

def function(*args):

    for item in args:
        print(f"item: {item}")

f = open('testing.json')

data = json.load(f)

print(f"old data: {data}\n")

for test_case in data['test cases']:

    
    test_case['input'] = tuple(test_case['input'])

    function(*test_case['input'])

    print(f"new test case: {test_case['input']}\n")


print(f"new data: {data}\n")


