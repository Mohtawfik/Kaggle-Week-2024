"""
Team 8 - Shadowfax

Mohammed Tawfik Sadhik Batcha
Huzaifa Mehmood
Karthikaijothi Murugan
Thamjeed Abdulla Kuniyil

"""

import time
from KCW_Team_8 import main

def KCW_final_score(input_file_path):

    res = 0

    isExample = False
    isBinary = False
    isComputable = False
    isRandom = False
    isOily = False

    if input_file_path == '0_example.txt':
        isExample = True
    elif input_file_path == '1_binary_landscapes.txt':
        isBinary = True
    elif input_file_path == '10_computable_moments.txt':
        isComputable = True
    elif input_file_path == '11_randomizing_paintings.txt':
        isRandom = True
    elif input_file_path == '110_oily_portraits.txt':
        isOily = True
    else:
        raise Exception('Error:', 'Invalid input file')
    res = main(input_file_path, isBinary, isOily, isRandom, isComputable, isExample)
    print(input_file_path, res)
    return res

import os 

start = time.time()

total = 0
for file in os.listdir('Data'):
    if file.endswith('.txt'):
        total += KCW_final_score(file)

print('Total time:', (time.time()-start) / 60, ' minutes')
print('Total score:', total)
