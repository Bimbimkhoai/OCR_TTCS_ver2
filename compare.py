from difflib import SequenceMatcher

text1 = open("Banro.txt")
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
dem = 0
for i, l in enumerate(list1):
    m = similar(list1[i], list2[i])
    print("Bản rõ:", list1[i])
    print("Kết quả:", list2[i])

    # print(m)
    tong = tong + m
    dem += 1

trungbinh = tong / (dem)
print("Tỉ lệ chính xác", trungbinh)
print("Phương sai")
