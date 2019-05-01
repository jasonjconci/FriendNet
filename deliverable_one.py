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
# Since we are taking Networking right now, we've decided to go with
# Dijkstra for the friendliest-path algorithm. We originally wanted to go with A*, but being
# that we can't come up with an admissable distance heuristic, we're deciding to go with
# old fashioned Dijkstra. Makes sense since each "node" knows the costs of every other "edge",
# and the only thing we've really got to change up is the fact that we'll be taking maxes,
# rather than mins.
# 
# We, initially, think that our two killer features will be as follows.
# 1.Best Friends Dashboard
#       This feature is intended to tell you who your best friends are, by examining all those
#   people that you're friends with, and finding those with the highest reciprocated friendship
#   rating. This feature is makes sense logically, is simple to implement, and frankly, is
#   missing from modern social media. We want to show you where your strongest connections are.
#       Going off of this, we'll also show you what percentage of your friends reciprocate your
#   friendship scores, within a threshhold that the user defines. For example, we'll show you how
#   many of your friends reciprocate your own friendship score within 2 points.
# 2.Suggested Friends
#       This feature will be our entire-graph-searching feature. With this feature, you'll be able
#   to see who you'd likely be good friends with, based on average scores on friendliest chains.
#   Basically, we'll traverse the entire network, and see what people are along some of the
#   friendliest chains that lead back to you, and show you those you aren't already friends with.
#       This will involve some sort of Dijkstra-ish graph traversal, but we're not yet sure how we'll
#   deal with scoring things (example: Someone 2 hops away with an average of 8, shouldn't
#   necessarily be suggested more highly than someone 5 hops away with an average of 7.5. 


from friendship import Friendship
import dijkstra as dj
import gameify as game
import recommend_friends as recommend
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


def print_friendlist_path(reverse_path, costs):
    if reverse_path != None and costs != None and reverse_path != [] and costs != []:
        i = 0
        print('\t', end = '')
        while i < len(reverse_path)-1:
            print(reverse_path[-i-1], end = ' ')
            print(' -> ', end = ' ')
            i+=1
        print(reverse_path[0])
        print("\tTOTAL FRIENDLINESS: ", sum(costs))
        print("\tAVG FRIENDLINESS: ", sum(costs) / len(costs))
    else:
        print("\tNo path could be found :(")

#### PORTION FOR PROGRAM DRIVER FUNCTIONS ####

# Function to serve as out command line interface for the time being, a sort of homemade
# do-while loop to get user input and feed back appropriate requested data
def command_line_interface(friendship_list):
    print("What would you like to do?")
    print("1. Check if user exists ")
    print("2. Check friendship weight between users")
    print("3. Find friendliest path between users")
    print("4. Find a best-friend dashboard")
    print("5. Find a user's recommended friends")
    print("Other. Quit")
    answer = input("> ")
    while "1" <= answer <= "5":
        if answer == "1":
            username = input("\tWhich user? ")
            print( "\tUser exists" if does_user_exist(username, friendship_list) else "\tUser does not exist")
        elif answer == "2":
            user_one, user_two = tuple(input("\tEnter usernames separated by spaces: ").split())
            weight = get_friendship_weight(user_one, user_two, friendship_list)
            print( "\tFriendship weight is " + str(weight) if weight > -1 else "\tFriendship does not exist")
        elif answer == "3":
            user_one, user_two = tuple(input('\tEnter usernames separated by spaces:').split())
            reverse_path, costs = dj.main(friendship_list, user_one, user_two)
            print_friendlist_path(reverse_path, costs)
        elif answer == "4":
            username = input('\tEnter username whose dashboard you want to see: ')
            highest_reciprocated, percentage_reciprocated = game.main(username, friendship_list)
            print("\tYour highest reciprocated friends are:")
            for i in range(len(highest_reciprocated)):
                print('\t\t' + str(i+1) + '. ' + highest_reciprocated[i].friend_a)
            print("\tYour reciprocation percentage: %.0f%%" % (percentage_reciprocated * 100))
        else:
            username = input('\tEnter username whose dashboard you want to see: ')
            valid = recommend.main(friendship_list, username)
            for i in range(len(valid)):
                print('\t\t' + str(i+1) + ". " + valid[i][0] + ", Estimated friendship Weight: %.1f" % (valid[i][1]/float(valid[i][2])))
        print()
        print("What would you like to do?")
        print("1. Check if user exists ")
        print("2. Check friendship weight between users")
        print("3. Find friendliest path between users")
        print("4. Find a best-friend dashboard")
        print("5. Find a user's recommended friends")
        print("Other. Quit")
        answer = input("> ")


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

