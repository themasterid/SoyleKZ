"""Application for learning the Kazakh language v 0.20a
All materials were taken from the site: sozdik.soyle.kz
"""
import sys
import random
import json
import os

from PyQt5 import QtWidgets
import vlc
from pydub import AudioSegment, effects
from sys import platform
from playsound import playsound

from SoyleGUI import MainWindow
from lists_soyle import combo_0, combo_1, combo_2, combo_3, combo_4, combo_5, combo_6, combo_7, combo_8, combo_less


flag_lesson = 0
lesson_number = 0


class SoyleWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SoyleWindow, self).__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.ui.comboBox_0.addItems(combo_less)
        self.ui.comboBox_0.setCurrentIndex(0)
        self.ui.comboBox_1.addItems(combo_0)
        self.ui.comboBox_1.setCurrentIndex(0)
        # self.ui.label_image.setPixmap(QtGui.QPixmap("blank.jpg"))
        self.ui.comboBox_0.activated.connect(self.select_list_item)
        self.ui.pushButton_0.clicked.connect(self.lesson_output)
        self.ui.pushButton_1.clicked.connect(self.check_word)
        self.ui.replay_word.clicked.connect(self.replay_sound)

    def replay_sound(self):
        get_text = self.ui.label_0.text().split('\n')[0]
        json_data = self.open_json_file()
        for _, value, in json_data.items():
            if get_text == value[0]:
                self.play_sound(value[3])

    def play_sound(self, number_word):
        json_data = self.open_json_file()
        file_number = '{}_file'.format(number_word)
        if platform == "linux" or platform == "linux2":
            playsound("sounds/{0}/{1}/".format(flag_lesson, lesson_number) +
                      json_data[file_number][2].lower(), block=True)
        elif platform == "darwin":
            playsound("sounds/{0}/{1}/".format(flag_lesson, lesson_number) +
                      json_data[file_number][2].lower(), block=True)
        elif platform == "win32":
            playsound("sounds/{0}/{1}/".format(flag_lesson, lesson_number) +
                      json_data[file_number][2].lower(), block=False)

    def create_file(self, url_file, dict_data):
        try:
            file_open_json = open(url_file, 'r', encoding='utf-8')
        except:
            with open(url_file, 'w', encoding='utf-8') as file_open_json:
                json.dump(dict_data, file_open_json,
                          ensure_ascii=False, indent=4)
                file_open_json.close()

    def create_dirs(self):
        if os.path.isdir('bd/{0}/'.format(flag_lesson)) is False:
            os.mkdir('bd/{0}/'.format(flag_lesson))
        if os.path.isdir('bd/{0}/{1}/'.format(flag_lesson, lesson_number)) is False:
            os.mkdir('bd/{0}/{1}/'.format(flag_lesson, lesson_number))

    def open_json_file(self):
        json_url_file = 'sounds/{0}/{1}/wf_{2}.json'.format(
            flag_lesson, lesson_number, lesson_number)
        with open(json_url_file, 'r', encoding='utf-8') as read_json_file:
            data_json = json.load(read_json_file)
            read_json_file.close()
        return data_json

    def lesson_output(self):
        global flag_lesson, lesson_number
        flag_lesson, lesson_number = self.lessons()
        self.create_dirs()  # create the directory for lessons
        json_words_bd = 'bd/{0}/{1}/words.json'.format(
            flag_lesson, lesson_number)
        json_words_bd_tmp = 'bd/{0}/{1}/words_tmp.json'.format(
            flag_lesson, lesson_number)
        json_data = self.open_json_file()  # getting the data from the json file
        count_words = len(json_data) - 1
        json_words = {}

        for _ in range(count_words):
            json_words[_] = 0

        self.create_file(json_words_bd, json_words)  # creating json files
        json_words_tmp = {
            'words_total': count_words,
            'word_no_end': count_words,
            'progress_bar': 0
        }

        # creating json files
        self.create_file(json_words_bd_tmp, json_words_tmp)

        # Getting data for the progress bar
        with open(json_words_bd_tmp, 'r', encoding='utf-8') as read_json_words_bd_tmp:
            data_json = json.load(read_json_words_bd_tmp)
            progress_bar = abs(
                int((data_json['word_no_end'] * 100 / data_json['words_total']) - 100))
            read_json_words_bd_tmp.close()

         # reading data from the json file
        with open(json_words_bd, 'r', encoding='utf-8') as read_data_from_file:
            result = os.stat(json_words_bd)
            if result.st_size == 2 or result.st_size == 0:
                self.ui.progressBar_0.setProperty("value", progress_bar)
                return self.ui.label_0.setText('Вы выучили все слова раздела')
            else:
                data_loaded = json.load(read_data_from_file)
                number_word, _ = random.choice(list(data_loaded.items()))
            read_data_from_file.close()

        # Recording data for the progress bar
        with open(json_words_bd_tmp, 'w', encoding='utf-8') as write_json_words_bd_tmp:
            data_json['word_no_end'] = len(data_loaded) - 1
            data_json['progress_bar'] = progress_bar
            json.dump(data_json, write_json_words_bd_tmp,
                      ensure_ascii=False, indent=4)
            write_json_words_bd_tmp.close()
            self.ui.progressBar_0.setProperty("value", progress_bar)

        # The number of repetitions to complete the lesson
        value_of_lessons_count = 3
        with open(json_words_bd, 'w', encoding='utf-8') as write_data_json_file:
            if data_loaded[str(number_word)] < value_of_lessons_count:
                data_loaded[str(number_word)] += 1
                json.dump(data_loaded, write_data_json_file,
                          ensure_ascii=False, indent=4)
                write_data_json_file.close()
                self.play_sound(int(number_word))
                text_out = json_data['{}_file'.format(
                    number_word)][0] + '\n' + json_data['{}_file'.format(number_word)][1]
                self.ui.label_0.setText(text_out)

            elif data_loaded[str(number_word)] == value_of_lessons_count:
                del data_loaded[str(number_word)]
                json.dump(data_loaded, write_data_json_file,
                          ensure_ascii=False, indent=4)
                write_data_json_file.close()
                text_out = 'Вы выучили слово ' + \
                    json_data['{}_file'.format(number_word)][0]
                self.ui.label_0.setText(text_out)
        return

    def check_word(self):
        text_check = self.ui.label_0.text().split('\n')[0]
        file_c = self.ui.textEdit_0.toPlainText().split('\n')[0]
        if len(file_c) > len(text_check):
            return self.ui.label_1.setText('Слишком длинное слово!')
        elif text_check == 'Вывод слов, нажмите кнопку "Следующее слово"' or len(file_c) == 0:
            return self.ui.label_1.setText('Введите не пустую строку!')
        if text_check == file_c:
            return self.ui.label_1.setText('"' + text_check + '" ошибок нет.')
        else:
            return self.ui.label_1.setText('Допущена ошибка "' + file_c + '"')

    def lessons(self):
        return self.ui.comboBox_0.currentIndex(), self.ui.comboBox_1.currentIndex()

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


app = QtWidgets.QApplication([])
application = SoyleWindow()
application.show()

sys.exit(app.exec())
