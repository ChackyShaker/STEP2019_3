#数字を処理
def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
        number += int(line[index]) * keta
        keta /= 10
        index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index

#記号の種類分類
def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1
def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1
def readMulti(line, index):
  token = {'type': 'MULTI'}
  return token, index + 1
def readDivison(line, index):
  token = {'type': 'DIVISION'}
  return token, index + 1


#数字と記号で分類したリストを作成
def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '/':
      (token, index) = readDivison(line, index)
    elif line[index] == '*':
      (token, index) = readMulti(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)#エラーによる終了
    tokens.append(token)
  return tokens

#演算
def simplify_sub(tokens):
    tokens_junk =[]
    result = 0
    for i in range(len(tokens)):
        if tokens[i]['type'] == 'DIVISION':
            result += tokens[i-1]['number']/tokens[i+1]['number']
            tokens_junk.append(tokens[:i-1])
            tokens_junk.insert(i-1,result)
            tokens_junk.append(tokens[i:])
            break
        elif tokens[i]['type'] == 'MULTI':
            result += tokens[i-1]['number']*tokens[i+1]['number']
            tokens_junk.append(tokens[:i-1])
            tokens_junk.insert(i-1,result)
            tokens_junk.append(tokens[i:])
            break
        else:
            pass
    print(tokens_junk)

    

def simplify(tokens_junk):
    idx = 0
    if tokens_junk[idx]['type'] == 'DIVISION' or tokens_junk[idx]['type'] == 'MULTI':
        simplify_sub(tokens_junk)
    else:
        pass
    idx += 1
    return tokens_junk



def evaluate(tokens_junk):
    answer = 0
    tokens_junk.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens_junk):
        if tokens_junk[index]['type'] == 'NUMBER':
            if tokens_junk[index - 1]['type'] == 'PLUS':
                answer += tokens_junk[index]['number']
            elif tokens_junk[index - 1]['type'] == 'MINUS':
                answer -= tokens_junk[index]['number']
                #else:
                #print('Invalid syntax')
                #exit(1)
        index += 1
    return answer
                                        



#テスト入力
def test(line):
  tokens = tokenize(line)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))
# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("1+2/2")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  tokens_junk = simplify_sub(tokens)
  answer = evaluate(tokens_junk)
  print("answer = %f\n" % answer)

#

