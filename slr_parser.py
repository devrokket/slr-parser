# import requirements
import sys


# 명령줄 인수 파싱
if len(sys.argv) != 2:
	print('사용 방법 : python slr_parser.py <input_file>\n')
	sys.exit(1)


# 전역 변수
txt_path = './' + sys.argv[1]
parsing_table = {} # 예시) "State 숫자" : [[{"ACTION의 non-terminal" : "행동", ...}],[{"GOTO의 terminal", "GOTO할 위치", ...}]]


# 파일 읽기
def read_file():
	try:
		with open(txt_path, 'r') as f:
			contents = f.read()
			print(f'입력된 문자열 : {contents}\n')

	except FileNotFoundError:
		print(f'[Error] {sys.argv[1]} 파일이 존재하지 않습니다.\n')

	return contents.split()


# parsing 로직
def parse(token_arr):
	pass


# main
def main():
	token_arr = read_file()
	parse(token_arr)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\n\n프로그램을 종료합니다.\n')
	except Exception as e:
		print(f'[Error] 예상치 못한 에러가 발생했습니다. 에러 메시지 : {e}\n')