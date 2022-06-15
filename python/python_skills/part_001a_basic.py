import string

if __name__=='__main__':
    print(__file__ + "=>")

    # test the difference between built-in function reversed() and object method reverse()
    words = "Here are some words."
    print( reversed(words) )   # <reversed object at 0x0000023DC1295BE0>
    print( ''.join(reversed(words)))  # .sdrow emos era ereH
    print(words[::-1])                # .sdrow emos era ereH

    strlst = []
    for i in range (10):
        strlst.append(str(i))
    print('->'.join(strlst))
    print('->'.join(reversed(strlst)))
    strlst.reverse()  # in-place reverse() for iterable 
    print('->'.join(strlst))

    print(f"{('5' in strlst) = }")
    print(f"{('5' not in strlst) = }")
    print(f"{(not '5' in strlst) = }")
    
    print( f"{string.ascii_lowercase = }")
    print( f"{type(string.ascii_lowercase) = }")

    dic = {}
    for i, alpha in enumerate(string.ascii_lowercase):
        dic[alpha] = str(i)
    print("dic['a']: " + dic['a'])
    print("dic['z']: " + dic['z'])

    for key in dic:
        print('key: ' + key + ', val: ' + dic[key] )
    
    for key, val in dic.items():
        print(key, ' -> ', val)

    print(dic)

    print(':'.join(dic))

    print(dic.keys())
    print(dic.values())

    print('(k) '.join(dic.keys()))
    print('(v) '.join(dic.values()))

    print(f"{('e' in dic.keys()) = }")
    print(f"{('7' in dic.values()) = }")

    print(f"{ord('a') = }")
    print(f"{type(ord('a')) = }")

    # line = input("Please enter something:")
    # print(line)




    