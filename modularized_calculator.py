#! /usr/bin/python3

# プログラム説明:
#   数式を読み取ってトークン化（数字、演算子、かっこ）し、構文木化、評価を行うプログラム。

# read_number(line, index)
# 数字を読み取ってトークンとして返す。
# 入力:
#   line: 数式が含まれる文字列。
#   index: 数字の読み取りを開始するインデックス
# 出力:
#   数字トークンと次のインデックス
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

# read_plus(line, index), read_minus(line, index), read_multiplication(line, index), read_division(line, index)
# 演算子（+、-、*、/）を読み取ってトークンとして返す
# 入力:
#   line: 数式が含まれる文字列
#   index: 演算子の読み取りを開始するインデックス
# 出力:
#   演算子トークンと次のインデックス
def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiplication(line, index):
    token = {'type': 'MULTIPLICATION'}
    return token, index + 1

def read_division(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1

# read_left_parenthesis(line, index), read_right_parenthesis(line, index)
# 左括弧/右括弧を読み取ってトークンとして返す
# 入力:
#   line: 数式が含まれる文字列
#   index: 括弧の読み取りを開始するインデックス
# 出力:
#   括弧のトークンと次のインデックス
def read_left_parenthesis(line, index):
    token = {'type': 'LEFT_PARENTHESIS'}
    return token, index + 1

def read_right_parenthesis(line, index):
    token = {'type': 'RIGHT_PARENTHESIS'}
    return token, index + 1

# tokenize(line)
# 数式の文字列をトークンのリストに変換する。
# 入力:
#   line: 数式が含まれる文字列
# 出力:
#   トークンのリスト
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiplication(line, index)
        elif line[index] == '/':
            (token, index) = read_division(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parenthesis(line, index)
        elif line[index] == ')':
            (token, index) = read_right_parenthesis(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

# parse(tokens)
# トークンのリストを構文木に変換する。
# 入力:
#   tokens: トークンのリスト
# 出力:
#   構文木（リストの入れ子構造）
def parse(tokens):
    def parse_expression(tokens, index=0):
        elements = []
        while index < len(tokens):
            token = tokens[index]
            if token['type'] == 'NUMBER':
                elements.append(token['number'])
            elif token['type'] in ('PLUS', 'MINUS', 'MULTIPLICATION', 'DIVISION'):
                elements.append(token['type'])
            elif token['type'] == 'LEFT_PARENTHESIS':
                sub_expr, index = parse_expression(tokens, index + 1)
                elements.append(sub_expr)
            elif token['type'] == 'RIGHT_PARENTHESIS':
                return elements, index
            index += 1
        return elements, index
    parsed_expression, _ = parse_expression(tokens)
    return parsed_expression

# evaluate(expression)
# 構文木を評価して数式の結果を計算する。
# 入力:
#   expression: かっこの入れ子構造を含めた構文木
# 出力:
#   数式の計算結果
def evaluate(expression):
    if isinstance(expression, list):
        while len(expression) > 1:
            for i in range(len(expression)):
                if expression[i] == 'MULTIPLICATION':
                    left = evaluate(expression[i-1])
                    right = evaluate(expression[i+1])
                    expression = expression[:i-1] + [left * right] + expression[i+2:]
                    break
                elif expression[i] == 'DIVISION':
                    left = evaluate(expression[i-1])
                    right = evaluate(expression[i+1])
                    expression = expression[:i-1] + [left / right] + expression[i+2:]
                    break
            else:
                for i in range(len(expression)):
                    if expression[i] == 'PLUS':
                        left = evaluate(expression[i-1])
                        right = evaluate(expression[i+1])
                        expression = expression[:i-1] + [left + right] + expression[i+2:]
                        break
                    elif expression[i] == 'MINUS':
                        left = evaluate(expression[i-1])
                        right = evaluate(expression[i+1])
                        expression = expression[:i-1] + [left - right] + expression[i+2:]
                        break
    return expression[0] if isinstance(expression, list) else expression

# test(line)
# 数式を評価し、Pythonのeval関数による期待される結果と比較する。
# 入力:
#   line: 数式が含まれる文字列
# 出力:
#   期待される結果とプログラム内のevaluate関数で計算した結果との比較
def test(line):
    tokens = tokenize(line)
    parsed_expression = parse(tokens)
    actual_answer = evaluate(parsed_expression)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

# run_test()
# いくつかのテストケースを実行して結果を表示する。
# 入力: なし
# 出力: なし
def run_test():
    print("==== Test started! ====")
    test("1+2")  # Simple addition
    test("1.0+2.1-3")  # Addition and subtraction with floating points
    test("2*3")  # Simple multiplication
    test("4/2")  # Simple division
    test("2+3*4")  # Mixed addition and multiplication
    test("10/2-3")  # Mixed division and subtraction
    test("10/2*3")  # Mixed division and multiplication
    test("2*3+1")  # Multiplication followed by addition
    test("2*(3+1)")  # Multiplication with parentheses
    test("4/(2+2)")  # Division with parentheses
    test("4/(2.0+2.0)")  # Division with floating point and parentheses
    test("3.5*2-1.2/0.6")  # Complex expression with floating point
    test("10-3+5")  # Mixed subtraction and addition
    test("10-(3+5)")  # Subtraction with parentheses
    test("(2+3)*4")  # Addition within parentheses followed by multiplication
    test("2*(3+4*(2-1))")  # Complex expression with multiple operations and parentheses
    test("10/3")  # Division resulting in a floating point number
    test("3+4*2/(1-5)")  # Complex expression with all four operations and parentheses
    test("(3.5+2.5)/(2.0-1.0)")  # Addition and subtraction within parentheses
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    parsed_expression = parse(tokens)
    answer = evaluate(parsed_expression)
    print("answer = %f\n" % answer)
