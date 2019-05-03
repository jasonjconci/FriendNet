# This program is meant to be used in conjuction with deliverable_one.py, found
# within this repository.
# 
# This program takes in a list of Friendship objects (found in friendship.py),
# as well as the name of a user who has listed a friendship with another person.
# This program will recommend friends to that input user who they aren't already
# friends with, based on a calculated average-friendship-weight along the path
# from input user to a recommended friend. Traversal of this graph is performed
# with a sort of depth first search, with a depth bound of 2-3, for the sake of
# keeping both runtimes and potential friendships feasible.


from collections import deque

# Simple function for generating neighbors of a particular node.
# In regular terms, get all the friendships a particular user has listed.
def get_friends_of_user(friendship_list, username):
    return [i for i in friendship_list if i.friend_a == username]

def bfs(friendship_list, user, DEPTH_BOUND = 3):
    # Not visited and visited stacks, running in parallel
    not_visited = []
    visited = []
    valid_endpoints = []
    CURR_DEPTH = 0
    not_visited.append([user, 0, CURR_DEPTH])
    # While we've still got nodes to explore,
    while len(not_visited) > 0:
        # Dequeue the leaading node
        curr_node = not_visited.pop(0)
        # If we aren't at our depth bound,
        if curr_node[2] < DEPTH_BOUND:
            # Append non-visited neighbors of current node
            neighbors = get_friends_of_user(friendship_list, curr_node[0])
            for item in neighbors:
                # If this item has not been visited,
                if not [i for i in visited if i[0] == item.friend_a]:
                    # Append to visited: [person's name, previous_friendship_weight + curr_friendship_weight, new_depth]
                    not_visited.append([item.friend_b, item.weight + curr_node[1], curr_node[2] + 1])
        # Otherwise, this is a valid path, and we append it to the valid_endpoints list
        else:
            valid_endpoints.append(curr_node)
        # Add curr_node to visited stack so we don't hit it again
        visited.append(curr_node)


    # Only allow those friendships that don't already exist
    user_friends = [i.friend_b for i in get_friends_of_user(friendship_list, user)]
    valid_endpoints_filtered = [i for i in valid_endpoints if i not in user_friends]

    # Sort the friends we want to show, from highest average weight on path to lowest
    valid_endpoints_sorted = list(reversed(sorted(valid_endpoints_filtered, key = lambda t: (t[1]/float(t[2])))))

    # We remove duplicates here - BUT, we sort first, to ensure we're always getting max path weight
    already_gotten = set()
    valid_endpoints_remove_dupes = []
    for item in valid_endpoints_sorted:
        if item[0] not in already_gotten:
            already_gotten.add(item[0])
            valid_endpoints_remove_dupes.append( tuple(item))

    # Only return the top 5 recommended friends
    # We do this here to ensure highest weight, no dupes, etc
    return valid_endpoints_remove_dupes[:5]


def main(friendship_list, user):
    assert get_friends_of_user(friendship_list, user), "Invalid user"
    valid = bfs(friendship_list, user, DEPTH_BOUND=3)
    return valid


            


