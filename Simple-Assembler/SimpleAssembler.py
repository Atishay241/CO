import checker_f as cf
import fileinput
import machine_code_converter as mc


#this list contains all the instructions in the text file
list_instruction=[]

#dictionary contains the variables as their key and the their memory adress as their value
variables={}

#dictionary contains the labels as their key and the their memory adress as their value
labels={}

#list contains pc having var as their first element but length is not acc to the syntax 
invalid_var_arg=[]

#list contains pc having redeclaratioin of the variable.
error_duplicate_var=[]

#list contains pc having redeclaratioin of the label.
error_duplicate_lbl=[]

#list contains pc having declaratioin of the variable in beween.
error_in_between_var=[]

#goes through each instruct in a text file one by one
pc=0

#goes through only those instruct in a text file that does not specify any variable declarartion
count=0

#var_flag==1 only when variables are declared in start of the program and it goes to 0. instantly when the instruction is not var and will never change to 1 again
var_flag=1

# def check_var_name(word):
# 	for i in word:
# 		if i not in valid_var_name:
# 			return False
# 	return True

#Taking input from terminal
import sys
l=sys.stdin.read().splitlines()
for i in l:
	list_instruction.append(i.split())


# with fileinput.input(files=('test.txt')) as f:
# 		for line in f:

# 			l=line.split()
# 			list_instruction.append(l)


for i in (list_instruction):
	#var xyz here xyz is already a declared variable
	if(len(i)==2 and i[0]=="var" and i[1] in variables):
		error_duplicate_var.append(pc)

	#var xyz here xyz is a newly declared variable
	elif(len(i)==2 and i[0]=="var" and i[1] not in variables):
		# newly declared variable
		variables[i[1]]=0	

	#var xyz adef sf here invalid argument number
	elif(len(i)>=1 and len(i)!=2 and i[0]=="var"):
		invalid_var_arg.append(pc)

	#foo: a newly declared variable actually and assigning them the memory adress actually
	elif (len(i)>=1 and i[0][-1]==":" and i[0][:-1] not in labels and i[0]!="var"):
		# new label declared
		labels[i[0][:-1]]=count
		count+=1

	#foo: a redeclared variable actually
	elif (len(i)>=1 and i[0][-1]==":" and i[0][:-1] in labels and i[0]!="var"):
		error_duplicate_lbl.append(pc)
		count+=1

	#foo: fv vfe
	elif(len(i)>=1 and i[0]!="var"):
		count+=1

	#we are going to new instruction
	pc+=1

last=pc-1

#again checking instruction from the start again
pc=0


for i in (list_instruction):
	#now we are checking whether or not were there any variable declaration in between the programme
	if(len(i)>=1 and i[0]=="var" and var_flag==0):
		error_in_between_var.append(pc)

	#now we are assigning memory adress to correctly declared variables
	elif(len(i)>=1 and i[0]=="var" and var_flag==1):
		variables[i[1]]=count
		count+=1

	#for empty lines we ignore them
	elif(len(i)==0):
		pass
	
	#now here if new inst except that of variable start then it is the flag=0
	else:
		var_flag=0
	pc+=1

pc=0

all_err=[]


# print(labels)
# print(variables)
# print(error_duplicate_lbl)
# print(error_duplicate_var)
# print(error_in_between_var)
# print(all_err)

# print(list_instruction)

m=last
#print("-")
#print(m)
#print("-")
while (len(list_instruction[m])==0 and m>0):
	m-=1
#print(m)
for i in (list_instruction):

	if pc in error_in_between_var:
		print(f"Syntax Error:line {pc+1}: Variables not declared at the beginning and being declared in between")
		all_err.append(0)

	elif pc in error_duplicate_var:
		print(f"General Syntax Error:line {pc+1}: Redeclaration of already declared variable.")
		all_err.append(0)

	elif(len(i)>2 and pc==last):
		print(f"Syntax error: line {pc+1} : Missing hlt instruction at the end")
		all_err.append(0)


	elif(len(i)==2 and pc==last):
		if(i[0][0:-1] in labels and i[1]=="hlt"):
			all_err.append(cf.check_intruc(i[1:],pc+1,variables,labels))
		else:
			print(f"Syntax error: line {pc+1} : Missing hlt instruction at the end")
			all_err.append(0)

	elif len(i)==1 and pc==last:
		# if(len(i)==1 and i[0]!="hlt" ):
		# 	print(f"Syntax error: line {pc+1} : Missing hlt instruction at the end")
		# 	all_err.append(0)

		# elif(len(i)==2 and i[0][0:-1] in labels and i[1]!="hlt"):
		# 	print(f"Syntax error: line {pc+1} : Missing hlt instruction at the end")
		# 	all_err.append(0)

		# elif(len(i)>2):
		if(i[0]=="hlt"):
			all_err.append(cf.check_intruc(i,pc+1,variables,labels))
		else:
			print(f"Syntax error: line {pc+1} : Missing hlt instruction at the end")
			all_err.append(0)

	elif len(i)>0 and pc!=last and i[0]=="hlt" and pc!=m:
		#print(pc)
		print(f"Syntax error: line {pc+1} : hlt not being used as the last instruction")
		all_err.append(0)

	elif len(i)==2 and pc!=last and i[0][0:-1] in labels and i[1]=="hlt" and pc!=m:
		#print(pc)
		print(f"Syntax error: line {pc+1} : hlt not being used as the last instruction")
		all_err.append(0)

	elif pc in invalid_var_arg:
		print(f"Syntax Error: line {pc+1}: Invalid number of arguments to declare a variable")
		all_err.append(0)

	elif pc in error_duplicate_lbl:
		print(f"General Syntax Error: line {pc+1}: Redeclaration of already declared label.")
		all_err.append(0)

	elif  len(i)==2 and i[1] in variables:
		all_err.append(1)

	elif len(i)>1 and i[0][:-1] in labels:
		all_err.append(cf.check_intruc(i[1:],pc+1,variables,labels))
		
	else:
		all_err.append(cf.check_intruc(i,pc+1,variables,labels))
	pc+=1

count=0

# print(all_err)
# print(len(all_err))
#print("fvffffsf")

if 0 in all_err:
	exit()


for i in all_err:
	if i==1:
		count+=1
		continue
	
	elif i=="A":
		if(list_instruction[count][0][0:-1] not in labels):
			print(mc.inst_A(list_instruction[count]))
		else:
			print(mc.inst_A(list_instruction[count][1:]))

	elif i=="B":
		if(list_instruction[count][0][0:-1] not in labels):
			print(mc.inst_B(list_instruction[count]))
		else:
			print(mc.inst_B(list_instruction[count][1:]))
	
	elif i=="C":
		if(list_instruction[count][0][0:-1] not in labels):
			print(mc.inst_C(list_instruction[count]))
		else:
			print(mc.inst_C(list_instruction[count][1:]))
		
	elif i=="D":
		if(list_instruction[count][0][0:-1] not in labels):
			a=""
			a+=mc.inst_D(list_instruction[count])
			b=int(variables[list_instruction[count][2]])
			c=str(mc.dec_to_bin(b))
			a+=(8-len(c))*"0"
			a+=c

		else:
			a=""
			a+=mc.inst_D(list_instruction[count][1:])
			b=int(variables[list_instruction[count][3]])
			c=str(mc.dec_to_bin(b))
			a+=(8-len(c))*"0"
			a+=c
	
		print(a)
	
	elif i=="E":
		if(list_instruction[count][0][0:-1] not in labels):
			a=""
			a+=mc.inst_E(list_instruction[count])
			a+="000"
			b=int(labels[list_instruction[count][1]])
			c=str(mc.dec_to_bin(b))
			a+=(8-len(c))*"0"
			a+=c

		else:
			a=""
			a+=mc.inst_E(list_instruction[count][1:])
			a+="000"
			b=int(labels[list_instruction[count][2]])
			# print(b)
			c=str(mc.dec_to_bin(b))
			# print(c)
			a+=(8-len(c))*"0"
			a+=c
	
		print(a)

	elif i=="F":
		print(mc.inst_F(list_instruction[count]))
		
	count+=1
	