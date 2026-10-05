"""parameter"""
lotID = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
levels = ['v', 'u', 't', 's', 'r']
number = [1, 2, 3, 4, 5, 6, 7, 8]
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
    
    """先檢查是否相連以及數字範圍是否在1-8再檢查是否重複橫線"""
    if abs(int(i) - int(j)) in (1, 7) and (int(i) in number) and (int(j) in number):
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
        print("格式錯誤! V_i 與 V_j 必須相鄰且範圍 1-8")
        print(Horizontal_line_info)
        continue

print(f"Final Horizontal_line_info:\n{Horizontal_line_info}")

def find_lotID(cur_number: int, lotID: list[str], levels: list[str], Horizontal_line_info: list[tuple]):
    """根據參賽者編號，模擬爬梯子過程，回傳最終對應的籤號。
    Args:
        cur_number(int)                  : 目前參賽者號碼
        lotID(list[str])                 : 籤號列表
        levels(list[str])                : 層數的處理順序（由下往上或由上往下）
        Horizontal_line_info(list[tuple]): 每條橫線的資訊
    Return:
        finalID(str): 最終輸出
    """
    for level in levels:
        for V_i, V_j, level_info in Horizontal_line_info:
            if level == level_info:
                if cur_number == V_i:
                    cur_number = V_j
                    break
                elif cur_number == V_j:
                    cur_number = V_i
                    break
                else:
                    continue
            else:
                continue
    finalID = lotID[cur_number - 1]
    return finalID


for i in range(1, 9):
    cur_number = i
    number_lotID = find_lotID(cur_number, lotID, levels, Horizontal_line_info)
    print(f"No. {i} 參賽者之籤碼為[ {number_lotID} ]")