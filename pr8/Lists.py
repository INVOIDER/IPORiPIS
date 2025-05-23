# Задача 1: Найти первое вхождение 20 и заменить его на 200
nums1 = [5, 10, 20, 25, 20, 30]
if 20 in nums1:
    index = nums1.index(20)
    nums1[index] = 200
print("Задача 1:", nums1)

# Задача 2: Удалить пустые строки из списка строк
strs = ["hello", "", "world", "", "python", " "]
cleaned_strs = list(filter(lambda x: x.strip(), strs))  # Убираем пустые и состоящие только из пробелов строки
print("Задача 2:", cleaned_strs)

# Задача 3: Превратить список чисел в список квадратов
nums2 = [1, 2, 3, 4, 5]
squared_nums = [x**2 for x in nums2]
print("Задача 3:", squared_nums)

# Задача 4: Удалить все вхождения числа 20
nums3 = [10, 20, 30, 20, 40, 20, 50]
filtered_nums = [x for x in nums3 if x != 20]
print("Задача 4:", filtered_nums)
