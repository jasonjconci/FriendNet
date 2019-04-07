# Placeholder comment
# Instructions to run:
#   Run script at command line as:
#       $ python3 deliverable_one.py matrix_filename debug_flag
#   matrix_filename (I've provided matrix.txt and matrix_new.txt) is not optional
#   debug_flag (0/1) is optional, debug flag defaults to False if no value present.
from friendship import Friendship
import sys

DEBUG = False

# Function to read in a file of friendships (file in format as defined in class), and
# place these friendships in a list of Friendship objects (as defined in friendship.py)
# I've opted for the Object route bc it makes sorting, existence, etc prettier (no lambdas)
def read_matrix_to_list(infile):
    friendship_list = []
    opened = open(infile, 'r')
    for line in opened.readlines():
        splitted = line.split()
        friendship_list.append(Friendship(splitted[0], splitted[1], splitted[2]))
    return friendship_list

# Function to determine if a friendship exists within our list of friends
def does_friendship_exist(friend_a, friend_b, friendship_list):
    return Friendship(friend_a, friend_b, -1) in friendship_list

# Using any here since it returns early if possible
def does_user_exist(user, friendship_list):
    return any(x.friend_a == user or x.friend_b == user for x in friendship_list)

# Main function
def main(infile):
    friendship_list = read_matrix_to_list(infile)
    # If DEBUG flag, print all friendships in Friendship list and check if a few friendships exist
    if DEBUG:
        for each in friendship_list:
            print(each)
        print(does_friendship_exist("Jason", "Depalma", friendship_list))
        print(does_friendship_exist("Jacob", "Emily", friendship_list))


if __name__ == "__main__":
    assert len(sys.argv) > 1, "Need input matrix filename (matrix.txt for example)"
    if len(sys.argv) == 3:
        DEBUG = True if int(sys.argv[2]) == 1 else False
    main(str(sys.argv[1]))

