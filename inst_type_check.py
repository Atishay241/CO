import opcode as op
import machine_code_converter as mc
import string
import main


def check(instruction):
    op.FLAG["V"]=0
    op.FLAG["G"]=0
    op.FLAG["L"]=0
    op.FLAG["E"]=0

    if len(instruction!=4):
            # add r1 r2
        if instruction[0] in op.opcode_type_A:
            print(f'General Syntax Error: Invalid number of arguments to perform the {instruction[0]} operation')

        elif len(instruction)!=3:

            # div r3 r4 r5
            if (instruction[0] in op.opcode_type_B) or (instruction[0] in op.opcode_type_C) or (instruction[0] in op.code_type_D):
                print(f'General Syntax Error: Invalid number of arguments to perform the {instruction[0]} operation')

            elif len(instruction)!=2:

                if (instruction[0] in op.opcode_type_E):
                    print(f'General Syntax Error: Invalid number of arguments to perform the {instruction[0]} operation')

                elif len(instruction)!=1:
                    if (instruction[0] in op.opcode_type_F) or (instruction[0][-1]==":"):
                        print(f'General Syntax Error: Invalid number of arguments to perform the {instruction[0]} operation')

                else:
                    if (instruction[0] not in op.opcode_type_F) or (instruction[0][-1] != ":"):
                        print("Syntax Error: [TYPO] : Invalid instruction name is used")


            else:
                # here length of instruction = 2 and opcode can be of E type or can be a variable declaration.

                # vhfv  vbfrvjh
                if (instruction[0] not in op.opcode_type_E):
                    print("Syntax Error: [TYPO] : Invalid instruction name is used")

                # jmp bfhrf
                elif (instruction[0] in op.opcode_type_E): #jmp, jlt, jgt, je

                    #jmp FLAGS
                    if (instruction[1] == "FLAGS"):
                        print("Syntax Error: Illegal use of FLAGS register is observed here")

                    #jmp <var>
                    elif (instruction[1] not in main.labels) and (instruction[1] in main.variables):
                        print("Syntax Error: Misuse of variables as labels")

                    #jmp dbhvj
                    elif (instruction[1] not in main.labels):
                        print("Syntax Error: Use of undefined labels")

                    #jmp <lbl>
                    else:
                        if (instruction[1]=="jmp"):
                            pass
                        elif (instruction[1]=="jlt"):
                            pass
                        elif (instruction[1]=="jgt"):
                            pass
                        elif (instruction[1]=="je"):
                            pass

                        print(mc.inst_E(instruction))

        else:
        # here length of instruction = 3 and opcode can be of B or C or D type.

            # kare R1 R2
            if (instruction[0] not in op.opcode_type_B) and (instruction[0] not in op.opcode_type_C) and (instruction[0] not in op.code_type_D):
                print("Syntax Error: [TYPO] : Invalid instruction name is used")

            elif (instruction[0] in op.opcode_type_B and instruction[0] not in op.opcode_type_C and instruction[2][0]!='$'):
                print("Syntax Error: [TYPO] :Invalid immediate value syntax")

            # ls Rererg frfgerfg
            elif (instruction[0] in op.opcode_type_B and instruction[2][0]=='$'):  # mov ($) ,rs,ls

                #rs FLAGS $10
                if (instruction[1] == "FLAGS"):
                    print("Syntax Error: Illegal use of FLAGS register is observed here")

                #rs ro1 $10
                elif (instruction[1] not in op.register):
                    print("Syntax Error: [TYPO] :Invalid registers are used")

                #mov R1 $jvhvj or # mov R2 $300
                elif (int(instruction[2][1:])<=255 and int(instruction[2][1:])>=0)==False:
                    print("Syntax Error: Illegal Immediate values is used")

                else:
                    a=int(instruction[2][1:])

                    # mov R1 $100
                    if(instruction[0]=="mov"):
                        op.Reg_val[instruction[1]]=a

                    # ls R3 $190
                    elif(instruction[0]=="ls"):
                        ans=op.Reg_val[instruction[1]]<<a

                        if ans>2**16-1:
                            op.Reg_val[instruction[1]]=ans % (2**16)
                            op.FLAG["V"]=1 #overflow is observed

                        elif ans<0:
                            op.Reg_val[instruction[1]]=0
                            op.FLAG["V"]=1 #underflow is observed

                        else:
                           op.Reg_val[instruction[1]]=ans

                    # rs R3 $190
                    if(instruction[0]=="rs"):
                        ans=op.Reg_val[instruction[1]]>>a
                        op.Reg_val[instruction[1]]=ans

                    print(mc.inst_B(instruction))
            elif (instruction[0] in op.opcode_type_C):  # mov,div,not,cmp

                if(instruction[0]!="mov"):

                    #div FLAGS vfvdffv
                    if (instruction[1] == "FLAGS") or (instruction[2] == "FLAGS"):
                        print("Syntax Error: Illegal use of FLAGS register is observed here")

                    #div dfsdfsd vfvdffv
                    elif (instruction[1] not in op.register) or (instruction[2] not in op.register):
                        print("Syntax Error: [TYPO] :Invalid registers are used")

                    else:
                        a=op.Reg_val[instruction[1]]
                        b=op.Reg_val[instruction[2]]

                        # not R1 R2
                        if(instruction[0]=="not"):
                            op.Reg_val[instruction[2]]= ~a

                        # div R1 R2
                        if(instruction[0]=="div"):
                            try:
                                op.Reg_val["R0"]=a//b
                                op.Reg_val["R1"]=a%b

                            except ZeroDivisionError as Zer:
                                print("Error: ",Zer,": division is not possible") 

                        # cmp R1 R2
                        if(instruction[0]=="cmp"):
                            
                            if a>b :
                                op.FLAG["G"]=1 #greater than flag is set

                            elif a<b:
                                op.FLAG["L"]=1 #less than flag is set

                            elif a==b:
                                op.FLAG["E"]=1 # equal to flag is set

                        print(mc.inst_C(instruction))

                else:

                    #mov FLAGS EDBDB 
                    if (instruction[1] == "FLAGS"):
                        print("Syntax Error: Illegal use of FLAGS register is observed here")

                    #mov dfsdfsd vfvdffv
                    elif (instruction[1] not in op.register) or ((instruction[2] != "FLAGS") and (instruction[2] not in op.register)):
                        print("Syntax Error: [TYPO] :Invalid registers are used")

                    # mov R1 FLAGS
                    elif (instruction[2] == "FLAGS"):
                        a=op.Reg_val["FLAGS"]
                        op.Reg_val[instruction[1]]=a

                    # mov R1 R2
                    elif (instruction[2] in op.register):
                        a=op.Reg_val[instruction[1]]
                        op.Reg_val[instruction[2]]=a

                        print(mc.inst_C(instruction))

            elif (instruction[0] in op.opcode_type_D):  # ld,st

                #ld FLAGS gyguyv
                if (instruction[1] == "FLAGS") or (instruction[2] == "FLAGS"):
                    print("Syntax Error: Illegal use of FLAGS register is observed here")

                #ld ro1 gvgvg
                elif (instruction[1] not in op.register):
                    print("Syntax Error: [TYPO] :Invalid registers are used")

                #ld R1 gcgcgh
                elif (instruction[2] not in main.variables) and (instruction[2] not in main.labels):
                    print("Syntax Error: Use of undefined variable")

                #ld R1 <lbl>
                elif (instruction[2] not in main.variables) and (instruction[2] in main.labels):
                    print("Syntax Error: Misuse of labels as variables")

                else:
                    #ld R1 x
                    if(instruction[0]=="ld"):
                        op.Reg_val[instruction[1]]=main.variables[instruction[2]]

                    #st R1 x
                    elif(instruction[0]=="st"):
                        main.variables[instruction[2]]=op.Reg_val[instruction[1]]

                    print(mc.inst_D(instruction))

    else:
        #if instruction==4 here we have taken all possible error that could have been in case of the opcode_type_A

            # fuclk r2 r4 e3
        if instruction[0] not in op.opcode_type_A:
            print("Syntax Error: [TYPO] : Invalid instruction name is used")

            # add R1 FLAGS erer
        elif (instruction[1] == "FLAGS") or (instruction[2] == "FLAGS") or (instruction[3] == "FLAGS"):
            print("Syntax Error: Illegal use of FLAGS register is observed here")

            # add R1 R2 FEFEF
        elif (instruction[1] not in op.register) or (instruction[2] not in op.register) or (instruction[3] not in op.register):
            print("Syntax Error: [TYPO] :Invalid registers are used")

        else: # add,mul,sub,xor,or,and

            # add R1 R2 R3
            if(instruction[0]=="add"):
                ans= op.Reg_val[instruction[1]] + op.Reg_val[instruction[2]]
                if ans>2**16-1:
                    op.Reg_val[instruction[3]]=ans % (2**16)
                    op.FLAG["V"]=1; #overflow is observed

                elif ans<0:
                    op.Reg_val[instruction[3]]=0
                    op.FLAG["V"]=1 #underflow is observed

                else:
                   op.Reg_val[instruction[3]]=ans

            # sub R1 R2 R3
            elif(instruction[0]=="sub"):
                ans= op.Reg_val[instruction[1]] - op.Reg_val[instruction[2]]

                if ans>2**16-1:
                    op.Reg_val[instruction[3]]=ans % (2**16)
                    op.FLAG["V"]=1; #overflow is observed

                elif ans<0:
                    op.Reg_val[instruction[3]]=0
                    op.FLAG["V"]=1 #underflow is observed

                else:
                    op.Reg_val[instruction[3]]=ans 

            # mul R1 R2 R3
            elif(instruction[0]=="mul"):
                ans= op.Reg_val[instruction[1]] * op.Reg_val[instruction[2]]
                if ans>2**16-1:
                    op.Reg_val[instruction[3]]=ans % (2**16)
                    op.FLAG["V"]=1; #overflow is observed

                elif ans<0:
                    op.Reg_val[instruction[3]]=0
                    op.FLAG["V"]=1 #underflow is observed

                else:
                    op.Reg_val[instruction[3]]=ans

            # xor R1 R2 R3
            elif(instruction[0]=="xor"):
                ans=op.Reg_val[instruction[1]] ^ op.Reg_val[instruction[2]] 
                op.Reg_val[instruction[3]]=ans
            
            # or R1 R2 R3
            elif(instruction[0]=="or"):
                ans=op.Reg_val[instruction[1]] | op.Reg_val[instruction[2]] 
                op.Reg_val[instruction[3]]=ans

            # and R1 R2 R3
            elif(instruction[0]=="and"):
                ans=op.Reg_val[instruction[1]] & op.Reg_val[instruction[2]] 
                op.Reg_val[instruction[3]]=ans

            print(mc.inst_A(instruction))