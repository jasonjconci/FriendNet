# Friendship Class, defined in another file because it makes sense.
# Takes in, as parameters:
#   - String "friend a" (source node)
#   - String "friend b" (dest node)
#   - Integer "weight" (friendship weight from a -> b)

class Friendship:
    friend_a = ""
    friend_b = ""
    weight = 0
    def __init__(self, friend_a, friend_b, weight):
        self.friend_a = str(friend_a)
        self.friend_b = str(friend_b)
        try:
            self.weight = int(weight)
            if weight > 10:
                weight = 10
            if weight < 0:
                weight = 0
        except ValueError:
            print("Weight isn't an integer. Setting weight to -1.")
            self.weight = -1
        except Exception:
            print("Something else happened converting weight to int. Setting weight to -1.")
            self.weight = -1
    
    def __eq__(self, other):
        return self.friend_a == other.friend_a and self.friend_b == other.friend_b
    
    def __gt__(self, other):
        if self.weight > other.weight:
            return True
        return False
    
    def __lt__(self, other):
        if self.weight < other.weight:
            return True
        return False

    def __str__(self):
        return "Friendship from " + self.friend_a + " to " + self.friend_b + " with weight " + str(self.weight)

        