my_list = [i for i in range(-5,11)]
k=2

my_map={}
result =[]
for i in my_list:
    if my_map.get(i-k)!=None:
        result.append( (i,i-k))
        my_map[i]=[]
    else :
        my_map[i]=[]

print(result)
