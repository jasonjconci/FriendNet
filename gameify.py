# Placeholder comment

import os
import sys
from friendship import Friendship


def highest_scoring(source, friendship_list):
    # Friendships where A is the source
    initial = [i for i in friendship_list if i.friend_a == source]
    eligible = []
    for each in initial:
        reversed = Friendship(each.friend_b, source, -1)
        try:
            ix = friendship_list.index(reversed)
            # The friendship is reciprocated; add the reciprocated friendship
            eligible.append(friendship_list[ix])
        except:
            # Do nothing, this means that the friendship isn't reciprocated
            pass
    highest_scoring = list(sorted(eligible, key = lambda t: t.weight, reverse=True))
    return highest_scoring[:5]

def percent_reciprocate(source, friendship_list):
    eligible = [i for i in friendship_list if i.friend_a == source]
    num_less = 0
    num_geq = 0
    # For each person in source's friend list,
    for friend in eligible:
        # get source -> dest friendship weight
        source_dest_weight = friend.weight
        try:
            # Try to get dest -> source friendship weight
            ix = friendship_list.index(Friendship(friend.friend_b, source, -1))
            dest_source_weight = friendship_list[ix].weight
            # Then increment the appropriate counter
            if dest_source_weight < source_dest_weight:
                num_less += 1
            else:
                num_geq += 1
        # If we get a valueError, couldn't find the index. As such, num_less +=1, 
        # since the friendship doesn't exist at all
        except ValueError:
            num_less += 1
    num_total = len(eligible)
    return num_geq, num_less, num_total

def main(user, friendship_list):
    x = 1
    highest_reciprocated = highest_scoring(user, friendship_list)
    num_geq, _, num_total = percent_reciprocate(user, friendship_list)
    return highest_reciprocated, (float(num_geq) / float(num_total))