import inst_type_check as check
def main():
	all_inst=[]
	a=[str(i) for i in input().split()]
	if check.check(a)=="F":
		exit()
	else:
		while(check.check(a)=="F"):
			a=[str(i) for i in input().split()]
			all_inst.append(a)
		


	

if _name_ == '_main_':
	main()