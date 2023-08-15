from collections import defaultdict
import heapq


## Build Frequency Tables
def build_frequency(text):
    frequency_table = defaultdict(int)
    for char in text:
        frequency_table[char] += 1
    return frequency_table

### Node class for Huffman Tree
class Node:
    def __init__(self, char=None, frequency = 0):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self,other):
        return self.frequency < other.frequency

## build huffman tree from text input using Node class
def build_huffman_tree(frequency_table):
    construction_queue = []
    
    ## Insert all Nodes of Character and Frequency onto construction queue
    for char, frequency in frequency_table.items():
        node = Node(char,frequency)
        heapq.heappush(construction_queue, node)

    ##Remove Nodes from Construction queue and construct the Tree, adding internal node until 1 node remains
    while len(construction_queue) > 1:
        ##Remove the 2 smallest Nodes
        left_node = heapq.heappop(construction_queue)
        right_node = heapq.heappop(construction_queue)

        ##Create a Parent node of the 2 smallest
        parent_node = Node(frequency=left_node.frequency + right_node.frequency)
        parent_node.left = left_node
        parent_node.right = right_node

        ##Insert Parent onto Construction Queue
        heapq.heappush(construction_queue,parent_node)
    
    ##Return Root Node of tree
    return construction_queue[0]

## Build Code to Char Table
def build_code_char_table(root):
    codechar_table = {}
    ##Traverse Tree if goes Left add 0, if right add 1
    def traverse_tree(node, code):
        if node.char:
            codechar_table[node.char] = code
        else:
            traverse_tree(node.left, code + '0')
            traverse_tree(node.right, code + '1')
    
    traverse_tree(root,'')
    return codechar_table

## Full Compression Operations --------------------
## Convert frequency table to binary
def compress_frequency_table(frequency_table):
    length = len(bin(max(frequency_table.values()))[2:])
    result = '' + ('1' * length) + ('0' * length)    
    for key in frequency_table:
        binaryKey = bin(ord(key))[2:].zfill(8)
        binaryNum = format(frequency_table[key], '0{}b'.format(length))
        result += binaryNum + binaryKey
    result += ('0' * length) + '00110000' 
    return result

## Convert binary to frequency table 
def decompress_frequency_table(data):
    length = 0
    for digit in data:
        if digit == '1':
            length += 1
        else:
            break
    frequency_table = {}
    binary = data[2*length:]
    while True:
        entry = binary[:length + 8]
        number = int(entry[:length], 2)
        letter = chr(int(entry[length:], 2))
        binary = binary[length + 8:]
        if number == 0 and letter == '0':
            break
        else:
            frequency_table[letter] = int(number)
    return frequency_table,binary


def is_ascii(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    return True

def ensure_ascii(s):
    if is_ascii(s):
        return s
    else:
        return s.encode('ascii', 'ignore').decode('ascii')

###Compress Operations--------------------------------
def compress(text):
    ## Build Required Frequency table, Huffman tree and Code Char table
    frequency_table = build_frequency(text)
    huffman_tree = build_huffman_tree(frequency_table)
    codechar_table = build_code_char_table(huffman_tree)

    ##code chars to binary code
    result = ''
    for char in text:
        result += codechar_table[char]

    return result,huffman_tree

def compress_alldata(text):
    ## Build Required Frequency table, Huffman tree and Code Char table
    #text = ensure_ascii(text)
    frequency_table = build_frequency(text)
    print(frequency_table)
    huffman_tree = build_huffman_tree(frequency_table)
    codechar_table = build_code_char_table(huffman_tree)
    
    result = compress_frequency_table(frequency_table)
    for char in text:
        result += codechar_table[char]
    return result



def decompress(data, huffman_tree):
    result = ''
    curr_node = huffman_tree

    ##Loop over bitstream, traverse tree until char found, reset traversal
    for bit in data:
        ##Select Left or Right Travel
        if bit == '0':
            curr_node = curr_node.left
        else:
            curr_node = curr_node.right

        ##Write Found Node to result and reset
        if curr_node.char:
            result += curr_node.char
            curr_node = huffman_tree

    return result

###Decompress Operation----------------------
def decompress_all(data):
    frequency_table, binary = decompress_frequency_table(data)
    huffman_tree = build_huffman_tree(frequency_table)
    return decompress(binary, huffman_tree)

def string_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_string(binary):
    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        decimal_value = int(byte, 2)
        character = chr(decimal_value)
        text += character
    return text





# text_file = "Romeo&Juliet.txt"
# text_file = "msg.txt"

# with open(text_file, 'r') as file:
#     text = file.read

# print(text)
# compressed_data = compress_alldata(text)
# decompressed_data = decompress_all(compressed_data)

# print(decompressed_data)

text_file = "Romeo&Juliet.txt"

#Open Text File and Get string
with open(text_file, 'r') as file:
    text = file.read()

#text = "Hello World"
#print(text)
#compressed_data,tree = compress(text)

#decompressed_data = decompress(compressed_data,tree)

compressed_data = compress_alldata(text)
decompressed_data = decompress_all(compressed_data)
print(compressed_data)
print(decompressed_data)

with open('result.txt', 'w') as file:
    file.write(compressed_data + '\n' + decompressed_data)

text_bitlength = len(string_to_binary(text))
compressed_bitlength = len(compressed_data)
print('The Original Text was ' + str(text_bitlength) + ' bits, The compressed Size was ' + str(compressed_bitlength))

print('The size is ' + str((compressed_bitlength)/text_bitlength) + '  the original size')