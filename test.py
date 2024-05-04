import sys

def getFirstDigit(string: str) -> int:
    for i in range(len(string)):
        if string[i].isdigit():
           return i
    
    return -1

def assertLicensePlate(string: str, first: int) -> bool:
    for i in range(first + 1, len(string)):
        if not string[i].isdigit():
            return False
    
    return True


string: str = "abcd1a12"
last: int = getFirstDigit(string)
if last == -1:
    sys.exit(1)
valid: bool = assertLicensePlate(string, last)
print(valid)