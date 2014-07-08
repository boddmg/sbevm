stack = []
instructionSet = ["in","out",
                  "add","sub","mul","div",  #computing symbol
                  "push","pop",
                  "jgt","jge", "jlt","jeq","jne","jmp" ]
program = []
mem = [0 for n in range(1000)]

print instructionSet