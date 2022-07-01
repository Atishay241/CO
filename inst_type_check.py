import opcode as op

def check(instruction):

    if len(instruction)==0:
        return "empline"


    elif(len(instruction)==1):

        if(instruction[0][-1]==":"):
            return "label"

        elif(instruction[0]=="hlt"):
            return "F"


    elif(len(instruction)==2):
        #error if in var xyz len(xyz)>2
        if(instruction[0]=="var" and len(xyz)>2):
            return "var_def"

        else:
            return "E"


    elif(len(instruction)==3):

        if(instruction[2][0]=="$"):
            return "B"

        elif(instruction[0] in op.opcode_type_C):
            return "C"

        elif(instruction[0] in op.opcode_type_D):
            return "D"


    elif(len(instruction)==4):
        return "A"
