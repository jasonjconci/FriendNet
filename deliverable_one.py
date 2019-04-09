# Names: Jason Conci, Daniel Abrahms
# Date: 4/9/2019, T
# Class: CPSC450, Algorithms, Dr. Schroeder
# Assignment: FriendNet project, deliverable one
# Description: Initial progress implementation of FriendNet, namely user existence and
# friendship-weight functions, with appropriate errors, etc. Includes text-based menu system
# to use, per slides suggestions.
# 
# Instructions to run:
#   Run script at command line as:
#       $ python3 deliverable_one.py matrix_filename debug_flag
#   param: matrix_filename > not optional, we've provided matrix_one.txt to use.
#   param: debug_flag (0/1) > optional, debug flag defaults to False if no value present.
#
# ---- ANSWERS TO PATH TRAVERSAL + 2 KILLER FEATURES ----
#
# Since both Daniel and Jason are taking Networking right now, we've decided to go with
# Dijkstra for the friendliest-path algorithm. We originally wanted to go with A*, but being
# that we can't come up with an admissable distance heuristic, we're deciding to go with
# old fashioned Dijkstra. Makes sense since each "node" knows the costs of every other "edge",
# and the only thing we've really got to change up is the fact that we'll be taking maxes,
# rather than mins.
#
# We, initially, think that our two killer features will be as follows.
# 1.Best Friends
#   This feature is intended to tell you who your best friends are, by examining all those
#   people that you're friends with, and finding those with the highest reciprocated friendship
#   rating. This feature is makes sense logically, is simple to implement, and frankly, is
#   missing from modern social media. We want to show you where your strongest connections are.
# 2.Suggested Friends
#   This feature will be our entire-graph-searching feature. With this feature, you'll be able
#   to see who you'd likely be good friends with, based on average scores on friendliest chains.
#   Basically, we'll traverse the entire network, and see what people are along some of the
#   friendliest chains that lead back to you, and show you those you aren't already friends with.
#   
#   This will involve some sort of Dijkstra-ish graph traversal, but we're not yet sure how we'll
#   deal with scoring things (example: Someone 2 hops away with an average of 8, shouldn't
#   necessarily be suggested more highly than someone 5 hops away with an average of 7.5; averages
#   are hard to maintain over time, so we'll put some thought into this). Maybe we can have different
#   modes for finding friends - pure average, and "I really want to branch out to new groups" modes.

from friendship import Friendship
import sys

DEBUG = False


#### PORTION FOR EASY UTILITY FUNCTIONS ####

# Function to read in a file of friendships (file in format as defined in class), and
# place these friendships in a list of Friendship objects (as defined in friendship.py)
# I've opted for the Object route bc it makes sorting, existence, etc prettier (no lambdas)
def read_matrix_to_list(infile):
    friendship_list = []
    opened = open(infile, 'r')
    for line in opened.readlines():
        splitted = line.split()
        friendship_list.append(Friendship(str(splitted[0]), str(splitted[1]), int(splitted[2])))
    return friendship_list

# Function to determine if a friendship exists within our list of friends
def does_friendship_exist(friend_a, friend_b, friendship_list):
    return Friendship(friend_a, friend_b, -1) in friendship_list

# Using any here since it returns early if possible
def does_user_exist(user, friendship_list):
    return any(x.friend_a == user or x.friend_b == user for x in friendship_list)

# Function for getting a friendship's weight from the friendship list we've defined
# within this program. If exists, return weight. If doesn't exist, return -1, since
# we expect an integer, and the only allowable weights are 1-10.
def get_friendship_weight(friend_a, friend_b, friendship_list):
    if does_friendship_exist(friend_a, friend_b, friendship_list):
        index = friendship_list.index(Friendship(friend_a, friend_b, -1))
        return friendship_list[index].weight
    else:
        return -1

# Way overly simple debug prints function
def debug_prints(friendship_list):
    for each in friendship_list:
        print(each)
    print('\t CHECK FOR FRIENDSHIP EXISTS')
    print(does_friendship_exist("Jason", "Depalma", friendship_list))
    print(does_friendship_exist("Jacob", "Emily", friendship_list))
    print("\t CHECK FOR USER EXISTS")
    print(does_user_exist("Jason", friendship_list))
    print(does_user_exist("Depalma", friendship_list))
    print(does_user_exist("Louis", friendship_list))
    print(does_user_exist("Ella", friendship_list))
    print("\t CHECK FOR FRIENDSHIP WEIGHTS")
    print(get_friendship_weight("Jason", "Depalma", friendship_list))
    print(get_friendship_weight("Depalma", "Jason", friendship_list))



#### PORTION FOR PROGRAM DRIVER FUNCTIONS ####

# Function to serve as out command line interface for the time being, a sort of homemade
# do-while loop to get user input and feed back appropriate requested data
def command_line_interface(friendship_list):
    print("What would you like to do?")
    print("1. Check if user exists ")
    print("2. Check friendship weight between users")
    print("Other. Quit")
    answer = input("> ")
    while answer == "1" or answer == "2":
        if answer == "1":
            username = input("\tWhich user? ")
            print( "\tUser exists" if does_user_exist(username, friendship_list) else "\tUser does not exist")
        else:
            user_one, user_two = tuple(input("\tEnter usernames separated by spaces: ").split())
            weight = get_friendship_weight(user_one, user_two, friendship_list)
            print( "\tFriendship weight is " + str(weight) if weight > -1 else "\tFriendship does not exist")
        print()
        print("What would you like to do?")
        print("1. Check if user exists ")
        print("2. Check friendship weight between users")
        print("Other. Quit")
        answer = input(">")


# Main function
def main(infile):
    friendship_list = read_matrix_to_list(infile)
    # If DEBUG flag, print all friendships in Friendship list and check if a few friendships exist
    if DEBUG:
        debug_prints(friendship_list)
    command_line_interface(friendship_list)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "Need input matrix filename (matrix.txt for example)"
    if len(sys.argv) == 3:
        DEBUG = True if int(sys.argv[2]) == 1 else False
    main(str(sys.argv[1]))

