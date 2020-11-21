# Program Name: testing
# Description: Tests potential code

#INIT#
#objects#
class Object():
    def __init__(self, attributes):
        for attribute in attributes:
            value = attribute.assignment()
            attribute.declaration(self, value)

class Attribute():
    def __init__(self, declaration, assignment):
        self.declaration = declaration
        self.assignment = assignment

#MAIN#
if __name__ == '__main__':
    #testing#
    class Test:
        def __init__(self, str, l1, l2=[]):
            for int in l1:
                print(int)
    list = [1, 2, 3]
    Test('str', list, [4, 5])

# Author: Jack Paul Martin
# Start: 11/20/2020, Completion: