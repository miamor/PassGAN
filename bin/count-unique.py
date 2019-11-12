import sys
from collections import Counter
import operator
import collections
import csv

'''
 Count all unique passwords 
'''

if len(sys.argv) == 2:
    dataset = sys.argv[1]
else:
    dataset = 'rockyou'

# with open('data/'+dataset+'_train.txt', 'r') as f:
#     train_set = f.read().splitlines()

with open('data/'+dataset+'_test.txt', 'r') as f:
    test_set = f.read().splitlines()


# freq_train_set = Counter(train_set)
freq_test_set = Counter(test_set)

# freq_train_set = collections.OrderedDict(sorted(freq_train_set.items(), key=operator.itemgetter(1)))
freq_test_set = collections.OrderedDict(sorted(freq_test_set.items(), key=operator.itemgetter(1)))

unique = []
for key in freq_test_set.keys():
    # if not key in freq_train_set:
    #     unique.append(key)
    unique.append(key)

with open('data/'+dataset+'_unique.txt', 'w') as f:
    # f.write('\n'.join(unique))
    for pw in unique:
        for i in range(freq_test_set[pw]):
            f.write(pw+'\n')

with open('data/'+dataset+'_unique_withcount.csv', 'w') as f:
    fieldnames = ['password', 'fq_in_test']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()

    for pw in unique:
        w.writerow({'password':pw, 'fq_in_test':freq_test_set[pw]})
