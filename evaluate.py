import sys
from collections import Counter
import operator
import collections
import csv
import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', '-d',
                        required=True,
                        default='rockyou')

    parser.add_argument('--generated-file', '-g',
                        required=True,
                        default='generated/gen_passwords.txt')
    
    args = parser.parse_args()

    return args


args = parse_args()
prefix = args.generated_file.split('/')[-1].split('.txt')[0]

# get all generated passwords
with open(args.generated_file, 'r') as f:
    gen_set = f.read().splitlines()

# freq_gen_set = dict((x, gen_set.count(x)) for x in set(gen_set))
freq_gen_set = Counter(gen_set)
freq_gen_set = collections.OrderedDict(
    sorted(freq_gen_set.items(), key=operator.itemgetter(1)))
keys_gen = set(freq_gen_set.keys())

''' 
Compare and statistics frequency of generated password with full dataset
by Union 2 set of paswords and get frequency from each set and save to file
'''
# get all the passwords
with open('data/'+args.dataset+'.txt', 'r') as f:
    full_set = f.read().splitlines()


# print(full_set)
freq_full_set = Counter(full_set)
# print(freq_full_set)

freq_full_set = collections.OrderedDict(
    sorted(freq_full_set.items(), key=operator.itemgetter(1)))

keys_full = set(freq_full_set.keys())

# Union 2 set of paswords and get frequency from each set and save to file
union_passwords = keys_full | keys_gen

match_full = 0
with open('evaluate/'+prefix+'__'+args.dataset+'__full.csv', 'w') as csv_file:
    fieldnames = ['password', 'fq_in_full', 'fq_in_gen']
    w = csv.DictWriter(csv_file, fieldnames=fieldnames)
    w.writeheader()

    for pw in union_passwords:
        # frequency of this password in full set
        fq_in_full = 0 if not pw in freq_full_set else freq_full_set[pw]
        # frequency of this password in gen set
        fq_in_gen = 0 if not pw in freq_gen_set else freq_gen_set[pw]

        w.writerow({'password':pw, 'fq_in_full':fq_in_full, 'fq_in_gen':fq_in_gen})

        if fq_in_full > 0 and fq_in_gen > 0:
            match_full += 1

# print('Match with original dataset: {}/{} = {}%'.format(match_full, len(keys_full), float(match_full/len(keys_full))*100))
print('Match with original dataset: %d/%d = %.5f' % (match_full, len(keys_full), float(match_full)/float(len(keys_full))))


''' 
Match unique passwords 
'''
# get unique passwords
with open('data/'+args.dataset+'_unique.txt', 'r') as f:
    unique_set = f.read().splitlines()

freq_unique_set = Counter(unique_set)
keys_unique = set(freq_unique_set.keys())

match_unique = 0
with open('evaluate/'+prefix+'__'+args.dataset+'__unique.csv', 'w') as csv_file:
    fieldnames = ['password', 'fq_in_unique', 'fq_in_gen']
    w = csv.DictWriter(csv_file, fieldnames=fieldnames)
    w.writeheader()

    for pw in keys_unique:
        # frequency of this password in full set
        fq_in_unique = 0 if not pw in freq_unique_set else freq_unique_set[pw]
        # frequency of this password in gen set
        fq_in_gen = 0 if not pw in freq_gen_set else freq_gen_set[pw]

        w.writerow({'password':pw, 'fq_in_unique':fq_in_unique, 'fq_in_gen':fq_in_gen})

        if fq_in_gen > 0:
            match_unique += 1

print('Unique match: %d/%d = %.5f' % (match_unique, len(keys_unique), float(match_unique)/float(len(keys_unique))))
