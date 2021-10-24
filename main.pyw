"""Application for learning the Kazakh language v 0.25a
All materials were taken from the site: sozdik.soyle.kz
"""
import json
import os
import random
import sys
from sys import platform

import vlc
from playsound import playsound
from PyQt5 import QtWidgets

from res.lists_soyle import (combo_0, combo_1, combo_2, combo_3, combo_4,
                             combo_5, combo_6, combo_7, combo_8, combo_less)
from res.mainUI import Ui_MainWindow

LESS_COUNT = 30
flag_lesson = 0
less_n = 0
times_new_roman_black = (
    "font: 75 12pt 'Times New Roman';"
    "background-color: rgb(255, 255, 255);"
    "text color: rgb(0, 0, 0);")
times_new_roman_green = (
    "font: 75 12pt 'Times New Roman';"
    "background-color: rgb(233, 255, 233);"
    "text color: rgb(0, 0, 0);")
times_new_roman_red = (
    "font: 75 12pt 'Times New Roman';"
    "background-color: rgb(255, 194, 194);"
    "text color: rgb(0, 0, 0);")


class SoyleWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(SoyleWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.comboBox_0.addItems(combo_less)
        self.ui.comboBox_0.setCurrentIndex(0)
        self.ui.comboBox_1.addItems(combo_0)
        self.ui.comboBox_1.setCurrentIndex(0)
        self.ui.comboBox_0.activated.connect(self.select_list_item)
        self.ui.pushButton_0.clicked.connect(self.lesson_output)
        self.ui.pushButton_1.clicked.connect(self.check_word)
        self.ui.replay_word.clicked.connect(self.replay_sound)

    def replay_sound(self):
        for self._, self.value, in self.open_json_file().items():
            if self.ui.label_0.text().split('\n')[0] == self.value[0]:
                self.play_sound(self.value[3])

    def play_sound(self, number_word):
        if platform == "linux" or platform == "linux2":
            play_sound_less = vlc.MediaPlayer(
                f"sounds/{flag_lesson}/{less_n}/" +
                self.open_json_file()[f'{number_word}_file'][2].lower())
            play_sound_less.audio_set_volume(80)
            play_sound_less.play()
        elif platform == "darwin":
            # normalize sound by volume
            # rawsound = AudioSegment.from_file("sounds/{0}/{1}/".format(flag_lesson, less_n) + self.open_json_file()[f'{number_word}_file'][2].upper(), "mp3")
            # normalizedsound = effects.normalize(rawsound)
            # normalizedsound.export("sounds/{0}/{1}/{0}_{1}".format(flag_lesson, less_n) + "." +str(number_word) + "." + self.open_json_file()[f'{number_word}_file'][2].lower(), format="mp3")
            play_sound_less = vlc.MediaPlayer(
                f"sounds/{flag_lesson}/{less_n}/" +
                self.open_json_file()[f'{number_word}_file'][2].lower())
            play_sound_less.audio_set_volume(80)
            play_sound_less.play()
        elif platform == "win32":
            playsound(
                f"sounds/{flag_lesson}/{less_n}/" +
                self.open_json_file()[f'{number_word}_file'][2].lower(),
                block=False)

    def create_file(self, url_file, dict_data):
        try:
            f = open(url_file, 'r', encoding='utf-8')
        except FileNotFoundError:
            with open(url_file, 'w', encoding='utf-8') as f:
                json.dump(dict_data, f, ensure_ascii=False, indent=4)

    def create_dirs(self, flag_lesson, less_n):
        if not os.path.isdir(f'bd/{flag_lesson}/'):
            os.mkdir(f'bd/{flag_lesson}/')
        if not os.path.isdir(f'bd/{flag_lesson}/{less_n}/'):
            os.mkdir(f'bd/{flag_lesson}/{less_n}/')

    def open_json_file(self):
        with open(
            f'sounds/{flag_lesson}/{less_n}/new_wf_{less_n}.json',
            'r',
            encoding='utf-8'
        ) as f:
            return json.load(f)

    def lesson_output(self):
        global flag_lesson, less_n
        self.ui.pushButton_0.setDisabled(True)
        flag_lesson, less_n = self.lessons()
        # create the directory for lessons
        self.create_dirs(flag_lesson, less_n)
        words_bd = f'bd/{flag_lesson}/{less_n}/words.json'
        words_bd_tmp = f'bd/{flag_lesson}/{less_n}/words_tmp.json'
        json_data = self.open_json_file()
        count_words = len(json_data) - 1
        json_words = {}

        for _ in range(count_words):
            json_words[_] = 0

        self.create_file(words_bd, json_words)  # creating json files
        json_words_tmp = {
            'words_total': count_words,
            'word_no_end': count_words,
            'progress_bar': 0
        }

        # creating json files
        self.create_file(words_bd_tmp, json_words_tmp)

        # Getting data for the progress bar
        with open(words_bd_tmp, 'r', encoding='utf-8') as f:
            data_json = json.load(f)
            progress_bar = abs(int(
                (
                    data_json['word_no_end'] * 100 /
                    data_json['words_total']) - 100
            ))

        with open(words_bd, 'r', encoding='utf-8') as f:
            result = os.stat(words_bd)
            if result.st_size == 2 or result.st_size == 0:
                self.ui.progressBar_0.setProperty("value", progress_bar)
                return self.ui.label_0.setText('Вы выучили все слова раздела')
            data_loaded = json.load(f)
            number_word, _ = random.choice(list(data_loaded.items()))

        # Recording data for the progress bar
        with open(words_bd_tmp, 'w', encoding='utf-8') as f:
            data_json['word_no_end'] = len(data_loaded) - 1
            data_json['progress_bar'] = progress_bar
            json.dump(data_json, f, ensure_ascii=False, indent=4)
            self.ui.progressBar_0.setProperty("value", progress_bar)

        # The number of repetitions to complete the lesson
        with open(words_bd, 'w', encoding='utf-8') as f:
            if data_loaded[str(number_word)] < LESS_COUNT:
                data_loaded[str(number_word)] += 1
                json.dump(data_loaded, f, ensure_ascii=False, indent=4)
                self.play_sound(int(number_word))
                text_out = (
                    json_data[f'{number_word}_file'][0] +
                    '\n' + len(json_data[f'{number_word}_file'][1]) * "█")
                self.ui.label_0.setText(text_out)
            elif data_loaded[str(number_word)] == LESS_COUNT:
                del data_loaded[str(number_word)]
                json.dump(data_loaded, f, ensure_ascii=False, indent=4)
                text_out = (
                    'Вы выучили слово ' +
                    json_data[f'{number_word}_file'][0])
                self.ui.label_0.setText(text_out)

        list_words = []

        text_info = json_data[f'{number_word}_file'][1]

        self.ui.pushButton_var1.setDisabled(False)
        self.ui.pushButton_var2.setDisabled(False)
        self.ui.pushButton_var3.setDisabled(False)

        list_words.append(text_info)

        words2, _ = random.choice(list(data_loaded.items()))
        list_words.append(json_data[f'{words2}_file'][1])

        words3, _ = random.choice(list(data_loaded.items()))
        list_words.append(json_data[f'{words3}_file'][1])

        random.shuffle(list_words)

        self.ui.pushButton_var1.setStyleSheet(times_new_roman_black)
        self.ui.pushButton_var2.setStyleSheet(times_new_roman_black)
        self.ui.pushButton_var3.setStyleSheet(times_new_roman_black)

        self.ui.pushButton_var1.setText(list_words[0])
        self.ui.pushButton_var1.clicked.connect(
            lambda: self.next_word(text_info))

        self.ui.pushButton_var2.setText(list_words[1])
        self.ui.pushButton_var2.clicked.connect(
            lambda: self.next_word(text_info))

        self.ui.pushButton_var3.setText(list_words[2])
        self.ui.pushButton_var3.clicked.connect(
            lambda: self.next_word(text_info))

    def next_word(self, text_info):
        sender = self.sender()
        self.ui.pushButton_0.setDisabled(False)

        if sender.objectName() == 'pushButton_var1':
            if self.ui.pushButton_var1.text() == text_info:
                self.ui.pushButton_var1.setStyleSheet(times_new_roman_green)
            else:
                self.ui.pushButton_var1.setStyleSheet(times_new_roman_red)
        elif sender.objectName() == 'pushButton_var2':
            if self.ui.pushButton_var2.text() == text_info:
                self.ui.pushButton_var2.setStyleSheet(times_new_roman_green)
            else:
                self.ui.pushButton_var2.setStyleSheet(times_new_roman_red)
        elif sender.objectName() == 'pushButton_var3':
            if self.ui.pushButton_var3.text() == text_info:
                self.ui.pushButton_var3.setStyleSheet(times_new_roman_green)
            else:
                self.ui.pushButton_var3.setStyleSheet(times_new_roman_red)

        self.ui.pushButton_var1.setDisabled(True)
        self.ui.pushButton_var2.setDisabled(True)
        self.ui.pushButton_var3.setDisabled(True)
        return

    def check_word(self):
        text_check = self.ui.label_0.text().split('\n')[0]
        file_c = self.ui.textEdit_0.toPlainText().split('\n')[0]
        if len(file_c) > len(text_check):
            return self.ui.label_1.setText('Слишком длинное слово!')
        elif text_check == (
            'Вывод слов, нажмите кнопку "Следующее слово"'
        ) or len(file_c) == 0:
            return self.ui.label_1.setText('Введите не пустую строку!')
        if text_check == file_c:
            return self.ui.label_1.setText('"' + text_check + '" ошибок нет.')
        return self.ui.label_1.setText('Допущена ошибка "' + file_c + '"')

    def lessons(self):
        return (
            self.ui.comboBox_0.currentIndex(),
            self.ui.comboBox_1.currentIndex()
        )

    def select_list_item(self):
        if self.ui.comboBox_0.currentIndex() == 0:
            self.ui.comboBox_1.clear()
            self.ui.comboBox_1.addItems(combo_0)
            self.ui.comboBox_1.activated.connect(self.lessons)

        elif self.ui.comboBox_0.currentIndex() == 1:
            self.ui.comboBox_1.clear()
            self.ui.comboBox_1.addItems(combo_1)
            self.ui.comboBox_1.activated.connect(self.lessons)

        elif self.ui.comboBox_0.currentIndex() == 2:
            self.ui.comboBox_1.clear()
            self.ui.comboBox_1.addItems(combo_2)
            self.ui.comboBox_1.activated.connect(self.lessons)

        elif self.ui.comboBox_0.currentIndex() == 3:
            self.ui.comboBox_1.clear()
            self.ui.comboBox_1.addItems(combo_3)
            self.ui.comboBox_1.activated.connect(self.lessons)

        elif self.ui.comboBox_0.currentIndex() == 4:
            self.ui.comboBox_1.clear()
            self.ui.comboBox_1.addItems(combo_4)
            self.ui.comboBox_1.activated.connect(self.lessons)

        elif self.ui.comboBox_0.currentIndex() == 5:
            self.ui.comboBox_1.clear()
            self.ui.comboBox_1.addItems(combo_5)
            self.ui.comboBox_1.activated.connect(self.lessons)

        elif self.ui.comboBox_0.currentIndex() == 6:
            self.ui.comboBox_1.clear()
            self.ui.comboBox_1.addItems(combo_6)
            self.ui.comboBox_1.activated.connect(self.lessons)

        elif self.ui.comboBox_0.currentIndex() == 7:
            self.ui.comboBox_1.clear()
            self.ui.comboBox_1.addItems(combo_7)
            self.ui.comboBox_1.activated.connect(self.lessons)

        elif self.ui.comboBox_0.currentIndex() == 8:
            self.ui.comboBox_1.clear()
            self.ui.comboBox_1.addItems(combo_8)
            self.ui.comboBox_1.activated.connect(self.lessons)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = SoyleWindow()
    application.show()
    sys.exit(app.exec_())
