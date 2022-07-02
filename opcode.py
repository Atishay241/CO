# OPCODES for Type A instruction

opcode_type_A = { "add" : "10000" , "sub" : "10001" , "mul" : "10110" , "xor" : "11010" , "or" : "11011" , "and" : "11100" }


# OPCODES for Type B instruction

opcode_type_B = { "mov" : "10010" , "ls" : "11001" , "rs" : "11000" }


# OPCODES for Type C instruction

opcode_type_C = { "mov" : "10011" , "div" : "10111" , "not" : "11101" , "cmp" : "11110" }


# OPCODES for Type D instruction

opcode_type_D = { "ld" : "10100" , "st" : "10101" }


# OPCODES for Type E instruction

opcode_type_E = { "jmp" : "11111", "jlt" : "01100" , "jgt" : "01101" , "je" : "01111" }


# OPCODES for Type F instruction

opcode_type_F = { "hlt" : "01010" }

# Register (Binary representation)

register = { "R0" : "000" , "R1" : "001" , "R2" : "010" , "R3" : "011" , "R4" : "100" , "R5" : "101" , "R6" : "110"}

#Flag registor

flag = ["111"]

# Flags Semantics

FLAG = { "V" : 0 , "L" : 0 , "G" : 0 , "E" : 0 }

# Registers value

Reg_val = { "R0" : 0 , "R1" : 0 , "R2" : 0 , "R3" : 0 , "R4" : 0 , "R5" : 0 , "R6" : 0 ,"FLAGS" : 0}
     


