from collections import Counter
l = []
with open('ciphertext_71.txt') as f:
    data = f.read()
    # for lines in f.readlines():
    #     l.append(lines)

"""
for this manual approach is followed

first the obvious thing is to find the frequency of each characters in my text (please find it at the end of the code)
then obvious thing would be to replace the most occured with space as it is a direct hint from the paragraph as well that most occuring is the space
then replace the second most occuring is replaced by 'e'. luckily I got 'e' as the most occuring in my text itself so i did nothing in that regard

then after that I tried to observe the text manually and found that most of words are separated due to replacing with space and most of them has e
so most common approach to analyze the separated word based on intuition and guess and I kept on manually replacing the text and each time new words open for me and I tried to guess them and replace them and so on after continuously doing it the text eventually decrypted 

at the end of decryption I got the same webpage as well on google and was easily able to look for the shuffled string of alphabets and that was the key.

"""


# print(data.replace(' ',""))
# print(sum(map(int,list(Counter(data).values()))))
# print(Counter(data))
# print(len(Counter(data).keys()))

# replc = [('P',' '),('e','t'),('`','a'),('c','o'),('\\','j'),('#','n'),('&','c'),('C','K'),('8','d'),('3','e'),('9','a')]
# replc = [('P',' '),('/','T'),('I','h'),('c','t'),('8','i'),('#','s')]
replc = [('P',' '),('M','1'),('Y','2'),(';','3'),('|','4'),('U','5'),('F','6'),('<','7'),('t','.'),('N','8'),('c','t'),('I','h'),('\n','\n'),('e','e'),('3','n'),('q','C'),('L','o'),('#','s'),('u','A'),('9','r'),('?','f'),('\\','m'),('X','d'),('8','i'),('T','l'),('+','w'),('d','y'),('a','k'),('1','R'),('j','c'),('`','a'),('4','S'),('l','Q'),('C','u'),('&','g'),('r','q'),(' ','p'),('%','b'),('Z','L'),('/','T'),('b','I'),(')','x'),("'",','),('6','v'),('k','M'),('g','H'),('_','G'),('>',"F"),('~','['),('O',']'),('i','9'),('[','0'),('@','w'),('A','z'),('7','"'),('w','N'),(',','X'),('E','B'),('D','-'),('(','D'),('B',"'"),('5','!'),('V','Z'),('y','j')]


with open('ciphercode.txt') as f:
    dodata = f.read()



mydata = data
value = ""
mp = dict(replc)

for i in dodata:
    if i not in mp:
        print(i)
for i in mydata:
    if (i in mp):
        value += mp[i]
    else:
        value += "+"

with open('dec1.txt' ,'w') as f:
    f.write(value)


daata = ""
for i in data:
    if i in mp:
        daata += mp[i]
    else:
        daata += i

with open('decrypt.txt','w') as f:
    f.write(daata)
    


# print(data)
def dec(cipher):
    pass;


# Counter({'P': 4303, 'e': 2668, '`': 2115, 'c': 2058, '3': 1987, '8': 1800, '#': 1521, 'L': 1506, '9': 1370, 'T': 1063, '\\': 926, 'C': 923, 'j': 921, 'I': 840, 'X': 684, ' ': 608, '?': 419, '&': 410, '%': 305, 'd': 303, '+': 229, 'r': 208, "'": 183, '6': 183, 't': 175, '~': 123, 'O': 123, ')': 115, '\n': 115, 'a': 105, 
# 'D': 57, '/': 47, 'M': 45, 'Y': 42, 'k': 42, 'l': 41, 'A': 39, ';': 35, 'U': 33, 'u': 32, '|': 31, 'F': 31, 'b': 31, '[': 30, 'R': 30, '*': 30, '2': 29, 'v': 29, '"': 28, '<': 25, 'g': 24, 'E': 22, '4': 22, 'N': 21, 'w': 19, '>': 18, 'B': 18, '(': 18, '1': 17, 'i': 16, '_': 16, 'q': 15, '@': 14, '7': 12, 'z': 10, 'f': 9, '{': 9, 'K': 8, 'y': 6, '-': 6, 'H': 6, 'Z': 4, 's': 4, 'm': 4, ',': 3, 'h': 2, 'W': 2, 'n': 1, '.': 1, '5': 1, 'V': 1})
