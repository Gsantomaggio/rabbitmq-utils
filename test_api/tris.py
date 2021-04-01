# Suppose you have tris = 3 * 3, it means that you have 9 digits
# let's split the problem in 3 different areas:
# Horizontal
# Vertical
# Diagonal

# build Horizontal vectors
lenGame = 3

stringBit = ""
for x in range(lenGame):
    stringBit += "1"
for x in range(lenGame * 2):
    stringBit += "0"

# here we get the first correct sequence for the horizontal case:
# 111
# 000
# 000



arrayhorizontalOfWins = []
horizontalWin = int(stringBit, 2)
# print("Horizontal win", int(horizontalWin, 2))
arrayhorizontalOfWins.append(horizontalWin)
for x in range(lenGame - 1):
    arrayhorizontalOfWins.append(arrayhorizontalOfWins[x] >> lenGame)
print("Horizontal win", arrayhorizontalOfWins)

print("Horizontal map")
for x in arrayhorizontalOfWins:
    print("-", bin(x), x)

# let's calculate the other Vertical
arrayVerticalOfWins = []
stringBit = ""
for x in range(lenGame):
    stringBit += "1"
    for y in range(lenGame - 1):
        stringBit += "0"

# here we get the first correct sequence for the Vertical case:
# 100
# 100
# 100

# - 1000
#   1000
#   1000
#   1000
# - 1000
#   1000
#   1000
#   100
# - 1000
#   1000
#   1000
#   10
# - 1000
#   1000
#   1000
#   1

VerticalWin = int(stringBit, 2)
arrayVerticalOfWins.append(VerticalWin)

for x in range(lenGame - 1):
    arrayVerticalOfWins.append(arrayVerticalOfWins[x] >> 1)

print("Vertical map")
for x in arrayVerticalOfWins:
    print("-", bin(x), x)
