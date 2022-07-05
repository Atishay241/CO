import opcode as op


def dec_to_bin(num):
    a = num
    b = ''
    if a == 0:
        return 0
    if a != 0:
        while a != 0:
            b = b+str(a % 2)
            a = a//2
        b = b[::-1]
        return b

#here argument we are passing is in list and list contains 4 segments

def inst_A(instruction):
    a=""
    a+=op.opcode_type_A[instruction[0]]
    a+="00"
    a+=op.register[instruction[1]]
    a+=op.register[instruction[2]]
    a+=op.register[instruction[3]]
    
    return a

#here list contains only 3 segments.
def inst_B(instruction):
    a=""
    a+=op.opcode_type_B[instruction[0]]
    a+=op.register[instruction[1]]
    num1=int(instruction[2][1:])
    b=str(dec_to_bin(num1))
    c=len(b)
    a+=(8-c)*"0"
    a+=b
    return a

#here list contains only 3 segments.
def inst_C(instruction):
    a=""
    a+=op.opcode_type_C[instruction[0]]
    a+="00000"
    a+=op.register[instruction[1]]
    a+=op.register[instruction[2]]    
    return a

#here list contains only 3 segments.
def inst_D(instruction):
    a=""
    a+=op.opcode_type_D[instruction[0]]
    a+=op.register[instruction[1]]
    
    return a

#here list contains only 1 segment.
def inst_E(instruction):
    a=""
    a+=op.opcode_type_E[instruction[0]]
    
    return a

#here list contains only 1 segment.
def inst_F(instruction):
    a=""
    a+=op.opcode_type_F[instruction[0]]
    a+=11*"0"
    
    return a
    