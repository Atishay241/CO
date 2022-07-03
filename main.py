
def check_var_name(word):
	for i in word:
		if i not in valid_var_name:
			return False
	return True

def dict_making(list_instruction,count,var_flag,variables,var_num):
	for i in list_instruction:
		print(i)
		if(len(i)==2 and i[0]=="var" and var_flag==1 and i[1] not in variables):
			variables[i[1]]=0
			var_num+=1

		elif(len(i)==2 and i[0]=="var" and var_flag==1 and i[1] in variables):
			print("General Syntax Error: Redeclaration of already declared variable.")

		elif(len(i)==2 and i[0]=="var" and var_flag==0):
			print("Syntax Error: Variables not declared at the beginning and being declared in between")

		elif (len(i)==2 and i[0]!="var"):
			instructions.append(i)
			count+=1

		elif (len(i)==1 and i[0][-1]==":" and i[0][:-1] not in labels):
			labels[i[0][:-1]]=0
			count+=1

		elif (len(i)==1 and i[0][-1]==":" and i[0][:-1] in labels):
			print("General Syntax Error: Redeclaration of already declared label.")
			count+=1

		else:
			instructions.append(i)
			count =count+1
	return count,var_num


if __name__ == '__main__':
	import inst_type_check as check
	import fileinput
	import string

	list_instruction = []

	valid_var_name = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_')

	instructions = []
	variables = {}
	var_num=0
	labels = {}
	count=0

	pc = 0

	var_flag=1
	with fileinput.input(files=('test.txt')) as f:
		for line in f:
			l=line.split()
			list_instruction.append(l)
			#print(list_instruction[pc])
			pc += 1
	count,var_num=dict_making(list_instruction,count,var_flag,variables,var_num)
	print(count)
	print(var_num)
	for i in instructions:
		print(i)