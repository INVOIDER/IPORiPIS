from PyQt5 import QtWidgets, uic
import smtplib
import os
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PyQt5.QtWidgets import QFileDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('main.ui', self)

        # self.msg_addr = self.findChild(QtWidgets.QLineEdit, 'email_to')
        self.choose_email_contacts = self.findChild(QtWidgets.QPushButton, 'email_to')
        self.msg_header = self.findChild(QtWidgets.QLineEdit, 'Header_email')
        self.msg_text = self.findChild(QtWidgets.QTextEdit, 'text_email')
        self.pushButton = self.findChild(QtWidgets.QPushButton, 'send_email')

        self.server_type = self.findChild(QtWidgets.QComboBox, 'server_selection')
        self.msg_sender_addr = self.findChild(QtWidgets.QLineEdit, 'email_from')
        self.from_password = self.findChild(QtWidgets.QLineEdit, 'user_password')
        self.from_password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.choose_files_button = self.findChild(QtWidgets.QPushButton, 'attach_file')
        self.UploadedFiles = self.findChild(QtWidgets.QTextEdit, 'files_to_be_send')

        self.pushButton.clicked.connect(self.on_send_button_clicked)
        self.choose_files_button.clicked.connect(self.on_choose_files_clicked)
        self.selected_files = []

        self.choose_email_contacts.clicked.connect(self.on_choose_email_contacts)
        self.csv_file_path = None

    def set_address(self, text):
        self.msg_addr.setText(text)

    def set_header(self, text):
        self.msg_header.setText(text)

    def set_message(self, text):
        self.msg_text.setPlainText(text)

    def get_address(self):
        return self.msg_addr.text()

    def get_header(self):
        return self.msg_header.text()

    def get_message(self):
        return self.msg_text.toPlainText()

    def get_user_password(self):
        return self.from_password.text()

    def get_sender_addr(self):
        return self.msg_sender_addr.text()

    def get_server_type(self):
        return self.server_type.currentText()

    def get_smtp_server(self, type):
        print('type = ', type)
        if type == "Яндекс":
            return "smtp.yandex.ru", 587
        elif type == "Google":
            return "smtp.gmail.com", 587
        elif type == "Mail.ru":
            return "smtp.mail.ru", 587
        else:
            raise ValueError("Неизвестный тип сервера")

    def on_choose_email_contacts(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите CSV-файл с адресатами", "",
                                                   "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.csv_file_path = file_path
            print('Выбран ',file_path)
            QtWidgets.QMessageBox.information(self, "Файл выбран", f"Выбран CSV-файл: {file_path}")

    def get_addreses_from_csv(self, file_path):
        recipients = []
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Пропуск пустых строк
                    addr_to = row[0].strip()  # Берём email-адрес
                    recipients.append(addr_to)
        print('Выбраны email: ', recipients)
        return recipients

    def on_choose_files_clicked(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "All Files (*);;", options=options)
        if files:
            self.selected_files = files
            self.UploadedFiles.setText("\n".join(files))

    def on_send_button_clicked(self):
        if not self.csv_file_path:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Отсутствует CSV-файл с адресатами!")
            return

        sender_addr = self.get_sender_addr()
        sender_passwd = self.get_user_password()
        server_type = self.get_server_type()
        # address = self.get_address()
        header = self.get_header()
        message = self.get_message()

        smtp_server, smtp_port = self.get_smtp_server(server_type)
        try:
            recipients = self.get_addreses_from_csv(self.csv_file_path)
            for address in recipients:
                print('Отправляю письмо на:', address)
                send_email(sender_addr, sender_passwd, smtp_server, smtp_port, self.selected_files, address, header, message)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось отправить письма: {str(e)}")


def send_email(sender_addr, sender_passwd, smtp_server, smtp_port, files, addr_to, msg_subj, msg_text):
    print('Готовлюсь к отправке')
    msg = MIMEMultipart()
    msg['From'] = sender_addr
    msg['To'] = addr_to
    msg['Subject'] = msg_subj

    msg.attach(MIMEText(msg_text, 'plain'))
    for file_path in files:
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(file_path)
                mime_part = MIMEBase("application", "octet-stream")
                mime_part.set_payload(file_data)
                encoders.encode_base64(mime_part)
                mime_part.add_header("Content-Disposition", f"attachment; filename={file_name}")
                msg.attach(mime_part)
        except Exception as e:
            print(f"Не удалось прикрепить файл {file_path}: {str(e)}")

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.set_debuglevel(1)

        server.login(sender_addr, sender_passwd)
        server.set_debuglevel(1)
        server.sendmail(sender_addr, [addr_to], msg.as_string())
        server.quit()
    except Exception as e:
        raise RuntimeError(f"Ошибка при отправке письма: {str(e)}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
