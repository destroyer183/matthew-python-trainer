import binascii


# create string to store every character that needs an integer representation
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890!@#$%^&*()`-=[]\;\',./~_+{}|:\"<>?\n'

# create dict to store integer representations of every character above 
char_values = {}

# loop over every character with both the index and the value
for index, value in enumerate(chars):

    # check if the string representation of the index is only one character long
    if len(str(index)) == 1:

        # create dictionary item with a key that is the charcter, and a value that is the index of that value
        # add a '0' to the front of the value, this is for purposes with converting hexidecimal to integer and vice versa, it makes things easier
        char_values[value] = f'0{index}'

    else:

        # create dictionary item with a key that is the character, and a value that is the index of that value
        char_values[value] = str(index)



# function to convert strings to integer values based on a table created when the file runs
def string_to_int(input: str):

    # print data
    print(f"\nconverting string to int...")
    print(f"input: {input}")

    # create list for the output
    output = []

    # loop over every character in the input string
    for value in input:

        # pass the string into the dictionary of character values as a key, and get the cooresponding value, and append it to the output list
        output.append(char_values[value])

    # print output list
    print(f"output: {output}\n")

    # return output list
    return output



# function to encrypt normal data to be written to a save file
def encrypt_data(input: str):

    # print data
    print(f"\nconverting string to byte...")
    print(f"input: {input}")

    # create empty byte for the output
    output = b''

    # loop over every character in the input string
    for value in input:

        # use the value as a key in the dictionary of character values to get the value associated with that key
        char_value = char_values[value]

        # pretend that the character value is a hexidecimal number (even though it isn't) and convert it back to an integer number
        hex_element = str(int(char_value, 16))

        # make sure that the element is at least 2 characters long
        if len(hex_element) % 2 != 0:
            hex_element = f"0{hex_element}"

        # print out element
        print(f"string: \"{hex_element}\"")

        # convert element to bytes with binascii function and add it to the output
        output += binascii.unhexlify(hex_element)

        # print out the byte value of the element
        print(f"value: {binascii.unhexlify(hex_element)}")

        # print out the current output bytes
        print(f"current output: {output}")

    # print out the full output
    print(f"output: {output}\n")

    # print out the integer representation of the output to make it easier to understand the output in the terminal
    print(f"hexlified: {binascii.hexlify(output)}")

    # return the output
    return output



# function to decrypt normal data that has been read from a save file
def decrypt_data(input: bytes):

    print(f"\nconverting byte to string...")

    print(f"input: {input}")

    input = binascii.hexlify(input)

    input = str(input).strip()

    input = input[2:len(input) - 1]

    temp_list = []

    temp_str = ''

    input = input.strip()

    split_size = 2

    for value in input:

        temp_str += value

        if len(temp_str) == split_size:

            if temp_str == '0a':
                continue

            temp_list.append(str(temp_str))
            temp_str = ''

            print(f"value: {str(temp_str)}, {temp_str}")

    output = ''

    print(f"temp_list: {temp_list}\n")

    for value in temp_list:

        value = hex(int(value))[2:]

        if len(value) == 1:
            value = f"0{value}"

        print(f"converted item value: {value}")

        output += list(char_values.keys())[list(char_values.values()).index(value)]

    print(f"output: {output}\n")

    return output



def encrypt_redundancy_value(password: str, completed: int):

    print('\nencrypting redundancy value...')

    print(f"password input: {password}\ncompletion input: {completed}")

    password_int = string_to_int(password)

    print(f"integer password: {password_int}")

    temp = []

    for element in password_int:
        temp.append(int(element, 16))

    sum = 0
    for num in temp:
        sum += num

    print(f"hexed & summed password: {sum}")

    base_value = completed + sum

    hex_value = hex(base_value)[2:]

    if len(hex_value) == 1:
        hex_value = f"0{hex_value}"

    print(f"hexed total sum: {hex_value}")

    int_value = string_to_int(hex_value)
    int_value = ('').join(int_value)
    final_value = binascii.unhexlify(int_value)

    print(f"final value: {final_value}")

    return final_value



def decrypt_redundancy_value(input: bytes):

    print('\ndecrypting redundancy value...')

    print(f"input: {input}")

    hexed_chars = str(binascii.hexlify(input))

    hexed_chars = hexed_chars[2:len(hexed_chars) - 1]

    print(f"hexed chars: {hexed_chars}")

    split_size = 2
    temp_list = []
    temp_str = ''

    for value in hexed_chars:
        temp_str += str(value)
        if len(temp_str) == split_size:
            temp_list.append(temp_str)
            temp_str = ''

    print(f"split chars: {temp_list}")

    output = ''

    for value in temp_list:

        output += list(char_values.keys())[list(char_values.values()).index(value)]

    output = int(output, 16)

    print(f"final value: {output}")

    return output