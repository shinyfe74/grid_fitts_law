import tkinter as tk
import pyautogui
import pygame
import time
import random
import os
import math


result_path = "./result"
os.makedirs(result_path, exist_ok=True)

form = tk.Tk()
form.title("타겟 클릭 실험")

pygame.init()


# 색상 설정
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)
White = (255, 255, 255)
Black = (0, 0, 0)

# 화면 비율 설정
screen_ratio = (16, 9)

monitor_height = form.winfo_screenheight()
monitor_width = form.winfo_screenwidth()

print("width x height = %d x %d (pixels)" %(monitor_width, monitor_height))

def calculate_r(monitor_size,ratiox=16, ratioy=9):
    x = pow(ratiox,2)
    y = pow(ratioy,2)
    result = x + y
    result = math.sqrt(pow(monitor_size,2)/result)
    calculated_r = 2.54 * result / 2    #최대 반지름
    calculated_x = ratiox * 2.54 * result    #가로길이
    calculated_y = ratioy * 2.54 * result    #세로길이
    return [round(calculated_r,2), round(calculated_x,1), round(calculated_y,1)]


# 피험자 입력
participant_Label = tk.Label(form, text="피험자번호:")
participant_Entry = tk.Entry(form)


#현재 모니터 정보
Target_size_info_label1 = tk.Label(form, text= "현재 해상도 기준 16:9 모니터별 최대 반지름 크기")
Target_size_info_label2 = tk.Label(form, text= "(15인치: {0}cm, 17인치: {1}cm, 24인치: {2}cm, 27인치:{3}cm)".format(calculate_r(15)[0], calculate_r(17)[0], calculate_r(24)[0], calculate_r(27)[0]))

# 타겟 최대 사이즈 입력
max_target_size = round(pyautogui.size()[0] / 16 / 37.79527559055 / 2, 3)
target_Label = tk.Label(form, text="타겟 반지름크기(cm단위)")
target_Entry = tk.Entry(form)

# 라인 유무 선택
line_Label = tk.Label(form, text="-----------------화면 격자 유무 선택------------------")
lineVar = tk.IntVar()
line0 = tk.Radiobutton(form, text="격자 무", variable=lineVar, value=1)
line1 = tk.Radiobutton(form, text="격자 유(기본)", variable=lineVar, value=2)
line1.select()

# 타겟 위치 고정 유무
target_location_Label = tk.Label(
    form, text="--------------격자내 타겟 위치------------------"
)
target_location_Var = tk.IntVar()
target_location0 = tk.Radiobutton(
    form, text="고정", variable=target_location_Var, value=1
)
target_location1 = tk.Radiobutton(
    form, text="랜덤", variable=target_location_Var, value=2
)
target_location0.select()

# 타겟 나타는 홈버튼
home_button_Label = tk.Label(form, text="-----------------홈버튼------------------")
home_button_Var = tk.IntVar()
home_button0 = tk.Radiobutton(form, text="없음(기본)", variable=home_button_Var, value=1)
home_button1 = tk.Radiobutton(form, text="있음", variable=home_button_Var, value=2)
home_button0.select()



# 스크린 비율
screen_ratio_Label = tk.Label(form, text="----------------화면 비율------------------")
screen_ratio_x_label = tk.Label(form, text="화면 가로 비율 (기본 16)")
screen_ratio_x_entry = tk.Entry(form)
screen_ratio_x_entry.insert(0, 16)
screen_ratio_y_label = tk.Label(form, text="화면 세로 비율 (기본 9)")
screen_ratio_y_entry = tk.Entry(form)
screen_ratio_y_entry.insert(0, 9)
monitor_size_label = tk.Label(form, text="모니터 사이즈(인치)")
monitor_size_entry = tk.Entry(form)
monitor_size_entry.insert(0, 31.5)



# 입력칸, 버튼 그리기

participant_Label.grid(row=0, column=0, padx=15, pady=15)
participant_Entry.grid(row=0, column=1, padx=15, pady=15)

Target_size_info_label1.grid(row=1, columnspan=3)
Target_size_info_label2.grid(row=2, columnspan=5)
target_Label.grid(row=3, column=0, padx=15, pady=15)
target_Entry.grid(row=3, column=1, padx=15, pady=15)

line_Label.grid(row=4, columnspan=3)
line0.grid(row=5, column=0, padx=15)
line1.grid(row=5, column=1, padx=15)

target_location_Label.grid(row=6, columnspan=3)
target_location0.grid(row=7, column=0, padx=15)
target_location1.grid(row=7, column=1, padx=15)

home_button_Label.grid(row=8, columnspan=3)
home_button0.grid(row=9, column=0, padx=15)
home_button1.grid(row=9, column=1, padx=15)

screen_ratio_Label.grid(row=10, columnspan=3)
screen_ratio_x_label.grid(row=11, column=0, padx=15, pady=15)
screen_ratio_x_entry.grid(row=11, column=1, padx=15, pady=15)
screen_ratio_y_label.grid(row=12, column=0, padx=15, pady=15)
screen_ratio_y_entry.grid(row=12, column=1, padx=15, pady=15)
monitor_size_label.grid(row=13, column=0, padx=15, pady=15)
monitor_size_entry.grid(row=13, column=1, padx=15, pady=15)


# 메인함수
def ex_set_without_home():

    pygame.init()
    # 폰트 지정
    number_font = pygame.font.SysFont("Monospace", 50)

    participant_number = participant_Entry.get()

    target_r_cm = float(target_Entry.get())

    screen_size = pyautogui.size()
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    screen_ratio = (int(screen_ratio_x_entry.get()), int(screen_ratio_y_entry.get()))
    pixel_size = calculate_r(float(monitor_size_entry.get()), screen_ratio[0],screen_ratio[1])[1]/monitor_width


    pygame.display.set_caption("fitts' law task")

    # 파일 생성

    result_file = open(
        "./result/result_%s_withoutHome.txt" % participant_number, "w", encoding="utf8"
    )
    result_file.write(
        "Participant_Number\t"
        + "Target_Number\t"
        + "Target_X\t"
        + "Target_Y\t"
        + "Point_X\t"
        + "Point_y\t"
        + "Distance(pixel)\t"
        + "Distance(cm)\t"
        + "Time\t"
        + "Trial\t"
        + "Success\n"
    )

    # 화면 분할 설정
    xplot = int(screen_size[0] / screen_ratio[0])
    yplot = int(screen_size[1] / screen_ratio[1])

    # 사각형 선택
    rect_x = random.randint(0, screen_ratio[0]-1)
    rect_y = random.randint(0, screen_ratio[1]-1)

    # 타겟 셋팅
    target_number = 1
    target_trial = 1

    # target_r_cm = 1
    target_r = int(target_r_cm / pixel_size)
    target_center = [0, 0]

    def Draw_target(target_location):
        if target_location == 1:
            target_x = int((2 * rect_x + 1) * xplot / 2)
            target_y = int((2 * rect_y + 1) * yplot / 2)

        elif target_location == 2:
            target_x = int(
                random.uniform(
                    rect_x * xplot + target_r, (rect_x + 1) * xplot - target_r
                )
            )
            target_y = int(
                random.uniform(
                    rect_y * yplot + target_r, (rect_y + 1) * yplot - target_r
                )
            )
        return [target_x, target_y]

    target_center = Draw_target(target_location_Var.get())

    # 이벤트 루프
    running = True  # 게임 진행중 체크

    # 시간 체크
    start_time = time.time()

    # 라인 그리기 함수
    def Draw_line():
        for y in range(10):
            pygame.draw.line(
                screen, Black, [0, yplot * y], [screen_size[0], yplot * y], 1
            )
        for x in range(17):
            pygame.draw.line(
                screen, Black, [xplot * x, 0], [xplot * x, screen_size[1]], 1
            )

    while running:

        target_x = target_center[0]
        target_y = target_center[1]

        for event in pygame.event.get():
            target_number_text = number_font.render(str(target_number), True, White)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # 거리계산
                mouse_vector = pygame.Vector2(
                    pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                )
                target_vector = pygame.Vector2(target_x, target_y)
                distance = mouse_vector.distance_to(target_vector)

                if distance <= target_r:
                    success_time = round(time.time() - start_time, 3)
                    start_time = time.time()
                    print("범위내")
                    print("마우스 위치 :", pygame.mouse.get_pos())
                    print("타겟 위치 : (", target_x, ", ", target_y, ")")
                    print("성공 횟수 : ", target_trial)
                    print("성공까지 시간 : ", success_time)

                    result_file.write(
                        "%s" % participant_number
                        + "\t"
                        + "%s" % target_number
                        + "\t"
                        + "%s" % target_x
                        + "\t"
                        + "%s" % (screen_size[1] - target_y)
                        + "\t"
                        + "%s" % mouse_vector[0]
                        + "\t"
                        + "%s" % (screen_size[1] - mouse_vector[1])
                        + "\t"
                        + "%s" % round(distance,3)
                        + "\t"
                        + "%s" % round((distance*pixel_size),3)
                        + "\t"
                        + "%s" % success_time
                        + "\t"
                        + "%s" % target_trial
                        + "\t"
                        + "%s" % 1
                        + "\n"

                    )

                    # 사각형 선택
                    rect_x = random.randint(0, 15)
                    rect_y = random.randint(0, 8)

                    # 타겟 리셋
                    target_center = Draw_target(target_location_Var.get())

                    target_number += 1
                    target_trial = 1

                else:
                    success_time = round(time.time() - start_time, 3)

                    print("범위밖")
                    print("마우스 위치 :", pygame.mouse.get_pos())
                    print("타겟 위치 : (", target_x, ", ", target_y, ")")
                    print("시도 횟수 :", target_trial)
                    
                    result_file.write(
                        "%s" % participant_number
                        + "\t"
                        + "%s" % target_number
                        + "\t"
                        + "%s" % target_x
                        + "\t"
                        + "%s" % (screen_size[1] - target_y)
                        + "\t"
                        + "%s" % mouse_vector[0]
                        + "\t"
                        + "%s" % (screen_size[1] - mouse_vector[1])
                        + "\t"
                        + "%s" % round(distance,3)
                        + "\t"
                        + "%s" % round((distance*pixel_size),3)
                        + "\t"
                        + "%s" % success_time
                        + "\t"
                        + "%s" % target_trial
                        + "\t"
                        + "%s" % 0
                        + "\n"
                    )

                    target_trial += 1

        screen.fill(White)

        if lineVar.get() == 2:
            Draw_line()

        pygame.draw.circle(screen, Blue, [target_x, target_y], target_r)

        # 공에 숫자 쓰기
        screen.blit(target_number_text, (target_x - 20, target_y - 30))

        pygame.display.update()

    result_file.close()

    pygame.quit()


def ex_set_with_home():
    pygame.init()
    # 폰트 지정
    number_font = pygame.font.SysFont("Monospace", 50)

    participant_number = participant_Entry.get()

    target_r_cm = float(target_Entry.get())

    screen_size = pyautogui.size()
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    screen_ratio = (int(screen_ratio_x_entry.get()), int(screen_ratio_y_entry.get()))
    pixel_size = calculate_r(float(monitor_size_entry.get()), screen_ratio[0],screen_ratio[1])[1]/monitor_width

    pygame.display.set_caption("fitts' law task")

    # 파일 생성

    result_file = open(
        "./result/result_%s_withHome.txt" % participant_number, "w", encoding="utf8"
    )
    result_file.write(
        "Participant_Number\t"
        + "Target_Number\t"
        + "Target_X\t"
        + "Target_Y\t"
        + "Point_X\t"
        + "Point_y\t"
        + "Distance\t"
        + "Time\t"
        + "Trial\t"
        + "Success\n"
    )

    # 화면 분할 설정
    xplot = int(screen_size[0] / screen_ratio[0])
    yplot = int(screen_size[1] / screen_ratio[1])

    # 사각형 선택
    rect_x = random.randint(0, screen_ratio[0]-1)
    rect_y = random.randint(0, screen_ratio[1]-1)

    # 타겟 셋팅
    target_number = 1
    target_trial = 1

    # target_r_cm = 1
    target_r = int(target_r_cm / pixel_size)
    target_center = [0, 0]

    def Draw_target(target_location):
        if target_location == 1:
            target_x = int((2 * rect_x + 1) * xplot / 2)
            target_y = int((2 * rect_y + 1) * yplot / 2)

        elif target_location == 2:
            target_x = int(
                random.uniform(
                    rect_x * xplot + target_r, (rect_x + 1) * xplot - target_r
                )
            )
            target_y = int(
                random.uniform(
                    rect_y * yplot + target_r, (rect_y + 1) * yplot - target_r
                )
            )
        return [target_x, target_y]

    target_center = Draw_target(target_location_Var.get())

    home_key = 1

    # 이벤트 루프
    running = True  # 게임 진행중 체크

    # 시간 체크
    start_time = time.time()

    # 라인 그리기 함수
    def Draw_line():
        for y in range(10):
            pygame.draw.line(
                screen, Black, [0, yplot * y], [screen_size[0], yplot * y], 1
            )
        for x in range(17):
            pygame.draw.line(
                screen, Black, [xplot * x, 0], [xplot * x, screen_size[1]], 1
            )

    while running:
        if home_key%2 == 1:
            target_x = int(screen_size[0]/2)
            target_y = int(screen_size[1]/2)
        elif home_key%2 ==0:
            target_x = target_center[0]
            target_y = target_center[1]

        for event in pygame.event.get():
            target_number_text = number_font.render(str(target_number), True, White)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    home_key = 1

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # 거리계산
                mouse_vector = pygame.Vector2(
                    pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                )
                target_vector = pygame.Vector2(target_x, target_y)
                distance = mouse_vector.distance_to(target_vector)

                if distance <= target_r:
                    success_time = round(time.time() - start_time, 3)
                    start_time = time.time()
                    print("범위내")
                    print("마우스 위치 :", pygame.mouse.get_pos())
                    print("타겟 위치 : (", target_x, ", ", target_y, ")")
                    print("성공 횟수 : ", target_trial)
                    print("성공까지 시간 : ", success_time)

                    result_file.write(
                        "%s" % participant_number
                        + "\t"
                        + "%s" % target_number
                        + "\t"
                        + "%s" % target_x
                        + "\t"
                        + "%s" % (screen_size[1] - target_y)
                        + "\t"
                        + "%s" % mouse_vector[0]
                        + "\t"
                        + "%s" % (screen_size[1] - mouse_vector[1])
                        + "\t"
                        + "%s" % round(distance,3)
                        + "\t"
                        + "%s" % round((distance*pixel_size),3)
                        + "\t"
                        + "%s" % success_time
                        + "\t"
                        + "%s" % target_trial
                        + "\t"
                        + "%s" % 1
                        + "\n"

                    )

                    # 사각형 선택
                    rect_x = random.randint(0, 15)
                    rect_y = random.randint(0, 8)

                    # 타겟 리셋
                    target_center = Draw_target(target_location_Var.get())

                    target_number += 1
                    target_trial = 1
                    home_key += 1

                else:
                    success_time = round(time.time() - start_time, 3)
                    print("범위밖")
                    print("마우스 위치 :", pygame.mouse.get_pos())
                    print("타겟 위치 : (", target_x, ", ", target_y, ")")
                    print("시도 횟수 :", target_trial)
                    
                    result_file.write(
                        "%s" % participant_number
                        + "\t"
                        + "%s" % target_number
                        + "\t"
                        + "%s" % target_x
                        + "\t"
                        + "%s" % (screen_size[1] - target_y)
                        + "\t"
                        + "%s" % mouse_vector[0]
                        + "\t"
                        + "%s" % (screen_size[1] - mouse_vector[1])
                        + "\t"
                        + "%s" % round(distance,3)
                        + "\t"
                        + "%s" % round((distance*pixel_size),3)
                        + "\t"
                        + "%s" % success_time
                        + "\t"
                        + "%s" % target_trial
                        + "\t"
                        + "%s" % 0
                        + "\n"
                    )

                    target_trial += 1

        screen.fill(White)

        if lineVar.get() == 2:
            Draw_line()

        if home_key%2 == 0:
            pygame.draw.circle(screen, Blue, [target_x, target_y], target_r)
        elif home_key%2 == 1:
            pygame.draw.circle(screen, Blue, [target_x, target_y], target_r)

        # 공에 숫자 쓰기
        screen.blit(target_number_text, (target_x - 20, target_y - 30))

        pygame.display.update()

    result_file.close()

    pygame.quit()



def Home():
    if home_button_Var.get() == 1:
        ex_set_without_home()
    elif home_button_Var.get() == 2:
        ex_set_with_home()


btn_start = tk.Button(form, text="실험 시작", command=Home)

btn_end = tk.Button(form, text="실험 종료", command=form.destroy)

btn_start.grid(columnspan=3, padx=15, pady=10)

btn_end.grid(columnspan=3, padx=15, pady=10)

form.mainloop()
