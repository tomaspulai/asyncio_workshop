def hello_world():
    yield "hello"
    yield "world"
    yield "from"
    yield "generator"


print("iterate via for loop:")
for one_word in hello_world():
    print(one_word, end="")
    print(" ", end="")

print()
print()

print("iterate via __next__:")
hw = hello_world()
print(hw.__next__(), end=" ")
print(hw.__next__(), end=" ")
print(hw.__next__(), end=" ")
print(hw.__next__(), end=" ")
#print(hw.__next__())


