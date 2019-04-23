# Placeholder comment

from friendship import Friendship

def setup_matrix(person_list, friends_list, source):
    matrix = {i: 0 for i in person_list}
    assert source in person_list, "Nonexistent person in the network!"
    del matrix[source]
    S = [ source ]
    for person in person_list:
        if person == source:
            continue
        weight = get_friendship_weight(source, person, friends_list)
        # if the friendship exists,
        if weight != None:
            matrix[person] = (weight, source)
        # Else, initialize to infinity, since there's no route
        else:
            # Silly me was wondering why my program was breaking. it's -inf
            matrix[person] = (float('-inf'), '\0')
    return source, matrix, S

def algorithm(matrix, S, person_list, friends_list):
    while(len(S) != len(person_list)):
        # This is the part where we set our costs
        max_val = max((i for i in matrix.items() if i[0] not in S), key = lambda t: t[1][0])
        S.append(max_val[0])
        # This is the part where we recalculate costs
        # Loop over all destinations
        for dest in person_list:
            # If it's a destination we haven't used yet
            if dest not in S:
                # if source -> dest is a valid path, add it as an option for dest
                options = []
                for source in S:
                    weight = get_friendship_weight(source, dest, friends_list)
                    if weight != None:
                        options.append((weight, source))
                # If we've got any options, set it to the lowest cost one
                if options:
                    matrix[dest] = max(options, key = lambda t: t[0])
    return matrix, S
    

def backtrack(matrix, S, source, dest, friends_list):
    # I'm reversing because I personally like it better
    reversed = [S[-i-1] for i in range(len(S))]
    for node in reversed:
        # If we're on the node which is our destination,
        if node == dest:
            try:
                # Do some setup work to keep track of our backtracking
                reverse_chain = []
                costs = []
                # Immediately set the reverse chain and cost-to-node for dest
                curr_node = node
                reverse_chain.append(curr_node)
                weight = get_friendship_weight(matrix[curr_node][1], curr_node, friends_list)
                costs.append(weight)
                while matrix[curr_node][1] != source:
                    curr_node = matrix[curr_node][1]
                    reverse_chain.append(curr_node)
                    weight = get_friendship_weight(matrix[curr_node][1], curr_node, friends_list)
                    costs.append(weight)
                reverse_chain.append(source)
            except:
                reverse_chain = None
                costs = None
    return reverse_chain, costs
    


def get_friendship_weight(friend_a, friend_b, friends_list):
    for each in friends_list:
        if friend_a == each.friend_a and friend_b == each.friend_b:
            return each.weight
    return None

def decompress_friends(friends_list):
    friend_list_a = [i.friend_a for i in friends_list]
    friend_list_a_set = set(friend_list_a)
    friend_list_b_set = set([i.friend_b for i in friends_list])
    # remove friends in a but not in b
    difference = friend_list_b_set - friend_list_a_set
    all_friends = friend_list_a + list(difference)
    return all_friends

def main(friends_list, source, dest):
    person_list = decompress_friends(friends_list)
    source, matrix, S = setup_matrix(person_list, friends_list, source)
    matrix, S = algorithm(matrix, S, person_list, friends_list)
    reverse_chain, weights = backtrack(matrix, S, source, dest, friends_list)
    return reverse_chain, weights