import numpy as np
from matplotlib.pyplot import imread
from heapq import heappush, heappop, heapify
from collections import defaultdict
from bitarray import bitarray


print('Type I for image file compression or T for Text file ')
op= input('Enter your choice: ').lower()
if op=='i':
    print('******************************Image file compression******************************')
    input_img = imread('sample_img.jpg') # Read img
    # convert img into gray scale to calculate intensity of pixes
    scale_gray = np.rint(input_img[:,:,0]*0.2989 + input_img[:,:,1]*0.5870 + input_img[:,:,2]*0.1140).astype(int)
    histogram_img = np.bincount(scale_gray.ravel(),minlength=256) # generate histogram from array of gray scale for img
    input_gen=histogram_img
elif op=='t':
    print('******************************Text file compression******************************')
    txt='BCAADDDCCACACACAAAAAAABBCDAAADDBCCCCCCCCAADDD' # sample text to verify huffman codding algo.
    #txt=open('sample_text.txt','r').read()
    input_gen=txt.lower()
    
else:
    assert 1==0, 'Please enter valid input.'

dict_char = defaultdict(int) # gereate dictionary for occurance of each chars and symbols
for ch in input_gen:
    dict_char[ch] += 1
print('Frequency of each character in given input is: ')
print(dict_char)

li_heap = [[co, [ch, ""]] for ch, co in dict_char.items()]   #create huffman tree
heapify(li_heap) 
#print(li_heap)
while len(li_heap) > 1:
    leaf_lo = heappop(li_heap)    # get left most node
    leaf_hi = heappop(li_heap)    # get second left most node
    
    for i in leaf_lo[1:]:      # add 0 to all leftmost node
        i[1] = '0' + i[1]
    for j in leaf_hi[1:]:      # add 1 to all second leftmost node
        j[1] = '1' + j[1]
    heappush(li_heap, [leaf_lo[0] + leaf_hi[0]] + leaf_lo[1:] + leaf_hi[1:])  # pust new parent node to tree 
huffman_tree= sorted(heappop(li_heap)[1:], key=lambda p: (len(p[-1]), p))  #return sorted tree

#print(huff_tree)

huffman_dict = {a[0]:str(a[1]) for a in huffman_tree}
print('Dictionary for huffman codes is: ')
print(str(huffman_dict).replace(', ',',\n '))
f = open("huffman_dict.txt","w") # write huffman codes to file for decryption
f.write( str(huffman_dict) )
f.close()

output_sequence=''
for i in input_gen: # map char/symb with iput array and generate output sequence
    for b in huffman_tree:
        if(b[0]==i):
            output_sequence+=str(b[1])
extra_pad= 8 - (len(output_sequence) % 8) # Add exra bits if output sequence length in not in multiple of 8(1byte=8bit)
for i in range(extra_pad):
    output_sequence += "0"

output_sequence=bitarray(output_sequence) # transfor output sequence into bit array to write it in bit format
print('Length of output sequence is: ',len(output_sequence))
#print(output_sequence)
with open('output_file.txt', 'wb') as w:  # write output sequence to file
    output_sequence.tofile(w)


    
print('*******************************Huffman compression is successfully done*******************************')

