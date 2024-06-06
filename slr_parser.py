# import requirements
import sys, json
import traceback
from anytree import Node, RenderTree

# command parsing
if len(sys.argv) != 2:
	print('사용 방법 : python slr_parser.py <input_file>\n')
	sys.exit(1)

# global variables
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

# file reading
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


# parsing logic
def parse(token_arr):
	stack = []
	token_idx = -1

	# tree stack
	tree_stack = []

	stack.append(0)
	while(1):
		token = token_arr[token_idx + 1]
		table_result = parsing_table[stack[-1]][token]

		# There is no value in parsing table
		if table_result == None:
			raise ValueError("[Error] parsing table에 값이 존재하지 않습니다.\n")
		
		# Shift
		elif table_result[0] == "s":
			num = int(table_result[1:])
			stack.append(num)
			token_idx += 1

			# append tree node
			tree_stack.append(Node(token))
		
		# Reduce
		elif table_result[0] == "r":
			num = int(table_result[1:])
			pop_count = len(remove[num][1].split())

			# combine tree node
			children = []
			for _ in range(pop_count):
				stack.pop()
				children.append(tree_stack.pop())
			
			parent = Node(remove[num][0], children=children[::-1])
			tree_stack.append(parent)

			# GOTO
			goto = parsing_table[stack[-1]][remove[num][0]]
			if goto == None:
				raise ValueError("[Error] parsing table에 값이 존재하지 않습니다.\n")
			else:
				# assume number
				stack.append(int(goto))

		# Accept
		elif table_result == "acc":
			print("Accept!!!\n")
			print("Parse Tree: ")
			# print tree
			for pre, _, node in RenderTree(tree_stack[0]):
				print("%s%s" % (pre, node.name))
			return


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
		print(f'Rejected...\n\n{e}')
		traceback.print_exc()