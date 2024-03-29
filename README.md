# SoyleKZ - программа для обучения казахскому языку в домашних условиях.

## Протестировано и работает под управлением

- Python 3.9.7
- Windows 10/11 x64 (x86) or LinuxMint 20, x64 (x86)
- PyQt5
- pyinstaller (для создания исполняемого exe файла)
- playsound==1.2.2 (для Windows 10/11)


### Клонируем репозиторий к себе на ПК

```bash
git clone git@github.com:themasterid/SoyleKZ.git
```

### Активируем виртуальное окружение

```bash
source venv/Scripts/activate
```

### Обновляем pip и устанавливаем зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Конвертируем GUI

```bash
pyuic5 mainUI.ui -o res/mainUI.py
```

### Запускаем приложение

```bash
python main.pyw
```


### Создаем exe файл для Windows

```bash
pyinstaller --onefile --noconsole --path venv\Lib\site-packages\PyQt5\Qt\bin main.pyw
```

Автор: [Клепиков Дмитрий](https://github.com/themasterid)
