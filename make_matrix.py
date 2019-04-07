# Placeholder comment
# This program takes in a filename (presumably names.txt as I've defined it), and
# generates a "friend matrix" based on that file (mostly random for the time being).

import sys
import random


def read_infile_to_list(infile):
    opened = open(infile, 'r')
    name_list = []
    for line in opened.readlines():
        for i in line.split()[1:]:
            name_list.append(i.strip())
    return name_list

def get_random(lst):
    return lst[random.randrange(0, len(lst))]

def main(infile):
    name_list = read_infile_to_list(infile)
    outfile = open("matrix_new.txt", "w")
    # We're keeping track of already used pairs in list-of-tuple
    used_pairs = []
    for _ in range(len(name_list)*3):
        # Get random people
        friend_one = get_random(name_list)
        friend_two = get_random(name_list)
        # If the names are different and we haven't used the pair yet, add it
        if friend_one != friend_two and (friend_one, friend_two) not in used_pairs:
            used_pairs.append((friend_one, friend_two))
            friendship_weight = random.randrange(1, 11)
            outfile.write(friend_one + " " + friend_two + " " + str(friendship_weight) + '\n')
            # I'm choosing to give us a 50% chance that this friendship goes both ways. If generator is >50,
            # and the friendship weight > 3 (if 3 or below, friendship probably won't go both ways anyway), and
            # the friendship hasn't been added yet, add it to the list
            generator = random.randrange(0, 100)
            if generator > 50 and friendship_weight > 3 and (friend_two, friend_one) not in used_pairs:
                used_pairs.append((friend_two, friend_one))
                outfile.write(friend_two + " " + friend_one + " " + str(random.randrange(1, 11)) +'\n')
    outfile.close()
    print("Matrix generation complete!")

if __name__ == "__main__":
    assert (len(sys.argv) == 2), "Need a filename (names.txt)"
    infile = sys.argv[1]
    main(infile)