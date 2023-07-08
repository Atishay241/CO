def convertToInt(mantissa_str):
	power_count = -1
	mantissa_int = 0
	for i in mantissa_str:

		mantissa_int += (int(i) * pow(2, power_count))
		power_count -= 1
		
	return (mantissa_int + 1)

if __name__ == "__main__":

	num = '11101011'

	expo_bias = int(num[0 :3 ], 2)

	expo_unbias = expo_bias - 4

	mantissa_str = num[3 : ]

	mantissa_int = convertToInt(mantissa_str)

	real_no = mantissa_int * pow(2, expo_unbias)
	print(type(real_no))

	print(real_no)