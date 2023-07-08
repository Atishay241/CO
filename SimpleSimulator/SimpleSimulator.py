import sys
import fileinput

op_codes = {"10000": ["add", "A"], "10001": ["sub", "A"], "10110": ["mul", "A"],
        "11010": ["xor", "A"], "11011": ["or", "A"], "11100": ["and", "A"],
        "10010": ["mov", "B"], "11001": ["ls", "B"], "11000": ["rs", "B"],
        "10011": ["mov", "C"], "10111": ["div", "C"], "11101": ["not", "C"],
        "11110": ["cmp", "C"], "10100": ["ld", "D"], "10101": ["st", "D"],
        "11111": ["jmp", "E"], "01100": ["jlt", "E"], "01101": ["jgt", "E"],
        "01111": ["je", "E"], "01010": ["hlt", "F"], "00000": ["addf", "A"],
        "00001": ["subf", "A"], "00010": ["movf", "B"]}

registers = {"000": 0, "001": 1, "010": 2, "011": 3,
    "100": 4, "101": 5, "110": 6, "111": 7}


flag = {"V": 0, "L": 0, "G": 0, "E": 0}

reg_value = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: flag}

list_instruction = []

# Taking input from terminal
l = sys.stdin.read().splitlines()
for i in l:
	list_instruction.append(i.strip())


# with fileinput.input(files=('test.txt')) as f:
# 		for line in f:
# 			list_instruction.append(line.strip())


# print(list_instruction)

def overflow(ans, reg):
    checker=isinstance(ans,float)
    if ans > (2**16)-1:
        reg_value[reg] = ans % (2**16)  # doubt
        flag["V"] = 1;  # overflow is observed
        # return True

    elif ans < 0:
        reg_value[reg] = 0
        flag["V"] = 1  # underflow is observed
        # return True
    
    elif(checker==True):

        a=[1.0, 1.03125, 1.0625, 1.09375, 1.125, 1.15625, 1.1875, 1.21875, 1.25, 1.28125, 1.3125, 1.34375, 1.375, 1.40625, 1.4375, 1.46875, 1.5, 1.53125, 1.5625, 1.59375, 1.625, 1.65625, 1.6875, 1.71875, 1.75, 1.78125, 1.8125, 1.84375, 1.875, 1.90625, 1.9375, 1.96875, 2.0, 2.0625, 2.125, 2.1875, 2.25, 2.3125, 2.375, 2.4375, 2.5, 2.5625, 2.625, 2.6875, 2.75, 2.8125, 2.875, 2.9375, 3.0, 3.0625, 3.125, 3.1875, 3.25, 3.3125, 3.375, 3.4375, 3.5, 3.5625, 3.625, 3.6875, 3.75, 3.8125, 3.875, 3.9375, 4.0, 4.125, 4.25, 4.375, 4.5, 4.625, 4.75, 4.875, 5.0, 5.125, 5.25, 5.375, 5.5, 5.625, 5.75, 5.875, 6.0, 6.125, 6.25, 6.375, 6.5, 6.625, 6.75, 6.875, 7.0, 7.125, 7.25, 7.375, 7.5, 7.625, 7.75, 7.875, 8.0, 8.25, 8.5, 8.75, 9.0, 9.25, 9.5, 9.75, 10.0, 10.25, 10.5, 10.75, 11.0, 11.25, 11.5, 11.75, 12.0, 12.25, 12.5, 12.75, 13.0, 13.25, 13.5, 13.75, 14.0, 14.25, 14.5, 14.75, 15.0, 15.25, 15.5, 15.75, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 31.0, 31.5, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0]
	    
        if(ans not in a):
            flag["V"]=1
            # return True

    else:
       reg_value[reg]=ans
    #    return False

    


def flag_value():
    f=12*"0"
    f+=str(flag["V"])+str(flag["L"])+str(flag["G"])+str(flag["E"])
    return f

def convertToInt(mantissa_str):
	power_count = -1
	mantissa_int = 0
	for i in mantissa_str:

		mantissa_int += (int(i) * pow(2, power_count))
		power_count -= 1
		
	return (mantissa_int + 1)

def floatingans(num):

	# num = '11101011'

	expo_bias = int(num[0 :3 ], 2)

	expo_unbias = expo_bias - 4

	mantissa_str = num[3 : ]

	mantissa_int = convertToInt(mantissa_str)

	real_no = mantissa_int * pow(2, expo_unbias)

	return real_no

def flag_reset():
    # print("dfsghfdsafgjfdsa")
    flag["E"]=0
    flag["G"]=0
    flag["L"]=0
    flag["V"]=0

def caller(instruction,instr_type,instr_name,r):
    # print("The answer of flag is ",int(flag_value(),2))
    opnext=list_instruction[r+1][0:5]
    instr_name_next=op_codes[opnext][0]
    instr_type_next=op_codes[opnext][1]

    if(instr_type=="A"):

        reg1 = registers[instruction[7:10]]
        reg2 = registers[instruction[10:13]]
        reg3 = registers[instruction[13:]]

        if(instr_name=="add" or instr_name=="addf"):

            reg_value[reg3] = reg_value[reg1]+reg_value[reg2]
            ans = reg_value[reg3]
            overflow(ans,reg3)

        elif(instr_name=="sub" or instr_name=="subf"):

            reg_value[reg3] = reg_value[reg1]-reg_value[reg2]
            ans = reg_value[reg3]
            overflow(ans,reg3)

        elif(instr_name=="mul"):

            reg_value[reg3] = reg_value[reg1] * reg_value[reg2]
            ans = reg_value[reg3]
            overflow(ans,reg3)

        elif(instr_name=="xor"):

            reg_value[reg3] = reg_value[reg1] ^ reg_value[reg2]

        elif(instr_name=="or"):

            reg_value[reg3] = reg_value[reg1] | reg_value[reg2]

        elif(instr_name=="and"):

            reg_value[reg3] = reg_value[reg1] & reg_value[reg2]

        answer()

        if(flag["V"]==1 and instr_name_next=="mov" and instr_type_next=="B"):
            pass
            
        else:
            flag_reset()

    
    
    elif(instr_type=="B"):

        reg = registers[instruction[5:8]]
        imm=int(instruction[8:],2)
        # print("register is ",reg)
        if(instr_name == "mov"):
            # print("hfgjklo")
            reg_value[reg]=imm
            # print("register value of 1 is : ",reg_value[1])
        elif(instr_name == "rs"):
            reg_value[reg]=reg_value[reg]>>imm

        elif(instr_name == "ls"):
            reg_value[reg]=reg_value[reg]<<imm

        elif(instr_name=="movf"):
            imm= floatingans(instruction[8:])
            reg_value[reg]=imm

        answer()



    elif(instr_type=="C"):
        global temp
        reg1 = registers[instruction[10:13]]
        reg2 = registers[instruction[13:]]

        if(instr_name == "mov"):
            if(reg1==7):
                reg_value[reg2]=int(flag_value(),2)
                # print("the value of reg is ",reg2)
                # print("the value of reg is ",reg_value[reg2])
                flag_reset()

            else:
                reg_value[reg2]=reg_value[reg1]
                flag_reset()
        
        
        elif(instr_name == "div"):
            reg_value[0]=reg_value[reg1]/reg_value[reg2]
            reg_value[1]=reg_value[reg1]%reg_value[reg2]

        
        elif(instr_name == "not"):
            reg_value[reg2] = ~reg_value[reg1]


        elif(instr_name == "cmp"):

            if(reg_value[reg1]==reg_value[reg2]):
                flag["E"]=1

            elif(reg_value[reg1]>reg_value[reg2]):
                flag["G"]=1

            else:
                flag["L"]=1

        answer()
    


    elif(instr_type=="D"):
        
        reg1 = registers[instruction[5:8]]
        address = int(instruction[8:],2)


        if(instr_name == "ld"):
            reg_value[reg1] = int(memory[address],2)
        

        elif(instr_name == "st"):
            a=bin(int(reg_value[reg1]))[2:]
            b=(16-len(a))*"0" + a
            memory[address]=b

        answer()


    elif(instr_type=="E"):
        global pc
        address = int(instruction[8:],2)

        if(instr_name == "jmp"):
            flag_reset()
            answer()
            pc=address-1
            
        
        elif(instr_name=="jlt" and flag["L"]==1):
            flag_reset()
            answer()
            pc=address-1

        elif(instr_name=="jgt" and flag["G"]==1):
            flag_reset()
            answer()
            pc=address-1

        elif(instr_name=="je" and flag["E"]==1):
            flag_reset()
            answer()
            pc=address-1
        
        else:
            # print("pc is ",pc)
            # print("6fryguhikjml")
            flag_reset()
            answer()
        
        # flag_reset()
        
        # answer()

    
    else:
        answer()
        
    

def reset(instr_type,instr_name):
    if(instr_type=="jlt" or instr_type=="jgt" or instr_type=="je" or instr_type=="cmp" or instr_name=="A"):
        return
    if(instr_type=="mov" and instr_name=="C" ):
        return
    else:
        flag_reset()

# def reset

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
    # addingbit = "0"*8
	return  exp+ mant


def converter(reg):
    check_type=isinstance(reg,int)
    if(check_type==True):
        a=bin(int(reg))[2:]
        b="0"*(16-len(a))+a
        return str(b)
    else:
        a="0"*8
        b= a+ floatingPoint(reg) 
        return str(b)


def answer():
    a=bin(int(pc))[2:]
    b="0"*(8-len(a)) + a
    print(b,end=" ")
    
    for i in range(0,7):
        # print("the value is ",reg_value[i])
        print(converter(reg_value[i]),end=" ")
        
    # ans[8]=flag_value
    print(flag_value())
    # # print(*ans)



pc=0
last=len(list_instruction)

lst="0"*16
memory=[lst]*256

cycle=[]
x=[]
y=[]
m=[]
counter=0


if(list_instruction[last-1]==""):
    for i in range(last-1):
        memory[i]=list_instruction[i]


    while(pc!=last-1):
        # flag_reset()
        opcode=list_instruction[pc][0:5]
        instr_name=op_codes[opcode][0]
        instr_type=op_codes[opcode][1]
        cycle.append(counter)
        m.append(pc)
        counter+=1
        r=pc
        if(pc==last-2):
            r=pc-1
        # print(instr_name,instr_type)
        caller(list_instruction[pc],instr_type,instr_name,r)
        reset(instr_name,instr_type)
        pc+=1


    for i in memory:
        print(i)

else:

    for i in range(last):
        memory[i]=list_instruction[i]


    while(pc!=last):
        # flag_reset()
        opcode=list_instruction[pc][0:5]
        instr_name=op_codes[opcode][0]
        instr_type=op_codes[opcode][1]
        cycle.append(counter)
        m.append(pc)
        r=pc
        if(pc==last-1):
            r=pc-1
        counter+=1
        # print(instr_name,instr_type)
        caller(list_instruction[pc],instr_type,instr_name,r)
        # temp=int(flag_value(),2)
        reset(instr_name,instr_type)

        pc+=1


    for i in memory:
        print(i)


# Q4  graph between the cycle no and corresponding memory address that was being accessed at that time

import numpy as np
import matplotlib.pyplot as plt
cycle.extend(x)
m.extend(y)
plt.scatter(np.array(cycle),np.array(m),marker="*",s=100,color="cyan")
plt.xlabel("cycle")
plt.ylabel("memory")
plt.show()