import os
import sys

current = os.path.dirname(os.path.realpath(__file__)) # get current directory - Basics
parent = os.path.dirname(current) # go up one directory level - Introduction
parent = os.path.dirname(parent) # go up another directory level - user_code
parent = os.path.dirname(parent) # go up another directory level - account_template
parent = os.path.dirname(parent) # go up another directory level - accounts
parent = os.path.dirname(parent) # go up another directory level - gui_code
parent = os.path.dirname(parent) # go up another directory level - codehs_python_practice_problems
sys.path.append(parent) # set current directory
import question_tester


'''

question description goes here

'''


def main_function(argument):

    return argument













# don't touch this stuff, it'll break lots of otehr things if you change this code

def main():

    quote_placeholder = '\"'

    # have 3 test cases
    input1 = 'something1'
    output1 = main_function(input1)
    answer1 = 'something3'

    print(f"\nTest case 1: {('Success!' * (output1 == answer1) + 'Failed.' * (output1 != answer1))}\
          \nYour output: {quote_placeholder * (type(output1) == str)}{output1}{quote_placeholder * (type(output1) == str)}\
          \nExpected output: {answer1}\n")


    input2 = 'something2'
    output2 = main_function(input2)
    answer2 = 'something2'

    print(f"\nTest case 1: {('Success!' * (output2 == answer2) + 'Failed.' * (output2 != answer2))}\
          \nYour output: {quote_placeholder * (type(output2) == str)}{output2}{quote_placeholder * (type(output2) == str)}\
          \nExpected output: {answer2}\n")
    

    input3 = 'something3'
    output3 = main_function(input3)
    answer3 = 'something1'

    print(f"\nTest case 1: {('Success!' * (output3 == answer3) + 'Failed.' * (output3 != answer3))}\
          \nYour output: {quote_placeholder * (type(output3) == str)}{output3}{quote_placeholder * (type(output3) == str)}\
          \nExpected output: {answer3}\n")



    # have 5 separate cases stored in an encoded file, use these cases for verification that the question was solved legitimately



    pass



if __name__ == '__main__':
    main()