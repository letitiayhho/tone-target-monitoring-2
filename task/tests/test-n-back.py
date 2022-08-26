import random
LETTERS = ['a', 'b', 'c']

force = False
one_back = 0
two_back = 0
for a in range(100):
    if not force:
        i = random.randint(0, len(LETTERS)-1)
    LET = LETTERS[i]
    print(LET)
    
    if LET == one_back == two_back:
        print(f"LET: {LET}, one_back: {one_back}, two_back: {two_back}")
        force = True
        drop = LETTERS.index(LET)
        indexes = [0, 1, 2]
        indexes.pop(drop)
        i = random.choice(indexes)
    else:
        force = False

#     three_back = two_back
    two_back = one_back
    one_back = LET
