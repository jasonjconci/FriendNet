# Placeholder comment

class Friendship:
    friend_a = ""
    friend_b = ""
    weight = 0
    def __init__(self, friend_a, friend_b, weight):
        self.friend_a = friend_a
        self.friend_b = friend_b
        self.weight = weight
    
    def __eq__(self, other):
        return self.friend_a == other.friend_a and self.friend_b == other.friend_b
    
    def __str__(self):
        return "Friendship from " + self.friend_a + " to " + self.friend_b + " with weight " + str(self.weight)