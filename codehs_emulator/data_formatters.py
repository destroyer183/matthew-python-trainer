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

    # print out data
    print(f"\nconverting byte to string...")
    print(f"input: {input}")

    # convert the byte input to integers
    input = binascii.hexlify(input)

    # convert the input to a string and remove any leading or trailiing whitespace
    input = str(input).strip()

    # remove any leading characters that are unnecessary
    input = input[2:len(input) - 1]

    # make temporary list and string
    temp_list = []
    temp_str = ''

    # strip any whitespace
    input = input.strip()

    # define the size of each section that the input will be split into
    split_size = 2

    # loop over the input by each character
    for value in input:

        # add character to the temporary string
        temp_str += value

        # check if the string is the size of the split size
        if len(temp_str) == split_size:

            # skip current loop if the hex representation of a '\n' is found
            if temp_str == '0a':
                continue

            # add the temp string to the temp list
            temp_list.append(str(temp_str))

            # clear temp string
            temp_str = ''

            # print out data
            print(f"value: {str(temp_str)}, {temp_str}")

    # make empty output string
    output = ''

    # print data
    print(f"temp_list: {temp_list}\n")

    # loop over every element in the temp list
    for value in temp_list:

        # convert the value to hexidecimal and remove extra characters
        value = hex(int(value))[2:]

        # make sure that the value is at least 2 characters long
        if len(value) == 1:
            value = f"0{value}"

        # print out data
        print(f"converted item value: {value}")

        # search through the 'char_values' dictionary by value, and add the cooresponding key to the output
        output += list(char_values.keys())[list(char_values.values()).index(value)]

    # print out output
    print(f"output: {output}\n")

    # return output
    return output


# function to encrypt the data that represents the redundancy bytes at the end of the save file
def encrypt_redundancy_value(password: str, completed: int):

    # print out data
    print('\nencrypting redundancy value...')
    print(f"password input: {password}\ncompletion input: {completed}")

    # convert the password to integers
    password_int = string_to_int(password)

    # print out data
    print(f"integer password: {password_int}")

    # create temprorary list
    temp = []

    # pretend every integer is a hexidecimal number, and convert it back to an integer number before adding it to the temp list
    for element in password_int:
        temp.append(int(element, 16))

    # sum the integers and store them in a variable
    sum = 0
    for num in temp:
        sum += num

    # print out data
    print(f"hexed & summed password: {sum}")

    # sum the amount of completed questions and the password sum
    base_value = completed + sum

    # convert the base value to hexidecmial and remove any leading characters that might be unnecessary
    hex_value = hex(base_value)[2:]

    # make sure that the hex value is at least two characters long
    if len(hex_value) == 1:
        hex_value = f"0{hex_value}"

    # print out data
    print(f"hexed total sum: {hex_value}")

    # conver the individual numbers to a list of integers
    int_value = string_to_int(hex_value)

    # combine the list into a string
    int_value = ('').join(int_value)

    # convert the string to bytes
    final_value = binascii.unhexlify(int_value)

    # print out data
    print(f"final value: {final_value}")

    # return output
    return final_value



# function to decrypt the redundancy bytes at the end of the save file
def decrypt_redundancy_value(input: bytes):

    # print out data
    print('\ndecrypting redundancy value...')
    print(f"input: {input}")

    # convert the bytes back to a string of integers
    hexed_chars = str(binascii.hexlify(input))

    # remove any leading characters that are unnecessary
    hexed_chars = hexed_chars[2:len(hexed_chars) - 1]

    # print out data
    print(f"hexed chars: {hexed_chars}")

    # define the length of each section that the characters will be split into
    split_size = 2

    # make temp list and string1
    temp_list = []
    temp_str = ''

    # loop over every value
    for value in hexed_chars:

        # add the value to the temp string
        temp_str += str(value)

        # check if the temp string is the size of the split size
        if len(temp_str) == split_size:

            # add the temp string to the temp list
            temp_list.append(temp_str)

            # clear the temp string
            temp_str = ''

    # print out data
    print(f"split chars: {temp_list}")

    # make empty string for output
    output = ''

    # loop over every value in temp list
    for value in temp_list:

        # search through the 'char_values' dictionary by value, and return the cooresponding key
        output += list(char_values.keys())[list(char_values.values()).index(value)]

    # pretend the integer output is hexidecimal and convert it back to an integer value
    output = int(output, 16)

    # print out data
    print(f"final value: {output}")

    # return output
    return output