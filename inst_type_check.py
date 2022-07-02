import opcode as op
import machine_code_converter as mc
variables={}
labels={}
def check(instruction):
    op.FLAG["V"]=0
    op.FLAG["G"]=0
    op.FLAG["L"]=0
    op.FLAG["E"]=0
    if len(instruction!=4):
            # add r1 r2
        if instruction[0] in op.opcode_type_A:
            print(f'General Syntax Error: Insufficient number of arguments to perform the {instruction[0]} operation')

        #if instruction==4 here we have taken all possible error that could have been in case of the opcode_type_A

        elif len(instruction)!=3:
            if (instruction[0] in op.opcode_type_B) or (instruction[0] in op.opcode_type_C) or (instruction[0] in op.code_type_D):
                print(f'General Syntax Error: Insufficient number of arguments to perform the {instruction[0]} operation')
        
        else:
        # here length of instruction = 3 and opcode can be of B or C or D type.

            # kare R1 R2
            if (instruction[0] not in op.opcode_type_B) and (instruction[0] not in op.opcode_type_C) and (instruction[0] not in op.code_type_D):
                print("Syntax Error: [TYPO] : Invalid instruction name is used")

            if (instruction[0] in op.opcode_type_B):  # mov,rs,ls

                #rs flag $10
                if (instruction[1] == "FLAGS"):
                    print("Syntax Error: Illegal use of FLAGS register is observed here")

                #rs ro1 $10
                elif (instruction[1] not in op.register):
                    print("Syntax Error: [TYPO] :Invalid registers are used")

                #rs R1 10
                elif (instruction[2][0]!='$'):
                    print("Syntax Error: [TYPO] :Invalid immediate value syntax")

                #mov R1 $300
                elif (int(instruction[2][1:])>255 or int(instruction[2][1:])<0):
                    print("Syntax Error: Illegal Immediate values (more than 8 bits)")

                else:
                    a=int(instruction[2][1:])
                    if(instruction[0]=="mov"):
                        op.Reg_val[instruction[1]]=a

                    if(instruction[0]=="ls"):
                        ans=op.Reg_val[instruction[1]]<<a
                        if ans>2**16-1:
                            op.Reg_val[instruction[1]]=ans % (2**16)
                            op.FLAG["V"]=1 #overflow is observed

                        elif ans<0:
                            op.Reg_val[instruction[1]]=0
                            op.FLAG["V"]=1 #underflow is observed

                        else:
                           op.Reg_val[instruction[1]]=ans

                    if(instruction[0]=="rs"):
                        ans=op.Reg_val[instruction[1]]>>a
                        op.Reg_val[instruction[1]]=ans

            elif (instruction[0] in op.opcode_type_C):  # mov,div,not,cmp

                if(instruction[0]!="mov"):

                    #div FLAGS vfvdffv
                    if (instruction[1] == "FLAGS"):
                        print("Syntax Error: Illegal use of FLAGS register is observed here")

                    #div dfsdfsd vfvdffv
                    elif (instruction[1] not in op.register) or (instruction[2] not in op.register):
                        print("Syntax Error: [TYPO] :Invalid registers are used")

                    else:
                        a=op.Reg_val[instruction[1]]
                        b=op.Reg_val[instruction[2]]
                        if(instruction[0]=="not"):
                            op.Reg_val[instruction[2]]= ~a

                        if(instruction[0]=="div"):
                            try:
                                op.Reg_val["R0"]=a//b
                                op.Reg_val["R1"]=a%b

                            except ZeroDivisionError as Zer:
                                print("Error: ",Zer,": division is not possible") 

                        if(instruction[0]=="cmp"):
                            
                            if op.Reg_val[instruction[1]]>op.Reg_val[instruction[2]]:
                                op.FLAG["G"]=1 #greater than flag is set

                            elif op.Reg_val[instruction[1]]<op.Reg_val[instruction[2]]:
                                op.FLAG["L"]=1 #less than flag is set

                            elif op.Reg_val[instruction[1]]<op.Reg_val[instruction[2]]:
                                op.FLAG["L"]=1 #less than flag is set

                else:
                    #mov FLAGS EDBDB 
                    if (instruction[1] == "FLAGS"):
                        print("Syntax Error: Illegal use of FLAGS register is observed here")

                    #mov dfsdfsd vfvdffv
                    elif (instruction[1] not in op.register) or (instruction[2] != "FLAGS"):
                        print("Syntax Error: [TYPO] :Invalid registers are used")

                    #mov R1 FLAGS
                    else:
                        a=op.Reg_val["FLAGS"]
                        op.Reg_val[instruction[1]]=a

            elif (instruction[0] in op.opcode_type_D):  # ld,st

                #ld FLAGS gyguyv
                if (instruction[1] == "FLAGS"):
                    print("Syntax Error: Illegal use of FLAGS register is observed here")

                #ld ro1 gvgvg
                elif (instruction[1] not in op.register):
                    print("Syntax Error: [TYPO] :Invalid registers are used")

                #ld R1 gcgcgh
                elif (instruction[2] not in variables):
                    print("Syntax Error: Use of undefined variable")

                #ld R1 x
                else:
                    if(instruction[0]=="ld"):
                        a=variables[instruction[2]]
                        op.Reg_val[instruction[1]]=a



    if (len(instruction!=2)):
        if (instruction[0] in (op.opcode_type_E)):
            print(f'General Syntax Error: Insufficient number of arguments to perform the {instruction[0]} operation')
        
    else:
        if (instruction[0] not in op.opcode_type_E):
            print("Syntax Error: [TYPO] : Invalid instruction name is used")

        elif(instruction[1] in variables):
                print("Syntax Error: [TYPO] :Variables can not be used in place of labels ")

        elif(instruction[1] not in labels):
            print("Syntax Error: [TYPO] :Invalid labels are used")

        else:
            if(instruction[0]=="jmp"):
                pass
            elif(instruction[0]=="jlt"):
                pass
            elif(instruction[0]=="jgt"):
                pass
            elif(instruction[0]=="je"):
                pass

    if (len(instruction!=1)):
        if (instruction[0] in (op.opcode_type_F)):
            print(f'General Syntax Error: Insufficient number of arguments to perform the {instruction[0]} operation')
                   
    else:
        if (instruction[0] not in op.opcode_type_E):
            print("Syntax Error: [TYPO] : Invalid instruction name is used")