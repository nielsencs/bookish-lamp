fp = open("sample.txt", "r+")
#def get_lines(fp, line_numbers):
#    return (x for i, x in enumerate(fp) if i in line_numbers)
print('fp.tell:')
print(fp.tell())

#fp.write('Fi')

#print('fp.tell:')
#print(fp.tell())

print(fp.readlines()[0])

#fp.seek(10)
fp.write('*')

print('fp.tell:')
print(fp.tell())

fp.close()
