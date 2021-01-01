from difflib import SequenceMatcher

text1 = open("banro.txt")
text2 = open("ketqua.txt")


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

list1 = []
list2 = []
for t1 in text1:
    list1.append(t1.strip())
for t2 in text2:
    list2.append(t2.strip())
tong = 0
sodong = 0
for i, l in enumerate(list2):
    m = similar(list1[i], list2[i])
    print("Bản rõ: ", list1[i])
    print("Kết quả:", list2[i])
    # print(m)
    tong = tong + m
    sodong += 1

trungbinh = (tong / sodong) * 100

print("Tỉ lệ chính xác trung bình đối với độ dài 32 ký tự, font chữ Courier, size 24 là:", trungbinh, "%")



