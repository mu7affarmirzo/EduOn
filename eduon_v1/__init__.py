# my_list = [1,3,42,100, 200, 700, 1000, 1200]
#
# found = False
# count = 0
# key = 1200
#
# mid = len(my_list)//2
# index = 0
#
# while not found:
#     if key not in my_list:
#         print('The key is not in list')
#         break
#     elif key in my_list[index:mid]:
#         count += 1
#         mid = mid//2
#         if key == my_list[mid]:
#             count += 1
#             found = True
#             break
#     elif key in my_list[mid:]:
#         count += 1
#         if key == my_list[mid]:
#             found = True
#             print(f'count: {count}')
#             break
#         index = mid
#         mid += (len(my_list) - mid)//2
#         print(f'index : {index}')
#         print(f'mid : {mid}')
#
