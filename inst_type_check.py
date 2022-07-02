import opcode as op
import machine_code_converter as mc

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
            print("")
        
        else:
        # here length of instruction = 3 and opcode can be of B or C or D type.
            print("")

            

    else:
            # fuclk r2 r4 e3
        if instruction[0] not in op.opcode_type_A:
            print("Syntax Error: [TYPO] : Invalid instruction name is used")

            # add R1 FLAGS erer
        elif (instruction[1] == "FLAGS") or (instruction[2] == "FLAGS") or (instruction[3] == "FLAGS"):
            print("Syntax Error: Illegal use of FLAGS register is observed here")

            # add R1 R2 FEFEF
        elif (instruction[1] not in op.register) or (instruction[2] not in op.register) or (instruction[3] not in op.register):
            print("Syntax Error: [TYPO] :Invalid registers are used")

            # add R1 R2 R3
        else:
            if(instruction[0]=="add"):
                ans= op.Reg_val[instruction[1]] + op.Reg_val[instruction[2]]
                if ans>2^16-1:
                    instruction[3]=ans % (2**16)
                    op.FLAG["V"]=1; #overflow is observed
                elif ans<0:
                    instruction[3]=0
                    op.FLAG["V"]=1

                else:
                    instruction[3]=ans

            elif(instruction[0]=="sub"):
                ans= op.Reg_val[instruction[1]] - op.Reg_val[instruction[2]]
                if ans>2^16-1:
                    instruction[3]=ans % (2**16)
                    op.FLAG["V"]=1; #overflow is observed
                elif ans<0:
                    instruction[3]=0
                    op.FLAG["V"]=1
                else:
                    instruction[3]=ans 


            elif(instruction[0]=="mul"):
                ans= op.Reg_val[instruction[1]] * op.Reg_val[instruction[2]]
                if ans>2**16-1:
                    instruction[3]=ans % (2**16)
                    op.FLAG["V"]=1; #overflow is observed
                elif ans<0:
                    instruction[3]=0
                    op.FLAG["V"]=1
                else:
                    instruction[3]=ans

            elif(instruction[0]=="xor"):
                ans=op.Reg_val[instruction[1]] ^ op.Reg_val[instruction[2]] 
                instruction[3]=ans
                
            elif(instruction[0]=="or"):
                ans=op.Reg_val[instruction[1]] | op.Reg_val[instruction[2]] 
                instruction[3]=ans

            elif(instruction[0]=="and"):
                ans=op.Reg_val[instruction[1]] & op.Reg_val[instruction[2]] 
                instruction[3]=ans


                
        

