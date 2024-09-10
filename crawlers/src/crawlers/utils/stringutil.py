import random
import string

"""
生成由数字组成的随机字符串.
"""
def generateRandomNumericString(length=22):
    return ''.join(random.choices(string.digits, k=length))