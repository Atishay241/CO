import opcode as op
import machine_code_converter as mc
import string


def binaryOfFraction(fraction):
    binary = str()
    while (fraction):

        fraction *= 2
        if (fraction >= 1):
            int_part = 1
            fraction -= 1
        else:
            int_part = 0

        binary += str(int_part)
    return binary


def floatingPoint(real):
    real = abs(real)
    int_string = bin(int(real))
    fraction = binaryOfFraction(real - int(real))
    ind = int_string.index('1')
    exp = bin((len(int_string) - ind - 1))[2:]
    exp = exp.zfill(3)

    mant = int_string[ind + 1:] + fraction
    mant = mant.rstrip("0")
    mant = mant + ('0' * (5 - len(mant)))
    return exp, mant


def check_intruc(instruction,pc,variables,labels):
    op.FLAG["V"]=0
    op.FLAG["G"]=0
    op.FLAG["L"]=0
    op.FLAG["E"]=0

    if(len(instruction)==0):
        return 1

    if len(instruction)!=4:
            # add r1 r2
        if len(instruction)>0 and instruction[0] in op.opcode_type_A:
            print(f'General Syntax Error: line {pc}: Invalid number of arguments to perform the {instruction[0]} operation')
            return 0

        elif len(instruction)!=3:

            # div r3 r4 r5
            if (instruction[0] in op.opcode_type_B) or (instruction[0] in op.opcode_type_C) or (instruction[0] in op.opcode_type_D):
                print(f'General Syntax Error:line {pc}: Invalid number of arguments to perform the {instruction[0]} operation')
                return 0

            elif len(instruction)!=2:

                if len(instruction)>0 and (instruction[0] in op.opcode_type_E):
                    print(f'General Syntax Error:line {pc}: Invalid number of arguments to perform the {instruction[0]} operation')
                    return 0

                elif len(instruction)!=1:
                    if (instruction[0] in op.opcode_type_F):
                        print(f'General Syntax Error:line {pc}: Invalid number of arguments to perform the {instruction[0]} operation')
                        return 0

                    elif len(instruction!=0):
                        print(f'General Syntax Error:line {pc}: Invalid number of arguments to perform any operation')
                        return 0

                    else:
                        return 1
                        
                else:
                    if len(instruction)>0 and (instruction[0] not in op.opcode_type_F):
                        print(f"Syntax Error: [TYPO] :line {pc}: Invalid instruction name is used")
                        return 0

                    elif (len(instruction)==1 and instruction[0]=="hlt"):
                        return "F"

            else:
                # print("gkhujlik;ol")
                # here length of instruction = 2 and opcode can be of E type or can be a variable declaration.

                # vhfv  vbfrvjh
                if len(instruction)>0 and (instruction[0] not in op.opcode_type_E):

                    print(f"Syntax Error: [TYPO]: line {pc}: Invalid instruction name is used")
                    return 0

                # jmp bfhrf
                elif (instruction[0] in op.opcode_type_E): #jmp, jlt, jgt, je

                    #jmp FLAGS
                    if (instruction[1] == "FLAGS"):

                        print(f"Syntax Error: line {pc}: Illegal use of FLAGS register is observed here")
                        return 0

                    #jmp <var>
                    elif (instruction[1] not in labels) and (instruction[1] in variables):
                        print(f"Syntax Error: line {pc}: Misuse of variables as labels")
                        return 0

                    #jmp dbhvj
                    elif (instruction[1] not in labels):
                        print(f"Syntax Error: line {pc}: Use of undefined labels")
                        return 0

                    #jmp <lbl>
                    else:
                        if (instruction[0] in op.opcode_type_E):
                            # print("ijguh")
                            return "E"

        else:
        # here length of instruction = 3 and opcode can be of B or C or D type.
            #print("***")
            # kare R1 R2
            if (instruction[0] not in op.opcode_type_B) and (instruction[0] not in op.opcode_type_C) and (instruction[0] not in op.opcode_type_D):
                print(f"Syntax Error: [TYPO] : line {pc}: Invalid instruction name is used")
                return 0

            elif (instruction[0] in op.opcode_type_B and instruction[0] not in op.opcode_type_C and instruction[2][0]!='$'):
                print(f"Syntax Error: [TYPO] : line {pc}:Invalid immediate value syntax")
                return 0

            # ls Rererg $frfgerfg
            elif (instruction[0] in op.opcode_type_B and instruction[2][0]=='$'):  # mov ($) ,rs,ls
                #print("$ ")
                #For mov R1 $abc
                if(instruction[0]=="mov"):
                    try:
                        #print("^^")
                        int(instruction[2][1:])
                    except:
                        print(f"Syntax Error: line {pc}: Illegal Immediate values is used")
                        return 0

                if (instruction[0] == "movf"):
                    try:
                        #print("&&")
                        float(instruction[2][1:])
                    except:
                        print(f"Syntax Error: line {pc}: Illegal Immediate values is used")
                        return 0

                #rs FLAGS $10
                if (instruction[1] == "FLAGS"):
                    #print("555")
                    print(f"Syntax Error: line {pc}: Illegal use of FLAGS register is observed here")
                    return 0

                #rs ro1 $10
                if (instruction[1] not in op.register):
                    #print("%%%")
                    print(f"Syntax Error: [TYPO] : line {pc}:Invalid registers are used")
                    return 0

                #mov R1 $jvhvj or # mov R2 $300

                if instruction[0]=="movf":
                    #print("####")
                    #print(float(instruction[2][1:]))
                    exp, mant = floatingPoint(float(instruction[2][1:]))

                    # Final  Representation.
                    newnot = exp + mant
                    if (len(newnot)!=8):
                        print(f"Syntax Error: line {pc}: Illegal Immediate values is used")
                        return 0
            
                if instruction[0]!="movf":
                    if int(instruction[2][1:])>255 or int(instruction[2][1:])<0:
                        print(f"Syntax Error: line {pc}: Illegal Immediate values is used")
                        return 0

                # mov R1 $100
                if(instruction[0]=="mov"):
                    a = int(instruction[2][1:])
                    op.Reg_val[instruction[1]]=a
                    return "B"

                if (instruction[0] == "movf"):
                    op.Reg_val[instruction[1]] = float(instruction[2][1:])
                    #print("fffefef")
                    return "B"

                # ls R3 $190
                elif(instruction[0]=="ls"):
                    a = int(instruction[2][1:])
                    ans=op.Reg_val[instruction[1]]<<a

                    if ans>2**16-1:
                        op.Reg_val[instruction[1]]=ans % (2**16)
                        op.FLAG["V"]=1 #overflow is observed
                        return "B"

                    elif ans<0:
                        op.Reg_val[instruction[1]]=0
                        op.FLAG["V"]=1 #underflow is observed
                        return "B"

                    else:
                        op.Reg_val[instruction[1]]=ans
                        return "B"

                # rs R3 $190
                elif(instruction[0]=="rs"):
                    a = int(instruction[2][1:])
                    ans=op.Reg_val[instruction[1]]>>a
                    op.Reg_val[instruction[1]]=ans
                    return "B"

            elif (instruction[0] in op.opcode_type_C):  # mov,div,not,cmp

                if(instruction[0]!="mov"):

                    #div FLAGS vfvdffv
                    if (instruction[1] == "FLAGS") or (instruction[2] == "FLAGS"):
                        print(f"Syntax Error: line {pc}: Illegal use of FLAGS register is observed here")
                        return 0

                    #div dfsdfsd vfvdffv
                    elif (instruction[1] not in op.register) or (instruction[2] not in op.register):
                        print(f"Syntax Error: [TYPO]: line {pc}: Invalid registers are used")
                        return 0

                    else:
                        a=op.Reg_val[instruction[1]]
                        b=op.Reg_val[instruction[2]]

                        # not R1 R2
                        if(instruction[0]=="not"):
                            op.Reg_val[instruction[2]]= ~a
                            return "C"

                        # div R1 R2
                        if(instruction[0]=="div"):
                            try:
                                op.Reg_val["R0"]=a//b
                                op.Reg_val["R1"]=a%b
                                return "C"


                            except ZeroDivisionError as Zer:
                                print(f"Error: {Zer}: line {pc}: division is not possible")
                                return 0
                                
                        # cmp R1 R2
                        if(instruction[0]=="cmp"):
                            
                            if a>b :
                                op.FLAG["G"]=1 #greater than flag is set

                            elif a<b:
                                op.FLAG["L"]=1 #less than flag is set

                            elif a==b:
                                op.FLAG["E"]=1 # equal to flag is set

                            return "C"

                        print(mc.inst_C(instruction))

                else:

                    #mov FLAGS EDBDB 
                    if (instruction[2] == "FLAGS"):
                        print(f"Syntax Error: line {pc}: Illegal use of FLAGS register is observed here")

                    #mov dfsdfsd vfvdffv
                    elif (instruction[1] not in op.register and instruction[1] != "FLAGS") or ( (instruction[2] not in op.register)):
                        print(f"Syntax Error: [TYPO] :line {pc}: Invalid registers are used")

                    # mov R1 FLAGS
                    elif (instruction[1] == "FLAGS"):
                        a=op.Reg_val["FLAGS"]
                        op.Reg_val[instruction[2]]=a
                        return "C"

                    # mov R1 R2
                    elif (instruction[1] in op.register):
                        a=op.Reg_val[instruction[1]]
                        op.Reg_val[instruction[2]]=a
                        return "C"

            elif len(instruction)>0 and (instruction[0] in op.opcode_type_D):  # ld,st

                #ld FLAGS gyguyv
                if (instruction[1] == "FLAGS") or (instruction[2] == "FLAGS"):
                    print(f"Syntax Error: line {pc}: Illegal use of FLAGS register is observed here")
                    return 0

                #ld ro1 gvgvg
                elif len(instruction)>0 and (instruction[1] not in op.register):
                    print(f"Syntax Error: [TYPO] :line {pc}: Invalid registers are used")
                    return 0

                #ld R1 gcgcgh
                elif (instruction[2] not in variables) and (instruction[2] not in labels):
                    print(f"Syntax Error: line {pc}: Use of undefined variable")
                    return 0

                #ld R1 <lbl>
                elif (instruction[2] not in variables) and (instruction[2] in labels):
                    print(f"Syntax Error: line {pc}: Misuse of labels as variables")
                    return 0

                else:
                    #ld R1 x
                    if(instruction[0]=="ld"):
                        # op.Reg_val[instruction[1]]=variables[instruction[2]]
                        return "D"

                    #st R1 x
                    elif(instruction[0]=="st"):
                        # variables[instruction[2]]=op.Reg_val[instruction[1]]
                        return "D"

    else:
        #if instruction==4 here we have taken all possible error that could have been in case of the opcode_type_A

            # fuclk r2 r4 e3
        if len(instruction)>0 and instruction[0] not in op.opcode_type_A:
            print(f"Syntax Error: [TYPO] : line {pc}: Invalid instruction name is used")
            return 0

            # add R1 FLAGS erer
        elif (instruction[1] == "FLAGS") or (instruction[2] == "FLAGS") or (instruction[3] == "FLAGS"):
            print(f"Syntax Error: line {pc}: Illegal use of FLAGS register is observed here")
            return 0

            # add R1 R2 FEFEF
        elif (instruction[1] not in op.register) or (instruction[2] not in op.register) or (instruction[3] not in op.register):
            print(f"Syntax Error: [TYPO] : line {pc}:Invalid registers are used")
            return 0

        else: # add,mul,sub,xor,or,and

            # add R1 R2 R3
            if(instruction[0]=="add"):
                ans= op.Reg_val[instruction[1]] + op.Reg_val[instruction[2]]
                if ans>2**16-1:
                    op.Reg_val[instruction[3]]=ans % (2**16)
                    op.FLAG["V"]=1; #overflow is observed
                    return "A"

                elif ans<0:
                    op.Reg_val[instruction[3]]=0
                    op.FLAG["V"]=1 #underflow is observed
                    return "A"

                else:
                   op.Reg_val[instruction[3]]=ans
                   return "A"

            if (instruction[0] == "addf"):
                ans = op.Reg_val[instruction[1]] + op.Reg_val[instruction[2]]
                if ans > 2 ** 16 - 1:
                    op.Reg_val[instruction[3]] = ans % (2 ** 16)
                    op.FLAG["V"] = 1;  # overflow is observed
                    return "A"

                elif ans < 0:
                    op.Reg_val[instruction[3]] = 0
                    op.FLAG["V"] = 1  # underflow is observed
                    return "A"

                else:
                    op.Reg_val[instruction[3]] = ans
                    return "A"

            # sub R1 R2 R3
            elif(instruction[0]=="sub"):
                ans= op.Reg_val[instruction[1]] - op.Reg_val[instruction[2]]

                if ans>2**16-1:
                    op.Reg_val[instruction[3]]=ans % (2**16)
                    op.FLAG["V"]=1; #overflow is observed
                    return "A"

                elif ans<0:
                    op.Reg_val[instruction[3]]=0
                    op.FLAG["V"]=1 #underflow is observed
                    return "A"

                else:
                    op.Reg_val[instruction[3]]=ans
                    return "A"

            elif (instruction[0] == "subf"):
                ans = op.Reg_val[instruction[1]] - op.Reg_val[instruction[2]]

                if ans > 2 ** 16 - 1:
                    op.Reg_val[instruction[3]] = ans % (2 ** 16)
                    op.FLAG["V"] = 1;  # overflow is observed
                    return "A"

                elif ans < 0:
                    op.Reg_val[instruction[3]] = 0
                    op.FLAG["V"] = 1  # underflow is observed
                    return "A"

                else:
                    op.Reg_val[instruction[3]] = ans
                    return "A"

            # mul R1 R2 R3
            elif(instruction[0]=="mul"):
                ans= op.Reg_val[instruction[1]] * op.Reg_val[instruction[2]]
                if ans>2**16-1:
                    op.Reg_val[instruction[3]]=ans % (2**16)
                    op.FLAG["V"]=1; #overflow is observed
                    return "A"

                elif ans<0:
                    op.Reg_val[instruction[3]]=0
                    op.FLAG["V"]=1 #underflow is observed
                    return "A"

                else:
                    op.Reg_val[instruction[3]]=ans
                    return "A"

            # xor R1 R2 R3
            elif(instruction[0]=="xor"):
                ans=op.Reg_val[instruction[1]] ^ op.Reg_val[instruction[2]] 
                op.Reg_val[instruction[3]]=ans
                return "A"
            
            # or R1 R2 R3
            elif(instruction[0]=="or"):
                ans=op.Reg_val[instruction[1]] | op.Reg_val[instruction[2]] 
                op.Reg_val[instruction[3]]=ans
                return "A"

            # and R1 R2 R3
            elif(instruction[0]=="and"):
                ans=op.Reg_val[instruction[1]] & op.Reg_val[instruction[2]] 
                op.Reg_val[instruction[3]]=ans
                return "A"