import time
import random
import tkinter as tk
from tkinter import messagebox
from plyer import notification
import keyboard
import pytz
from datetime import datetime

is_paused = False
paused_time = 0

def get_moscow_time():
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)
    return moscow_time.strftime("%Y-%m-%d %H:%M:%S")

def log_break(action, time_spent=None):
    moscow_time = get_moscow_time()
    with open("break_log.txt", "a") as log_file:
        if action == "break":
            log_file.write(f"Сделан перерыв в {moscow_time}. Всего прошло {time_spent} секунд работы.\n")
        elif action == "pause":
            log_file.write(f"Таймер поставлен на паузу в {moscow_time}.\n")
        elif action == "resume":
            log_file.write(f"Таймер возобновлен в {moscow_time}.\n")
        elif action == "stop":
            log_file.write(f"Программа завершена в {moscow_time}.\n")

def get_random_message():
    messages = [
        "Пора сделать перерыв! Встань и разомнись.",
        "Напоминаем: время сделать паузу.",
        "Как насчет короткой прогулки или растяжки?",
        "Остановись, сделай вдох и выдох.",
        "Хорошая работа! Но время сделать перерыв.",
        "Подумай о здоровье: время размяться.",
        "Перерыв поможет сохранить продуктивность.",
        "Вдохни глубоко. Время на перерыв.",
        "Ты молодец! Но небольшая пауза не повредит.",
        "Работа важна, но отдых важнее.",
        "Перерыв — это инвестиция в энергию.",
        "Время растянуться или прогуляться.",
        "Напоминаем: здоровье превыше всего.",
        "Перерыв? Самое время сделать его.",
        "Усталость — сигнал к отдыху.",
        "Время освежить мысли перерывом!"
    ]
    return random.choice(messages)

def update_timer(label, reminder_interval, window):
    global start_time, is_paused
    if not is_paused:
        current_time = int(time.time() - start_time)
        label.config(text=f"Прошло времени: {current_time} секунд")
        if current_time >= reminder_interval:
            label.config(text="Пора сделать перерыв!")
            log_break("break", current_time)
            notification.notify(
                title="Пора сделать перерыв!",
                message=get_random_message(),
                timeout=10
            )
            start_time = time.time()

    label.after(1000, update_timer, label, reminder_interval, window)

def main(reminder_interval, use_gui):
    global start_time, is_paused, paused_time
    total_time = 0
    is_paused = False
    paused_time = 0
    print(f"Трекер времени запущен. Напоминания будут каждые {reminder_interval} секунд.")
    
    if use_gui:
        window = tk.Tk()
        window.title("Трекер времени")

        label = tk.Label(window, text="Прошло времени: 0 секунд", font=("Arial", 16))
        label.pack(padx=20, pady=20)

        start_time = time.time()

        update_timer(label, reminder_interval, window)

        pause_button = tk.Button(window, text="Пауза", font=("Arial", 14), command=toggle_pause)
        pause_button.pack(pady=5)

        resume_button = tk.Button(window, text="Возобновить", font=("Arial", 14), command=resume_timer)
        resume_button.pack(pady=5)

        stats_button = tk.Button(window, text="Показать статистику", font=("Arial", 14), command=show_statistics)
        stats_button.pack(pady=5)

        keyboard.add_hotkey('ctrl+shift+1', lambda: quit_program(window))

        window.mainloop()

    else:
        print("GUI отключен, запуск в консольном режиме невозможен.")

def toggle_pause():
    global is_paused, start_time, paused_time
    if not is_paused:
        is_paused = True
        paused_time = int(time.time() - start_time)
        log_break("pause")
        print("Таймер поставлен на паузу.")

def resume_timer():
    global is_paused, start_time, paused_time
    if is_paused:
        is_paused = False
        start_time = time.time() - paused_time
        log_break("resume")
        print("Таймер возобновлен.")

def show_statistics():
    try:
        with open("break_log.txt", "r") as log_file:
            stats = log_file.read()
            stats_window = tk.Toplevel()
            stats_window.title("Статистика")
            stats_label = tk.Label(stats_window, text=stats, font=("Arial", 12), justify="left")
            stats_label.pack(padx=10, pady=10)
    except FileNotFoundError:
        messagebox.showinfo("Статистика", "Файл статистики отсутствует.")

def quit_program(window):
    print("Программа завершена по комбинации клавиш Ctrl + Shift + 1.")
    log_break("stop")
    window.destroy()
    exit()

if __name__ == "__main__":
    reminder_interval = 10

    main(reminder_interval, use_gui=True)
