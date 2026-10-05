from collections import defaultdict
example_1 = [
    (1, 8, "t"),
    (2, 3, "s"),
    (3, 4, "r"),
    (4, 5, "s"),
    (6, 7, "s"),
    (7, 8, "r"),
    (1, 8, "u"),
    (2, 3, "u"),
    (3, 4, "t"),
    (4, 5, "u"),
    (6, 7, "u"),
    (7, 8, "v"),
    (1, 2, "v"),
    (5, 6, "r"),
    (5, 6, "t"),
    (5, 6, "v")
]
example_2 = [
    (1, 2, "r"),
    (2, 3, "s"),
    (3, 4, "r"),
    (1, 8, "u"),
    (6, 7, "s"),
    (7, 8, "r"),
    (1, 2, "t"),
    (2, 3, "u"),
    (3, 4, "v"),
    (5, 6, "v"),
    (6, 7, "u"),
    (7, 8, "t"),
    (1, 2, "v"),
    (4, 5, "s"),
    (4, 5, "t"),
    (4, 5, "u")
]
"""parameter"""

levels = ['v', 'u', 't', 's', 'r']
number = []
lotID = []
"""調整邊數"""
print("請輸入邊數")
sides = input(">>> ")
for i in range (int(sides)):
    number.append(i + 1)
    lotID.append(chr(ord('A') + i))

"""輸入橫線資訊"""
Horizontal_line_info = []
print("請輸入橫線資訊，其輸入格式為 i (整數), j (整數), x (字元)")
while True:
    info = input(">>> ")

    if info.lower() == "q":
        break

    parts = info.split(",")

    """檢查格式"""
    if len(parts) != 3:
        print("格式錯誤! 輸入格式為 i (整數), j (整數), x (字元)")
        print(Horizontal_line_info)
        continue
    i, j, x = info.split(",")

    """檢查數字與層"""
    if not (i.isdigit() and j.isdigit()):
        print("格式錯誤! i、j 為整數")
        print(Horizontal_line_info)
        continue
    if x not in levels:
        print("格式錯誤!x 為 v/u/t/s/r")
        print(Horizontal_line_info)
        continue
    
    """先檢查是否相連以及數字範圍再檢查是否重複橫線"""
    if abs(int(i) - int(j)) in (1, (number[-1] - number[0])) and (int(i) in number) and (int(j) in number):
        i = int(i)
        j = int(j)
        if i > j:
            i, j = j, i

        conflict = False
        for V_i, V_j, level in Horizontal_line_info:
            if x != level:
                continue
            if  V_i in (i, j) or V_j in (i, j):
                conflict = True
                break
        """無重複可儲存橫線"""
        if conflict == False:
            Horizontal_line_info.append((i, j, x))
            print(Horizontal_line_info)
        else:
            print("格式錯誤! 重複橫線")
            print(Horizontal_line_info)
    else:
        print(f"格式錯誤! V_i 與 V_j 必須相鄰且範圍{number}{lotID}")
        print(Horizontal_line_info)
        continue
print(f"Final Horizontal_line_info:\n{Horizontal_line_info}")

def find_lotID(cur_number: int, lotID: list[str], levels: list[str], swap: dict[str, dict[int, int]]):
    """根據參賽者編號，模擬爬梯子過程，回傳最終對應的籤號。
    Args:
        cur_number(int)                  : 目前參賽者號碼
        lotID(list[str])                 : 籤號列表
        levels(list[str])                : 層數的處理順序（由下往上或由上往下）
        swap(dict)                       : 依照橫線層級分類的左右交換對應表
    Return:
        finalID(str): 最終輸出
    """
    for level in levels:
        if cur_number in swap[level]:
            cur_number = swap[level][cur_number]
    finalID = lotID[cur_number - 1]
    return finalID

"""建立交換表"""
swap = defaultdict(dict)
for V_i, V_j, level in example_1:
    swap[level][V_i] = V_j
    swap[level][V_j] = V_i

for i in range(1, len(number)+1):
    cur_number = i
    number_lotID = find_lotID(cur_number, lotID, levels, swap)
    print(f"No. {i} 參賽者之籤碼為[ {number_lotID} ]")