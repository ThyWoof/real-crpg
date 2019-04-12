import random as rd

def rollDice(pcs, num, correction):  # 주사위를 굴리는 함수입니다. 인수로 몇개인지 몇면체인지, 보정값을 받습니다.
    result = []
    for i in range(pcs):
        result.append(rd.randint(1, num))
    num = 0
    string = ''
    for i in result:
        num += i
        string += str(i) + ' + '
    num += correction
    string += str(correction) + ' = ' + str(num)
    print(string)
    return num  # 결과를 출력하며, 최종 값을 반환합니다.
