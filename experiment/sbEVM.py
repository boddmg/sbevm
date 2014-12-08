stack = []

class Stack():
    def __init__(self,init = []):
        self.data = init

    def push(self,item):
        self.append(item)

    def pop(self):
        return self.pop()

# instruction structure: {"cmd":cmd,"data":data}
INSTRUCTION_SET = ["in","out",
                  "add","sub","mul","div","or","and","xor",  #computing symbol
                  "push","pop",
                  "jgt","jge", "jlt","jeq","jne","jmp" ]

program = []
mem = [0 for n in range(1000)]

def read_from_mem(address):
    return

class sbVM():
    def __init__(self,program):
        self.stack = Stack()
        self.program = program

    def _push(self,data):
        address = data
        self.stack.push(mem[address])

    def _pop(self,data):
        value = self.stack.pop()
        address = data
        mem[address] = value

    def binary_operator(self,operator):
        value1 = self.stack.pop()
        value2 = self.stack.pop()
        value = operator(value1,value2)
        self.stack.push(value)

    def _add(self, data=None):
        self.binary_operator(lambda x,y:x+y)

    def _sub(self, data=None):
        self.binary_operator(lambda x,y:x-y)

    def _div(self, data=None):
        self.binary_operator(lambda x,y:x/y)

    def _mul(self, data=None):

        self.binary_operator(lambda x,y:x*y)

    def _or(self, data=None):
        self.binary_operator(lambda x,y:x or y)

    def _and(self, data=None):
        self.binary_operator(lambda  x,y:x and y)

def excute():
    pass

