import mysql.connector
from MegaLeilaoBD import *
from estilizacao import button_style
from janelaprincipal import MainWindow
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox,
                               QFileDialog, QTabWidget, QToolButton, QGridLayout)
from PySide6.QtGui import QPixmap, Qt, QFont, QIcon, QImage
from PySide6.QtCore import QSize

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MegaLeilão - Login")
        self.setFixedSize(450, 550)
        self.center_on_screen()
        self.setup_ui()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def setup_ui(self):
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet("background-color: #f4f6f9;")
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("MegaLeilão")
        title_label.setFont(QFont("Roboto", 36, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(20)

        self.login_frame = QFrame()
        self.login_frame.setStyleSheet("background-color: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);")
        self.login_frame.setMaximumWidth(380)
        login_layout = QVBoxLayout(self.login_frame)
        login_layout.setSpacing(20)
        login_layout.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário")
        self.username_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.username_input.setFixedHeight(45)
        self.username_input.setMaximumWidth(320)
        login_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.password_input.setFixedHeight(45)
        self.password_input.setMaximumWidth(320)
        login_layout.addWidget(self.password_input)

        login_btn_layout = QHBoxLayout()
        login_btn = QPushButton("Entrar")
        login_btn.setStyleSheet(button_style())
        login_btn.setFixedSize(140, 45)
        login_btn.clicked.connect(self.login)
        login_btn_layout.addWidget(login_btn)

        register_btn = QPushButton("Cadastrar")
        register_btn.setStyleSheet(button_style())
        register_btn.setFixedSize(140, 45)
        register_btn.clicked.connect(self.show_register)
        login_btn_layout.addWidget(register_btn)

        login_layout.addLayout(login_btn_layout)
        main_layout.addWidget(self.login_frame)

        self.register_frame = QFrame()
        self.register_frame.setStyleSheet("background-color: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);")
        self.register_frame.setMaximumWidth(380)
        self.register_frame.setVisible(False)
        register_layout = QVBoxLayout(self.register_frame)
        register_layout.setSpacing(20)
        register_layout.setAlignment(Qt.AlignCenter)

        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText("Novo Usuário")
        self.reg_username_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_username_input.setFixedHeight(45)
        self.reg_username_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_username_input)

        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("Email")
        self.reg_email_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_email_input.setFixedHeight(45)
        self.reg_email_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_email_input)  

        self.reg_cpf_input = QLineEdit()
        self.reg_cpf_input.setPlaceholderText("CPF")
        self.reg_cpf_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_cpf_input.setFixedHeight(45)
        self.reg_cpf_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_cpf_input)  


        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("Senha")
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        self.reg_password_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_password_input.setFixedHeight(45)
        self.reg_password_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_password_input)

        self.reg_confirm_password_input = QLineEdit()
        self.reg_confirm_password_input.setPlaceholderText("Confirme a Senha")
        self.reg_confirm_password_input.setEchoMode(QLineEdit.Password)
        self.reg_confirm_password_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_confirm_password_input.setFixedHeight(45)
        self.reg_confirm_password_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_confirm_password_input)


        
        reg_btn_layout = QHBoxLayout()
        submit_reg_btn = QPushButton("Cadastrar")
        submit_reg_btn.setStyleSheet(button_style())
        submit_reg_btn.setFixedSize(140, 45)
        submit_reg_btn.clicked.connect(self.register)
        reg_btn_layout.addWidget(submit_reg_btn)

        back_btn = QPushButton("Voltar")
        back_btn.setStyleSheet(button_style())
        back_btn.setFixedSize(140, 45)
        back_btn.clicked.connect(self.show_login)
        reg_btn_layout.addWidget(back_btn)

        register_layout.addLayout(reg_btn_layout)
        main_layout.addWidget(self.register_frame)
        main_layout.addStretch(1)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
        hashed_password = hash_password(password)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE nome = %s AND senha = %s", (username, hashed_password))
            user = cursor.fetchone()
            conn.close()
            if user:
                self.open_main_window(username)
            else:
                QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos!")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro no banco de dados: {e}")

    def register(self):
        username = self.reg_username_input.text()
        password = self.reg_password_input.text()
    
        confirm_password = self.reg_confirm_password_input.text()
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return
        hashed_password = hash_password(password)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sucesso", "Cadastro realizado com sucesso!")
            self.show_login()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro no banco de dados: {e}")

    def show_register(self):
        self.login_frame.setVisible(False)
        self.register_frame.setVisible(True)

    def show_login(self):
        self.register_frame.setVisible(False)
        self.login_frame.setVisible(True)
        self.reg_username_input.clear()
        self.reg_password_input.clear()
        self.reg_confirm_password_input.clear()

    def open_main_window(self, username):
        self.main_window = MainWindow(username, self)
        self.main_window.show()
        self.hide()