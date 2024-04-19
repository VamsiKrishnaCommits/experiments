# my_list = [[1, None, 3], [4, 5, None, 6], [None, 7, 8, None]]

# result = [[1, 3], [4, 5, 6], [7, 8]]

# for list in my_list:
#     for element in list:
#         if not element:
#             list.remove(element)

# print(my_list)

#Variation

my_list = [[1, None, 3], [4, [None, 5, None], 6], [None, 7, [8, None]], 9, None, [None]]

def sanitize_list(my_list):
    result_list = []

    size = len(my_list)

    for i in range(size):
        if type(my_list[i]) == list:
            sanitized_list = sanitize_list(my_list[i])
            if len(sanitized_list)!=0:
                result_list.append(sanitized_list)
        
        elif my_list[i]:
            result_list.append(my_list[i])
    
    return result_list
        

print(sanitize_list(my_list=my_list))

