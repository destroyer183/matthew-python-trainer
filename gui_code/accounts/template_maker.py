import binascii



chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()`-=[]\;\',./~_+{}|:\"<>? \n'

char_values = {}

for value, key in enumerate(chars):

    if len(str(value)) == 1:

        char_values[key] = f'0{value}'
    
    else:

        char_values[key] = str(value)



def string_to_int(input = None):

    if input is None:
        print('no value given\n\n')

    output = []

    for value in input:

        output.append(char_values[value])

    return output



with open('account_template.txt', 'wb') as f, open('data_template', 'wb') as fout:

    first_line = b'\n'

    fout.write(first_line)

    second_line = []

    for i in range(108):
        second_line.append(' ')

    for item in second_line:

        temp = ('').join(string_to_int(item))

        temp = binascii.unhexlify(temp)

        fout.write(temp)