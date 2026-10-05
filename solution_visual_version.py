import pygame
import math
from collections import defaultdict

pygame.init()

# --- 參數設定 ---
options = [3, 4, 5, 6, 7, 8]
select_sides = None
dropdown_open = False
submit = False
error_message = ""
error_time = 0
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Horizontal_line_info = []
level_map = {"v": 1, "u": 2, "t": 3, "s": 4, "r": 5}
level_str = ["v", "u", "t", "s", "r"]
input_text = ""
input_number = ""
number_list = []
lotID_list = []
number_move_pos = None
number_cur_level = 1
number_cur = None
move = False
swap = defaultdict(dict)
number_move_state = "vertical"
move_finished = False
active_input = 1
number_go = None
can_go = False
number_go_pre_state = None

width = 1280
height = 960
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("八卦鬼腳圖")

# --- 調色盤 (質感配色) ---
C_BG = (248, 249, 250)         # 背景微灰白
C_TEXT = (33, 37, 41)          # 主文字深灰
C_PRIMARY = (37, 99, 235)      # 經典科技藍
C_BORDER = (209, 213, 219)     # 質感邊框灰
C_WHITE = (255, 255, 255)      # 卡片純白
C_HOVER = (239, 246, 255)      # 選單懸停淺藍
C_DISABLED = (229, 231, 235)   # 禁用狀態灰

# --- 字型 ---
font_select = pygame.font.SysFont("arial", 20, bold=True)
font_label = pygame.font.SysFont("arial", 13, bold=True)
font_submit = pygame.font.SysFont("arial", 18, bold=True)
font_error_message = pygame.font.SysFont("arial", 20, bold=True)
font_lotID = pygame.font.SysFont("arial", 15, bold=True)
font_text_input = pygame.font.SysFont("arial", 40, bold=True)
font_text_number = pygame.font.SysFont("arial", 50, bold=True)
font_text_final_lotID = pygame.font.SysFont("arial", 30, bold=True)
font_level = pygame.font.SysFont("arial", 24, bold=True)  

# --- 矩型定義 (適度邊距) ---
rect_select = pygame.Rect(20, 30, 160, 42)
rect_submit = pygame.Rect(190, 30, 110, 42)
rect_input_Horizontal_line_info = pygame.Rect(0, 910, 250, 50)
rect_error_message = pygame.Rect(0, 0, 150, 40)
rect_move = pygame.Rect(1200, 0, 80, 40)
rect_input_number = pygame.Rect(1150, 0, 50, 40)
rect_text_final_lotID = pygame.Rect(900, 820, 350, 80)

def draw_select(select_sides, dropdown_open, options, submit):
    mouse_pos = pygame.mouse.get_pos()
    
    # 頂部小標籤
    lbl = font_label.render("POLYGON SIDES", True, (107, 114, 128))
    screen.blit(lbl, (rect_select.x, rect_select.y - 18))

    # 主按鈕狀態判斷
    is_hover = rect_select.collidepoint(mouse_pos) and not submit
    if submit:
        bg_col, border_col = C_DISABLED, C_BORDER
    elif is_hover or dropdown_open:
        bg_col, border_col = C_WHITE, C_PRIMARY
    else:
        bg_col, border_col = C_WHITE, C_BORDER

    # 繪製主卡片 (導圓角 8px)
    pygame.draw.rect(screen, bg_col, rect_select, border_radius=8)
    pygame.draw.rect(screen, border_col, rect_select, width=2, border_radius=8)

    # 顯示文字
    t_str = f"{select_sides} Sides" if select_sides else "Select..."
    t_color = (156, 163, 175) if submit else C_TEXT
    txt = font_select.render(t_str, True, t_color)
    screen.blit(txt, (rect_select.x + 14, rect_select.y + (rect_select.height - txt.get_height()) // 2))

    # 箭頭圖示
    arrow_str = "▲" if dropdown_open else "▼"
    arrow = font_label.render(arrow_str, True, border_col if not submit else (156, 163, 175))
    screen.blit(arrow, (rect_select.right - 22, rect_select.y + (rect_select.height - arrow.get_height()) // 2))

    # 下拉選單選單本體
    if dropdown_open and not submit:
        for i, opt in enumerate(options):
            opt_rect = pygame.Rect(rect_select.x, rect_select.y + rect_select.height + 6 + i * 38, rect_select.width, 38)
            opt_hover = opt_rect.collidepoint(mouse_pos)
            
            bg = C_HOVER if opt_hover else C_WHITE
            r_top = 8 if i == 0 else 0
            r_bot = 8 if i == len(options) - 1 else 0

            pygame.draw.rect(screen, bg, opt_rect, border_top_left_radius=r_top, border_top_right_radius=r_top, border_bottom_left_radius=r_bot, border_bottom_right_radius=r_bot)
            pygame.draw.rect(screen, C_BORDER, opt_rect, width=1, border_top_left_radius=r_top, border_top_right_radius=r_top, border_bottom_left_radius=r_bot, border_bottom_right_radius=r_bot)

            item_txt = font_select.render(f"{opt} Sides", True, C_PRIMARY if opt_hover else C_TEXT)
            screen.blit(item_txt, (opt_rect.x + 14, opt_rect.y + (opt_rect.height - item_txt.get_height()) // 2))

def draw_submit(submit):
    mouse_pos = pygame.mouse.get_pos()
    is_hover = rect_submit.collidepoint(mouse_pos)
    
    if submit:
        bg, text_str = (209, 213, 219), "Confirmed"
    else:
        bg = (29, 78, 216) if is_hover else C_PRIMARY
        text_str = "Submit"

    pygame.draw.rect(screen, bg, rect_submit, border_radius=8)
    txt = font_submit.render(text_str, True, (255, 255, 255))
    screen.blit(txt, (rect_submit.x + (rect_submit.width - txt.get_width()) // 2, rect_submit.y + (rect_submit.height - txt.get_height()) // 2))

def draw_error_message(error_message, error_time):
    if error_message != "":
        if pygame.time.get_ticks() - error_time < 3000:
            surface_error_message = font_error_message.render(error_message, True, (220, 38, 38))
            text_rect = surface_error_message.get_rect(center=(width // 2, 890))
            screen.blit(surface_error_message, text_rect)

def draw_regular_polygon(radius, sides):
    if sides is None:
        sides = 8
    vertexs = []
    connect_points = []
    center = (width / 2, height / 2)
    
    # 層級名稱，最內側(j=5)為 r，最外側(j=1)為 v
    # 建立對應：j=1 -> v, j=2 -> u, j=3 -> t, j=4 -> s, j=5 -> r
    level_labels = ["v", "u", "t", "s", "r"]

    for i in range(sides):
        angle = math.radians(-i * 360 / sides)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertex_info = {"line": i + 1, "pos": (x, y)}
        vertexs.append(vertex_info)

        text_number = font_text_number.render(str(vertex_info["line"]), True, (225, 29, 72))
        text_number_rect = text_number.get_rect(center=(vertex_info["pos"]))
        screen.blit(text_number, text_number_rect)

    vertex_points = [v["pos"] for v in vertexs]
    pygame.draw.polygon(screen, C_TEXT, vertex_points, width=4)

    for i, point in enumerate(vertex_points):
        dx = point[0] - center[0]
        dy = point[1] - center[1]
        line_start = (center[0] + dx * 0.12, center[1] + dy * 0.12)
        pygame.draw.line(screen, C_TEXT, line_start, point, width=4)
        circle_start = (center[0] + dx * 0.09, center[1] + dy * 0.09)
        pygame.draw.circle(screen, C_TEXT, (circle_start[0], circle_start[1]), 15, 4)
        text_lotID = font_lotID.render(letters[i], True, (225, 29, 72))
        text_lotID_rect = text_lotID.get_rect(center=(circle_start[0], circle_start[1]))
        screen.blit(text_lotID, text_lotID_rect)

        for j in range(1, 6):
            t = j / 6
            px = point[0] - (point[0] - center[0]) * t
            py = point[1] - (point[1] - center[1]) * t
            pygame.draw.circle(screen, C_PRIMARY, (px, py), 5)

            # --- 新增：僅在第 1 條線 (i == 0) 的藍點旁邊標示層級代號 ---
            if i == 0:
                label_text = level_labels[j - 1]  # j=1對應"v", j=5對應"r"
                text_lbl = font_level.render(label_text, True, (0, 0, 0))
                # 將文字稍微偏移放在藍點旁邊 (+12, -8)
                screen.blit(text_lbl, (px + 12, py - 8))

            connect_point_info = {"line": i + 1, "level": j, "pos": (px, py)}
            connect_points.append(connect_point_info)

    return vertexs, connect_points

def draw_error_message_connect(text_input, Horizontal_line_info, number_list):
    parts = text_input.split(",")
    if len(parts) != 3:
        return "Format error! Input format: i (integer), j (integer), x (character)", pygame.time.get_ticks(), Horizontal_line_info
    i, j, x = text_input.split(",")
    if not (i.isdigit() and j.isdigit()):
        return "Format error! i、j are integer", pygame.time.get_ticks(), Horizontal_line_info
    if x not in level_map:
        return "Format error! x is v/u/t/s/r", pygame.time.get_ticks(), Horizontal_line_info
    
    if abs(int(i) - int(j)) in (1, (number_list[-1] - number_list[0])) and (int(i) in number_list) and (int(j) in number_list):
        i, j = int(i), int(j)
        if i > j:
            i, j = j, i

        conflict = False
        for V_i, V_j, level in Horizontal_line_info:
            if x != level:
                continue
            if V_i in (i, j) or V_j in (i, j):
                conflict = True
                break

        if not conflict:
            Horizontal_line_info.append((i, j, x))
            return "draw connect line successful!!", pygame.time.get_ticks(), Horizontal_line_info
        else:
            return "Format error! Duplicate horizontal line", pygame.time.get_ticks(), Horizontal_line_info
    else:
        return f"Format error! V_i and V_j Must be adjacent and within range {number_list}", pygame.time.get_ticks(), Horizontal_line_info

def draw_connections(points, data):
    point_dict = {(p["line"], p["level"]): p["pos"] for p in points}
    for i, j, x in data:
        level = level_map[x]
        pygame.draw.line(screen, (225, 29, 72), point_dict[(i, level)], point_dict[(j, level)], 4)

def draw_text_input(input_text):
    pygame.draw.rect(screen, C_WHITE, rect_input_Horizontal_line_info, border_radius=6)
    pygame.draw.rect(screen, C_BORDER, rect_input_Horizontal_line_info, 2, border_radius=6)
    text_text_input = font_text_input.render(input_text, True, C_TEXT)
    screen.blit(text_text_input, (60, 910))

def draw_text_number(input_number):
    pygame.draw.rect(screen, C_WHITE, rect_input_number, border_radius=6)
    pygame.draw.rect(screen, C_BORDER, rect_input_number, 2, border_radius=6)
    text_text_number = font_text_input.render(input_number, True, C_TEXT)
    text_rect = text_text_number.get_rect(center=rect_input_number.center)
    screen.blit(text_text_number, text_rect)

def draw_number_move(vertexs, connect_points, number_move_pos, number_cur_level, number_cur, swap, number_move_state, move_finished, number_go, move):
    number_go = number_go - 1    
    vertexs_points = [v["pos"] for v in vertexs]
    vertexs_lines = [v["line"] for v in vertexs]
    center = (width / 2, height / 2)

    point_dict = {(p["line"], p["level"]): p["pos"] for p in connect_points}

    text_number = font_text_number.render(str(vertexs_lines[number_go]), True, (225, 29, 72))
    text_number_rect = text_number.get_rect(center=(vertexs_points[number_go]))
    
    if number_move_pos is None:
        number_move_pos = list(vertexs_points[number_go])
        number_cur = vertexs_lines[number_go]
    if number_cur_level < 6:
        if number_move_state == "vertical":
            target_pos = point_dict[number_cur, number_cur_level]
            speed = 0.005
            number_move_pos[0] += (target_pos[0] - number_move_pos[0]) * speed
            number_move_pos[1] += (target_pos[1] - number_move_pos[1]) * speed
            text_number_rect = text_number.get_rect(center=number_move_pos)
            screen.blit(text_number, text_number_rect)
            if math.dist(number_move_pos, target_pos) < 2:
                if number_cur in swap[level_str[number_cur_level - 1]]:
                    number_move_state = "horizontal"
                else:
                    number_cur_level += 1
        elif number_move_state == "horizontal":
            number_cur_change = swap[level_str[number_cur_level - 1]][number_cur]
            target_pos = point_dict[number_cur_change, number_cur_level]
            speed = 0.005
            number_move_pos[0] += (target_pos[0] - number_move_pos[0]) * speed
            number_move_pos[1] += (target_pos[1] - number_move_pos[1]) * speed
            text_number_rect = text_number.get_rect(center=number_move_pos)
            screen.blit(text_number, text_number_rect)
            if math.dist(number_move_pos, target_pos) < 2:
                number_cur = number_cur_change
                number_cur_level += 1
                number_move_state = "vertical"
    elif number_cur_level == 6:
        dx = vertexs_points[number_cur - 1][0] - center[0]
        dy = vertexs_points[number_cur - 1][1] - center[1]
        target_pos = (center[0] + dx * 0.09, center[1] + dy * 0.09)
        speed = 0.005
        number_move_pos[0] += (target_pos[0] - number_move_pos[0]) * speed
        number_move_pos[1] += (target_pos[1] - number_move_pos[1]) * speed
        text_number_rect = text_number.get_rect(center=number_move_pos)
        screen.blit(text_number, text_number_rect)
        if math.dist(number_move_pos, target_pos) < 2:
            number_cur_level += 1

    elif number_cur_level >= 7:
        move_finished = True

    if move_finished:
        text_final_lotID = font_text_final_lotID.render(f"The lot ID of participant No. {number_go+1} is {lotID_list[number_cur-1]}.", True, C_TEXT)
        text_text_final_lotID = text_final_lotID.get_rect(center=rect_text_final_lotID.center)
        screen.blit(text_final_lotID, text_text_final_lotID)
        move = False

    return number_move_pos, number_cur_level, number_cur, number_move_state, move_finished, move

def draw_error_input_number(input_number, number_list):
    if input_number == "":
        return "Please input number!", pygame.time.get_ticks(), None
    if not input_number.isdigit():
        return "Please input integer!", pygame.time.get_ticks(), None
    input_number = int(input_number)
    if input_number not in number_list:
        return f"Please input {number_list}!", pygame.time.get_ticks(), None
    return "Start!", pygame.time.get_ticks(), input_number

# --- 主迴圈 ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect_submit.collidepoint(event.pos):
                if select_sides is None:
                    error_message = "please select number of side first"
                    error_time = pygame.time.get_ticks()
                    submit = False
                else:
                    error_message = "Selection successful!!"
                    error_time = pygame.time.get_ticks()
                    number_list.clear()
                    lotID_list.clear()
                    for i in range(select_sides):
                        number_list.append(i + 1)
                        lotID_list.append(chr(ord('A') + i))
                    submit = True
            elif not submit:
                if rect_select.collidepoint(event.pos):
                    dropdown_open = not dropdown_open
                elif dropdown_open:
                    for i, number_select in enumerate(options):
                        opt_rect = pygame.Rect(rect_select.x, rect_select.y + rect_select.height + 6 + i * 38, rect_select.width, 38)
                        if opt_rect.collidepoint(event.pos):
                            select_sides = number_select
                            dropdown_open = False
                            break
                    else:
                        dropdown_open = False
            elif submit and rect_move.collidepoint(event.pos) and can_go:
                swap.clear()
                for V_i, V_j, level in Horizontal_line_info:
                    swap[level][V_i] = V_j
                    swap[level][V_j] = V_i
                move = True
                number_move_pos = None
                number_cur = None
                number_cur_level = 1
                number_move_state = "vertical"
                move_finished = False
                can_go = False

            if rect_input_Horizontal_line_info.collidepoint(event.pos):
                active_input = 1
            elif rect_input_number.collidepoint(event.pos):
                active_input = 2

        if submit and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if active_input == 1:
                    error_message, error_time, Horizontal_line_info = draw_error_message_connect(input_text, Horizontal_line_info, number_list)
                    input_text = ""
                elif active_input == 2:
                    error_message, error_time, number_go = draw_error_input_number(input_number, number_list)
                    input_number = ""
                    if number_go is not None:
                        can_go = True
            elif event.key == pygame.K_BACKSPACE:
                if active_input == 1:
                    input_text = input_text[:-1]
                elif active_input == 2:
                    input_number = input_number[:-1]
            else:
                if active_input == 1:                    
                    input_text += event.unicode
                elif active_input == 2:
                    input_number += event.unicode

    # --- 畫面更新與渲染 ---
    screen.fill(C_BG)

    vertexs, connect_points = draw_regular_polygon(radius=400, sides=select_sides)
    draw_connections(points=connect_points, data=Horizontal_line_info)
    draw_text_input(input_text=input_text)
    draw_text_number(input_number=input_number)
    draw_submit(submit)
    draw_error_message(error_message, error_time)

    if (move or move_finished) and number_go is not None:
        number_move_pos, number_cur_level, number_cur, number_move_state, move_finished, move = draw_number_move(
            vertexs, connect_points, number_move_pos, number_cur_level, number_cur, swap, number_move_state, move_finished, number_go, move
        )

    # 按鈕 GO 繪製
    go_bg = (34, 197, 94) if can_go else C_DISABLED
    pygame.draw.rect(screen, go_bg, rect_move, border_radius=6)
    pygame.draw.rect(screen, C_BORDER, rect_move, width=1, border_radius=6)
    screen.blit(font_submit.render("GO!", True, C_WHITE if can_go else (156, 163, 175)), (rect_move.x + 22, rect_move.y + 8))

    # 最後繪製 UI 選單 (確保選單層級最頂層)
    draw_select(select_sides, dropdown_open, options, submit)

    pygame.display.flip()

pygame.quit()