def check(password: int)->bool:
    pw = [int(i) for i in str(password)]
    prev = pw[0]
    for i,digit in enumerate(pw[1:]):
        pw[i] = int(digit) - int(prev)
        prev = digit
    duplicate = False
    zeros = 0
    for i,digit in enumerate(pw):
        if digit < 0:
            return False
        if digit == 0:
            zeros += 1
        else:
            if zeros == 1:
                duplicate = True
            zeros = 0
    return duplicate or zeros == 2

def usingAddition(low: int,high: int)->int:
    curr = low
    count = 0
    while curr <= high:
        if check(curr):
            count += 1
        curr += 1
    return count


if __name__ == '__main__':
    print(usingAddition(273025,767253))

def test_check():
    testInput = 112233
    expected = True
    result = check(testInput)
    assert result == expected

    testInput = 123444
    expected = False
    result = check(testInput)
    assert result == expected

    testInput = 111122
    expected = True
    result = check(testInput)
    assert result == expected

