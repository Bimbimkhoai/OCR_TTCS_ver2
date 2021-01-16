from difflib import SequenceMatcher

text1 = open("banro1.txt")
text2 = open("ketqua.txt")


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


list1 = []
list2 = []
for t1 in text1:
    list1.append(t1.strip())
for t2 in text2:
    list2.append(t2.strip())
dong1 = similar(list1[0], list2[0])
if dong1 > 0.3 and len(list1) == len(list2):
    ratio_sum = 0
    len1 = len(list1)
    for i, l in enumerate(list2):
        m = similar(list1[i], list2[i])
        print("Bản rõ: ", list1[i])
        print("Kết quả:", list2[i])
        print("<===>do chinh xac tung khoa<====>", m)
        ratio_sum = ratio_sum + m

    average = (ratio_sum / len1) * 100
    print("Tỉ lệ chính xác trung bình đối với độ dài 32 ký tự, font chữ Courier, size 24 là:", average, "%")

else:
    text1 = open("banro1.txt").read()
    text2 = open("ketqua.txt").read()


    def similar(a, b):
        print(a)
        print("==========================")
        print(b)
        return SequenceMatcher(None, a, b).ratio()


    m = similar(text1, text2)
    print("[Không thể nhận diện hết] Tỉ lệ chính xác trung bình đối với độ dài 32 ký tự, font chữ Courier, size 24 là:", m*100,"%")
