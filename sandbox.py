import os
import re 

a = open(os.getcwd() + '/body.txt')
b = a.read()
a.close()
rge = '\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\d'
f = re.findall(rge, b)
print(type(f))
print(f)
quit()