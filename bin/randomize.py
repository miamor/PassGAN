import random
import sys

if len(sys.argv) == 2:
    dataset = sys.argv[1]
else:
    dataset = 'rockyou'

with open('data/'+dataset+'-full.txt', 'r') as f:
    lines = f.readlines()
    random.shuffle(lines)
