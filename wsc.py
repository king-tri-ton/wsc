import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys

def checksite(url):
    try:
        response = requests.get(url, timeout=5)
        response_time = response.elapsed.total_seconds() * 1000  # Время ответа в миллисекундах
        if response.status_code == 200:
            try:
                page_title = response.text.split('<title>')[1].split('</title>')[0]  # Извлечение заголовка страницы
            except IndexError:
                page_title = "Заголовок не найден"
            show_custom_message(f'Сайт: {url}\nДоступен\nВремя ответа: {response_time:.2f} мс\nЗаголовок страницы: {page_title}')
        else:
            show_custom_message(f'Сайт: {url}\nНедоступен\nСтатус: {response.status_code}')
    except requests.exceptions.RequestException as e:
        show_custom_message(f'Не удалось подключиться к сайту: {url}\nОшибка: {str(e)}')

def show_custom_message(message):
    dialog = QDialog()
    dialog.setWindowTitle("Результат проверки")
    dialog.setFixedSize(360, 640)  # Установка фиксированного размера окна 9:16
    dialog.setWindowIcon(QIcon('check.ico'))  # Установка иконки окна

    layout = QVBoxLayout()

    label = QLabel(message, dialog)
    label.setFont(QFont('Arial', 12))  # Использование делового шрифта
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("color: #333;")
    label.setWordWrap(True)  # Включение переноса текста по словам
    layout.addWidget(label)

    close_button = QPushButton("Закрыть", dialog)
    close_button.setFont(QFont('Arial', 10))  # Использование делового шрифта
    close_button.setStyleSheet("""
        QPushButton {
            background-color: #007BFF;
            color: #FFFFFF;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
    """)
    close_button.clicked.connect(dialog.accept)
    layout.addWidget(close_button, alignment=Qt.AlignCenter)

    dialog.setLayout(layout)
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f8f9fa;
            border-radius: 10px;
        }
    """)
    dialog.exec_()

class WebsiteStatusChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Оформление в деловом стиле
        self.label = QLabel('Введите URL-адрес сайта:')
        self.label.setFont(QFont('Arial', 12))  # Использование делового шрифта
        self.label.setStyleSheet("color: #333;")
        layout.addWidget(self.label, alignment=Qt.AlignLeft)

        self.url_input = QLineEdit(self)
        self.url_input.setFont(QFont('Arial', 10))  # Использование делового шрифта
        self.url_input.setStyleSheet("""
            border: 1px solid #ced4da;
            padding: 8px;
            border-radius: 5px;
        """)
        self.url_input.setText("https://")  # Заранее вставленный текст
        layout.addWidget(self.url_input)  # Растягиваем по ширине благодаря QVBoxLayout

        # Разделительная линия
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ced4da; height: 1px;")
        layout.addWidget(line)

        self.check_button = QPushButton('Проверить', self)
        self.check_button.setFont(QFont('Arial', 10))  # Использование делового шрифта
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: #FFFFFF;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.check_button.clicked.connect(self.on_click)
        layout.addWidget(self.check_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('WSC v3.2')
        self.setFixedSize(360, 640)  # Установка фиксированного размера окна 9:16
        self.setWindowIcon(QIcon('check.ico'))  # Установка иконки окна

        # Установка общего стиля окна
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
            }
        """)

    def on_click(self):
        url = self.url_input.text()
        if url:
            checksite(url)
        else:
            show_custom_message('Пожалуйста, введите URL-адрес.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WebsiteStatusChecker()
    ex.show()
    sys.exit(app.exec_())
