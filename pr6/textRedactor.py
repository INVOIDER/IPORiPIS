import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('textRedactor.ui', self)

        self.textBrowser.setReadOnly(False)

        self.pushButton.clicked.connect(self.open_file)  # Открыть файл
        self.pushButton_2.clicked.connect(self.save_file)  # Сохранить файл

        self.current_file_path = None


    def open_file(self):
        # Открываем диалоговое окно для выбора файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self,"Открыть текстовый файл","","Text Files (*.txt);;All Files (*)",options=options)
        if file_path:
            try:
                # Читаем содержимое файла
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Отображаем содержимое в текстовом поле
                self.textBrowser.setPlainText(content)

                # Обновляем метку с выбранным файлом
                self.label.setText(f"Выбранный файл: {file_path}")

                # Сохраняем путь к файлу
                self.current_file_path = file_path
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{str(e)}")


    def save_file(self):
        # Если файл уже был открыт, сохраняем изменения в тот же файл
        if self.current_file_path:
            try:
                # Получаем текст из текстового поля
                content = self.textBrowser.toPlainText()

                # Сохраняем текст в файл
                with open(self.current_file_path, "w", encoding="utf-8") as file:
                    file.write(content)

                QMessageBox.information(self, "Успех", "Файл успешно сохранен!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            # Если файл не был открыт, предлагаем выбрать место для сохранения
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить текстовый файл",
                "",
                "Text Files (*.txt);;All Files (*)",
                options=options
            )

            if file_path:
                try:
                    # Получаем текст из текстового поля
                    content = self.textBrowser.toPlainText()

                    # Сохраняем текст в файл
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(content)

                    # Обновляем метку с выбранным файлом
                    self.label.setText(f"Выбранный файл: {file_path}")

                    # Сохраняем путь к файлу
                    self.current_file_path = file_path

                    QMessageBox.information(self, "Успех", "Файл успешно сохранен!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
