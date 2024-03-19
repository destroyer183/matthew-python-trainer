import binascii
import mmap








def string_to_int(input = None):

    if input is None:
        print('no value given\n\n')

    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()`-=[]\;\',./~_+{}|:\"<>?'

    values = {}

    for key, value in enumerate(chars):

        if len(str(key)) == 1:

            values[value] = f'0{key}'
        
        else:

            values[value] = str(key)


    values[' '] = 100


    output = []

    for value in input:

        output.append(values[value])

    return output



with open('account_template.txt', 'wb') as f:
    f.write(b'Hello Python!\n')


with open('account_template.txt', 'r+b') as f, open('test', 'r+b') as fout:

    fmm = mmap.mmap(f.fileno(), 0)
    # foutmm = mmap.mmap(fout.fileno(), 0, access=mmap.ACCESS_READ)

    string = "hello"

    string = ('').join(string_to_int(string))

    new_string = binascii.unhexlify(string)

    fmm.seek(0)

    fmm.write(new_string)
    fmm.write(b'\n')
    fmm.write(new_string)




