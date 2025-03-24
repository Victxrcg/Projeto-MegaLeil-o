import mysql.connector
import hashlib  # Biblioteca para criptografia
import re  # Para validações com expressões regulares
from MegaLeilaoBD import *
from estilizacao import button_style
from janelaprincipal import MainWindow
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox,
                               QFileDialog, QTabWidget, QToolButton, QGridLayout)
from PySide6.QtGui import QPixmap, Qt, QFont, QIcon, QImage
from PySide6.QtCore import QSize

# Função para criptografar a senha usando SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MegaLeilão - Login")
        self.setFixedSize(450, 650)
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

        # Frame de Login
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

        # Frame de Cadastro
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
        self.reg_cpf_input.setPlaceholderText("CPF (ex.: 123.456.789-00)")
        self.reg_cpf_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_cpf_input.setFixedHeight(45)
        self.reg_cpf_input.setMaximumWidth(320)
        self.reg_cpf_input.textEdited.connect(self.format_cpf)
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

    def format_cpf(self, text):
        # Remove todos os caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, text))
        
        # Formata o CPF conforme o usuário digita
        formatted_cpf = ''
        if cpf:
            if len(cpf) <= 3:
                formatted_cpf = cpf
            elif len(cpf) <= 6:
                formatted_cpf = f"{cpf[:3]}.{cpf[3:]}"
            elif len(cpf) <= 9:
                formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
            else:
                formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
        
        # Define o texto formatado no campo, evitando loop infinito
        self.reg_cpf_input.blockSignals(True)
        self.reg_cpf_input.setText(formatted_cpf)
        self.reg_cpf_input.blockSignals(False)

    def validate_username(self, username):
        # Permitir apenas letras, hífen e sublinhado; tamanho entre 3 e 20 caracteres
        if not re.match(r'^[a-zA-Z][a-zA-Z_-]{2,19}$', username):
            return False
        return True

    def validate_email(self, email):
        # Validação de formato de email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False
        return True

    def validate_password(self, password):
        
        if len(password) < 3:
            return False
        if not re.match(r'^\d+$', password):
            return False
        return True

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        # Resetar estilos dos campos
        self.username_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.password_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")

        # Validações
        if not username or not password:
            if not username:
                self.username_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            if not password:
                self.password_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return

        # Validar nome de usuário
        if not self.validate_username(username):
            self.username_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            QMessageBox.warning(self, "Erro", "O nome de usuário deve conter apenas letras, hífen ou sublinhado, e ter entre 3 e 20 caracteres!")
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
        username = self.reg_username_input.text().strip()
        email = self.reg_email_input.text().strip()
        cpf = self.reg_cpf_input.text().strip()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_password_input.text()

        # Resetar estilos dos campos
        self.reg_username_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_email_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_cpf_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_password_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.reg_confirm_password_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")

        # Validações
        if not all([username, email, cpf, password, confirm_password]):
            if not username:
                self.reg_username_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            if not email:
                self.reg_email_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            if not cpf:
                self.reg_cpf_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            if not password:
                self.reg_password_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            if not confirm_password:
                self.reg_confirm_password_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return

        # Validar nome de usuário
        if not self.validate_username(username):
            self.reg_username_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            QMessageBox.warning(self, "Erro", "O nome de usuário deve conter apenas letras, hífen ou sublinhado, e ter entre 3 e 20 caracteres!")
            return

        # Validar email
        if not self.validate_email(email):
            self.reg_email_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            QMessageBox.warning(self, "Erro", "Email inválido! Use o formato nome@dominio.com.")
            return

        # Validar formato do CPF
        if not (len(cpf) == 14 and cpf[3] == '.' and cpf[7] == '.' and cpf[11] == '-'):
            self.reg_cpf_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            QMessageBox.warning(self, "Erro", "CPF deve estar no formato 123.456.789-00!")
            return

        # Validar senha
        if not self.validate_password(password):
            self.reg_password_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 3 dígitos e conter apenas números!")
            return

        if password != confirm_password:
            self.reg_confirm_password_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return

        # Verificar se o nome de usuário, email ou CPF já estão cadastrados
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Verificar nome de usuário
            cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (username,))
            if cursor.fetchone():
                self.reg_username_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
                QMessageBox.warning(self, "Erro", "Nome de usuário já cadastrado!")
                conn.close()
                return

            # Verificar email
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                self.reg_email_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
                QMessageBox.warning(self, "Erro", "Email já cadastrado!")
                conn.close()
                return

            # Verificar CPF
            cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", (cpf,))
            if cursor.fetchone():
                self.reg_cpf_input.setStyleSheet("font-size: 16px; border: 1px solid #e74c3c; border-radius: 8px; padding: 10px;")
                QMessageBox.warning(self, "Erro", "CPF já cadastrado!")
                conn.close()
                return

            # Se todas as validações passarem, cadastrar o usuário
            hashed_password = hash_password(password)
            cursor.execute("INSERT INTO usuarios (nome, cpf, email, senha) VALUES (%s, %s, %s, %s)", 
                           (username, cpf, email, hashed_password))
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
        self.reg_email_input.clear()
        self.reg_cpf_input.clear()
        self.reg_password_input.clear()
        self.reg_confirm_password_input.clear()

    def open_main_window(self, username):
        self.main_window = MainWindow(username, self)
        self.main_window.show()
        self.hide()