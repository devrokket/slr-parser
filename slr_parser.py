# import requirements
import sys, json
import traceback

# 명령줄 인수 파싱
if len(sys.argv) != 2:
	print('사용 방법 : python slr_parser.py <input_file>\n')
	sys.exit(1)


# 전역 변수
txt_path = './' + sys.argv[1]
table_path = './' + "table.json"

parsing_table = None

remove = {
	0: ["CODE_START", "CODE"],
	1: ["CODE", "VDECL CODE"],
	2: ["CODE", "FDECL CODE"],
	3: ["CODE", ""],
	4: ["VDECL", "vtype id semi"],
	5: ["VDECL", "vtype ASSIGN semi"],
	6: ["ASSIGN", "id assign RHS"],
	7: ["RHS", "EXPR"],
	8: ["RHS", "literal"],
	9: ["RHS", "character"],
	10: ["RHS", "boolstr"],
	11: ["EXPR", "EXPR_1 addsub EXPR"],
	12: ["EXPR", "EXPR_1"],
	13: ["EXPR_1", "EXPR_2 multdiv EXPR_1"],
	14: ["EXPR_1", "EXPR_2"],
	15: ["EXPR_2", "lparen EXPR rparen"],
	16: ["EXPR_2", "id"],
	17: ["EXPR_2", "num"],
	18: ["FDECL", "vtype id lparen ARG rparen lbrace BLOCK RETURN rbrace"],
	19: ["ARG", "vtype id MOREARGS"],
	20: ["ARG", ""],
	21: ["MOREARGS", "comma vtype id MOREARGS"],
	22: ["MOREARGS", ""],
	23: ["BLOCK", "STMT BLOCK"],
	24: ["BLOCK", ""],
	25: ["STMT", "VDECL"],
	26: ["STMT", "ASSIGN semi"],
	27: ["STMT", "if lparen COND rparen lbrace BLOCK rbrace ELSE"],
	28: ["STMT", "while lparen COND rparen lbrace BLOCK rbrace"],
	29: ["COND", "COND_1 comp COND"],
	30: ["COND", "COND_1"],
	31: ["COND_1", "boolstr"],
	32: ["ELSE", "else lbrace BLOCK rbrace"],
	33: ["ELSE", ""],
	34: ["RETURN", "return RHS semi"],
}

# 파일 읽기
def read_file():
	global parsing_table

	try:
		with open(txt_path, 'r') as f:
			contents = f.read()
			print(f'입력된 문자열 : {contents}\n')
	except FileNotFoundError:
		print(f'[Error] {sys.argv[1]} 파일이 존재하지 않습니다.\n')

	try:
		with open(table_path, 'r') as f:
			parsing_table = json.load(f)
	except FileNotFoundError:
		print(f'[Error] parsing table 파일이 존재하지 않습니다.\n')

	token_arr = contents.split()
	token_arr.append("$")

	return token_arr


# parsing 로직
def parse(token_arr):
	stack = []
	token_idx = -1

	stack.append(0)
	while(1):
		token = token_arr[token_idx + 1]
		#print(f'stack : {stack}, token : {token}\n')

		# key error 발생 가능
		table_result = parsing_table[stack[-1]][token]

		if table_result == None:
			raise ValueError("파싱 실패")
		
		elif table_result[0] == "s":
			num = int(table_result[1:])
			stack.append(num)
			token_idx += 1
		
		elif table_result[0] == "r":
			num = int(table_result[1:])
			pop_count = len(remove[num][1].split())
			print(f'Remove #{num} : {remove[num][0]} <= {"ε" if remove[num][1] == "" else remove[num][1]}')

			# index error 발생 가능
			for _ in range(pop_count):
				stack.pop()

			# key error 발생 가능
			goto = parsing_table[stack[-1]][remove[num][0]]
			if goto == None:
				raise ValueError("파싱 실패")
			else:
				# 숫자라고 가정
				stack.append(int(goto))

		elif table_result == "acc":
			print("Accept!!!")
			return

		else:
			raise ValueError("WHAT THE HELL")


# main
def main():
	token_arr = read_file()
	parse(token_arr)
	print("\n프로그램 종료.\n")


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\n\n프로그램을 종료합니다.\n')
	except Exception as e:
		print(f'[Error] 예상치 못한 에러가 발생했습니다. 에러 메시지 : {e}\n')
		traceback.print_exc()