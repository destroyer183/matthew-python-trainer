import binascii

def string_to_int(input = None):

    if input is None:
        print('no value given\n\n')

    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()`-=[]\;\',./~_+{}|:\"<>? '

    values = {}

    for value, key in enumerate(chars):

        if len(str(value)) == 1:

            values[key] = f'0{value}'

        else:

            values[key] = str(value)

    output = []

    for value in input:

        output.append(values[value])

    return output



with open('account_template.txt', 'wb') as f, open('data_template', 'wb') as fout:

    first_line = b'\n'

    fout.write(first_line)

    second_line = ''

    for i in range(108):
        second_line += ' '

    second_line = ('').join(string_to_int(second_line))

    second_line = binascii.unhexlify(second_line)

    fout.write(second_line)