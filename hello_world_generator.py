def hello_world():
    yield "hello"
    yield "world"
    yield "from"
    yield "generator"


for one_word in hello_world():
    print(one_word, end="")
    print(" ", end="")

