with open('new.txt', 'w') as file_object:
    i = 0
    import logging

    while True:
        file_object.write('%s' % i * 40 + "\n")  # 写入第一次: 只能写入字符串, 其他数据类型需要cast
        logging.info(111)
        i += 1
