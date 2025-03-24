import sys
import mysql.connector
import hashlib
import shutil
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox,
                               QFileDialog, QTabWidget, QToolButton, QGridLayout)
from PySide6.QtGui import QPixmap, Qt, QFont, QIcon, QImage
from PySide6.QtCore import QSize

# Configuração de conexão com o MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'megaleilao'
}

# Função para criar o banco de dados e as tabelas
def criar_banco_de_dados():
    try:
        # Conectar ao MySQL sem especificar um banco de dados
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()

        # Criar o banco de dados
        cursor.execute("CREATE DATABASE IF NOT EXISTS megaleilao")
        cursor.execute("USE megaleilao")

        # Criar a tabela de usuários (users)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(64) NOT NULL,
                email VARCHAR(100),
                cpf VARCHAR(14),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Criar a tabela de veículos (vehicles)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT,
                image_path VARCHAR(255),
                status ENUM('available', 'sold') DEFAULT 'available',
                buyer_id VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (buyer_id) REFERENCES users(username) ON DELETE SET NULL
            )
        """)

        # Criar a tabela de favoritos (favorites)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(50) NOT NULL,
                vehicle_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(username) ON DELETE CASCADE,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
                UNIQUE (user_id, vehicle_id)
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Banco de dados 'megaleilao' e tabelas criadas com sucesso!")
    except mysql.connector.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")

# Função para determinar a condição do carro
def determinar_condicao(preco):
    return "Novo" if preco > 100000 else "Usado"

# Função para criptografar a senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Estilo para botões
def estilo_botao():
    return """
        QPushButton {
            background-color: #2c3e50;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-family: 'Roboto', 'Arial', 'Sans-Serif';
            font-weight: bold;
            padding: 8px 16px;
            min-width: 80px;
            min-height: 30px;
        }
        QPushButton:hover {
            background-color: #34495e;
        }
        QPushButton:pressed {
            background-color: #1a252f;
        }
        QPushButton:disabled {
            background-color: #bdc3c7;
            color: #7f8c8d;
        }
    """

# Janela de Login
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

        self.login_frame = QFrame()
        self.login_frame.setStyleSheet("background-color: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);")
        self.login_frame.setMaximumWidth(380)
        login_layout = QVBoxLayout(self.login_frame)
        login_layout.setSpacing(20)
        login_layout.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuário")
        self.username_input.setFixedHeight(45)
        self.username_input.setMaximumWidth(320)
        login_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setMaximumWidth(320)
        login_layout.addWidget(self.password_input)

        login_btn_layout = QHBoxLayout()
        login_btn = QPushButton("Entrar")
        login_btn.setStyleSheet(estilo_botao())
        login_btn.setFixedSize(140, 45)
        login_btn.clicked.connect(self.login)
        login_btn_layout.addWidget(login_btn)

        register_btn = QPushButton("Cadastrar")
        register_btn.setStyleSheet(estilo_botao())
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
        self.reg_username_input.setFixedHeight(45)
        self.reg_username_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_username_input)

        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("E-mail")
        self.reg_email_input.setFixedHeight(45)
        self.reg_email_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_email_input)

        self.reg_cpf_input = QLineEdit()
        self.reg_cpf_input.setPlaceholderText("CPF (ex.: 123.456.789-00)")
        self.reg_cpf_input.setFixedHeight(45)
        self.reg_cpf_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_cpf_input)

        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("Nova Senha")
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        self.reg_password_input.setFixedHeight(45)
        self.reg_password_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_password_input)

        self.reg_confirm_password_input = QLineEdit()
        self.reg_confirm_password_input.setPlaceholderText("Confirme a Senha")
        self.reg_confirm_password_input.setEchoMode(QLineEdit.Password)
        self.reg_confirm_password_input.setFixedHeight(45)
        self.reg_confirm_password_input.setMaximumWidth(320)
        register_layout.addWidget(self.reg_confirm_password_input)

        reg_btn_layout = QHBoxLayout()
        submit_reg_btn = QPushButton("Cadastrar")
        submit_reg_btn.setStyleSheet(estilo_botao())
        submit_reg_btn.setFixedSize(140, 45)
        submit_reg_btn.clicked.connect(self.register)
        reg_btn_layout.addWidget(submit_reg_btn)

        back_btn = QPushButton("Voltar")
        back_btn.setStyleSheet(estilo_botao())
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
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
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
        email = self.reg_email_input.text()
        cpf = self.reg_cpf_input.text()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_password_input.text()
        if not username or not password or not confirm_password or not email or not cpf:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return
        hashed_password = hash_password(password)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, email, cpf) VALUES (%s, %s, %s, %s)",
                           (username, hashed_password, email, cpf))
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

# Janela Principal (Mercado de Veículos)
class MainWindow(QMainWindow):
    def __init__(self, username, login_window):
        super().__init__()
        self.username = username
        self.login_window = login_window
        self.setWindowTitle("MegaLeilão")
        self.setGeometry(100, 100, 1440, 900)
        self.setup_ui()
        self.load_vehicles()
        self.load_history()

    def setup_ui(self):
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet("background-color: #f4f6f9;")
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        # Menu Lateral
        self.menu_principal = QFrame(self.central_widget)
        self.menu_principal.setFixedWidth(250)
        self.menu_principal.setStyleSheet("background-color: #2c3e50; padding: 20px;")
        menu_layout = QVBoxLayout(self.menu_principal)
        menu_layout.setSpacing(20)

        filtros_label = QLabel("Filtros")
        filtros_label.setFont(QFont("Roboto", 20, QFont.Bold))
        filtros_label.setStyleSheet("color: #ecf0f1;")
        menu_layout.addWidget(filtros_label)

        self.btn_novo = QPushButton("Novo")
        self.btn_novo.setStyleSheet(estilo_botao())
        self.btn_novo.setFixedHeight(50)
        self.btn_novo.clicked.connect(lambda: self.filter_vehicles("Novo"))
        menu_layout.addWidget(self.btn_novo)

        self.btn_usado = QPushButton("Usado")
        self.btn_usado.setStyleSheet(estilo_botao())
        self.btn_usado.setFixedHeight(50)
        self.btn_usado.clicked.connect(lambda: self.filter_vehicles("Usado"))
        menu_layout.addWidget(self.btn_usado)

        menu_layout.addSpacing(30)

        opcoes_label = QLabel("Opções")
        opcoes_label.setFont(QFont("Roboto", 20, QFont.Bold))
        opcoes_label.setStyleSheet("color: #ecf0f1;")
        menu_layout.addWidget(opcoes_label)

        self.btn_comprar = QPushButton("Comprar")
        self.btn_comprar.setStyleSheet(estilo_botao())
        self.btn_comprar.setFixedHeight(50)
        self.btn_comprar.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        menu_layout.addWidget(self.btn_comprar)

        self.btn_vender = QPushButton("Vender")
        self.btn_vender.setStyleSheet(estilo_botao())
        self.btn_vender.setFixedHeight(50)
        self.btn_vender.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        menu_layout.addWidget(self.btn_vender)

        self.btn_historico = QPushButton("Histórico")
        self.btn_historico.setStyleSheet(estilo_botao())
        self.btn_historico.setFixedHeight(50)
        self.btn_historico.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
        menu_layout.addWidget(self.btn_historico)

        self.btn_editar_perfil = QPushButton("Editar Perfil")
        self.btn_editar_perfil.setStyleSheet(estilo_botao())
        self.btn_editar_perfil.setFixedHeight(50)
        self.btn_editar_perfil.clicked.connect(self.edit_profile)
        menu_layout.addWidget(self.btn_editar_perfil)

        menu_layout.addStretch()

        self.central_layout.addWidget(self.menu_principal)

        # Conteúdo Principal
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 25, 20)
        content_layout.setSpacing(20)

        self.header = QFrame()
        self.header.setFixedHeight(80)
        self.header.setStyleSheet("background-color: white; border-bottom: 1px solid #ecf0f1; box-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 0, 25, 0)

        title_label = QLabel("MegaLeilão")
        title_label.setFont(QFont("Roboto", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Procurar veículos...")
        self.search_bar.setFixedHeight(40)
        self.search_bar.setMaximumWidth(400)
        self.search_bar.textChanged.connect(self.search_vehicles)
        header_layout.addWidget(self.search_bar)

        welcome_label = QLabel(f"Bem-vindo, {self.username}")
        welcome_label.setFont(QFont("Roboto", 14))
        welcome_label.setStyleSheet("color: #7f8c8d;")
        header_layout.addWidget(welcome_label)

        sair_btn = QPushButton("Sair")
        sair_btn.setStyleSheet(estilo_botao())
        sair_btn.setFixedSize(100, 40)
        sair_btn.clicked.connect(self.logout)
        header_layout.addWidget(sair_btn)

        content_layout.addWidget(self.header)

        # Abas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 10px 60px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #2c3e50;
            }
        """)

        # Aba Comprar
        self.buy_tab = QWidget()
        buy_layout = QVBoxLayout(self.buy_tab)
        self.loja_principal_container = QScrollArea()
        self.loja_principal_container.setWidgetResizable(True)
        self.loja_principal = QWidget()
        self.grid_layout = QGridLayout(self.loja_principal)
        self.grid_layout.setSpacing(25)
        self.grid_layout.setContentsMargins(50, 50, 50, 50)
        self.loja_principal_container.setWidget(self.loja_principal)
        buy_layout.addWidget(self.loja_principal_container)

        # Aba Vender
        self.sell_tab = QWidget()
        sell_layout = QVBoxLayout(self.sell_tab)
        sell_layout.setSpacing(25)
        sell_layout.setContentsMargins(50, 50, 50, 50)
        sell_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        sell_title = QLabel("Vender um Veículo")
        sell_title.setFont(QFont("Roboto", 24, QFont.Bold))
        sell_title.setStyleSheet("color: #2c3e50;")
        sell_layout.addWidget(sell_title)

        sell_form_frame = QFrame()
        sell_form_frame.setStyleSheet("background-color: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);")
        sell_form_frame.setMaximumWidth(450)
        form_layout = QVBoxLayout(sell_form_frame)
        form_layout.setSpacing(20)

        self.sell_name = QLineEdit()
        self.sell_name.setPlaceholderText("Nome do Veículo")
        self.sell_name.setFixedHeight(45)
        form_layout.addWidget(self.sell_name)

        self.sell_price = QLineEdit()
        self.sell_price.setPlaceholderText("Preço (R$)")
        self.sell_price.setFixedHeight(45)
        form_layout.addWidget(self.sell_price)

        self.sell_desc = QLineEdit()
        self.sell_desc.setPlaceholderText("Descrição")
        self.sell_desc.setFixedHeight(45)
        form_layout.addWidget(self.sell_desc)

        self.sell_image_path = QLineEdit()
        self.sell_image_path.setPlaceholderText("Caminho da Imagem")
        self.sell_image_path.setFixedHeight(45)
        form_layout.addWidget(self.sell_image_path)

        self.image_preview = QLabel()
        self.image_preview.setFixedSize(280, 180)
        self.image_preview.setStyleSheet("border: 1px solid #ecf0f1; border-radius: 5px; background-color: white;")
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setText("Nenhuma imagem selecionada")
        form_layout.addWidget(self.image_preview)

        browse_btn = QPushButton("Escolher Imagem")
        browse_btn.setStyleSheet(estilo_botao())
        browse_btn.setFixedSize(170, 45)
        browse_btn.clicked.connect(self.browse_image)
        form_layout.addWidget(browse_btn)

        submit_btn = QPushButton("Enviar Veículo")
        submit_btn.setStyleSheet(estilo_botao())
        submit_btn.setFixedSize(160, 45)
        submit_btn.clicked.connect(self.submit_vehicle)
        form_layout.addWidget(submit_btn)

        sell_layout.addWidget(sell_form_frame)
        sell_layout.addStretch()

        # Aba Histórico
        self.history_tab = QWidget()
        history_layout = QVBoxLayout(self.history_tab)
        self.history_container = QScrollArea()
        self.history_container.setWidgetResizable(True)
        self.history_widget = QWidget()
        self.history_grid = QGridLayout(self.history_widget)
        self.history_grid.setSpacing(25)
        self.history_grid.setContentsMargins(50, 50, 50, 50)
        self.history_container.setWidget(self.history_widget)
        history_layout.addWidget(self.history_container)

        self.tabs.addTab(self.buy_tab, "Comprar")
        self.tabs.addTab(self.sell_tab, "Vender")
        self.tabs.addTab(self.history_tab, "Histórico")
        content_layout.addWidget(self.tabs)

        self.central_layout.addWidget(content_widget)

    def load_vehicles(self, filter_type=None, search_query=None):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "SELECT id, name, price, description, image_path FROM vehicles WHERE status = 'available'"
            params = []
            if filter_type:
                if filter_type == "Novo":
                    query += " AND price > 100000"
                elif filter_type == "Usado":
                    query += " AND price <= 100000"
            if search_query:
                query += " AND (name LIKE %s OR description LIKE %s)"
                params.extend([f"%{search_query}%", f"%{search_query}%"])
            cursor.execute(query, params)
            vehicles = cursor.fetchall()
            cursor.execute("SELECT vehicle_id FROM favorites WHERE user_id = %s", (self.username,))
            favorites = set(row[0] for row in cursor.fetchall())
            conn.close()

            if not vehicles:
                no_vehicles_label = QLabel("Nenhum veículo encontrado!")
                no_vehicles_label.setStyleSheet("font-size: 20px; color: #7f8c8d;")
                self.grid_layout.addWidget(no_vehicles_label, 0, 0, alignment=Qt.AlignCenter)
                return

            for idx, (vehicle_id, name, price, desc, image_path) in enumerate(vehicles):
                condition = determinar_condicao(price)
                is_favorite = vehicle_id in favorites
                card = self.create_vehicle_card(vehicle_id, name, price, desc, image_path, condition, is_favorite)
                row = idx // 3
                col = idx % 3
                self.grid_layout.addWidget(card, row, col, alignment=Qt.AlignCenter)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar veículos: {e}")

    def load_history(self):
        while self.history_grid.count():
            item = self.history_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price, description, image_path FROM vehicles WHERE status = 'sold' AND buyer_id = %s", (self.username,))
            vehicles = cursor.fetchall()
            conn.close()

            if not vehicles:
                no_history_label = QLabel("Nenhum veículo comprado ainda!")
                no_history_label.setStyleSheet("font-size: 20px; color: #7f8c8d;")
                self.history_grid.addWidget(no_history_label, 0, 0, alignment=Qt.AlignCenter)
                return

            for idx, (vehicle_id, name, price, desc, image_path) in enumerate(vehicles):
                condition = determinar_condicao(price)
                card = self.create_vehicle_card(vehicle_id, name, price, desc, image_path, condition, False, is_history=True)
                row = idx // 3
                col = idx % 3
                self.history_grid.addWidget(card, row, col, alignment=Qt.AlignCenter)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar histórico: {e}")

    def create_vehicle_card(self, vehicle_id, name, price, desc, image_path, condition, is_favorite, is_history=False):
        card = QFrame()
        card.setFixedSize(320, 380)
        card.setStyleSheet("background-color: white; border-radius: 15px; padding: 10px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);")
        layout = QVBoxLayout(card)
        layout.setSpacing(0)

        image_label = QLabel()
        image_label.setFixedSize(290, 200)
        pixmap = QPixmap(image_path if image_path else "default.png")
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(290, 200, Qt.KeepAspectRatio))
        else:
            image_label.setText("Sem Imagem")
            image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        name_layout = QHBoxLayout()
        name_label = QLabel(f"{name} ({condition})")
        name_label.setFont(QFont("Roboto", 16, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        name_layout.addWidget(name_label)

        if not is_history:
            favorite_btn = QToolButton()
            favorite_btn.setIcon(QIcon("favorite.png" if is_favorite else "not_favorite.png"))
            favorite_btn.setStyleSheet("border: none; background: none;")
            favorite_btn.clicked.connect(lambda: self.toggle_favorite(vehicle_id, favorite_btn))
            name_layout.addWidget(favorite_btn, alignment=Qt.AlignRight)

        layout.addLayout(name_layout)

        desc_label = QLabel(desc)
        desc_label.setStyleSheet("color: #7f8c8d;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        price_label = QLabel(f"R${price:,.2f}")
        price_label.setFont(QFont("Roboto", 16, QFont.Bold))
        price_label.setStyleSheet("color: #e74c3c;")
        layout.addWidget(price_label)

        if is_history:
            status_label = QLabel("Comprado")
            status_label.setStyleSheet("color: #27ae60;")
            layout.addWidget(status_label)
        else:
            buy_btn = QPushButton("Comprar")
            buy_btn.setStyleSheet(estilo_botao())
            buy_btn.clicked.connect(lambda: self.buy_vehicle(vehicle_id, name, price))
            layout.addWidget(buy_btn, alignment=Qt.AlignCenter)

        return card

    def toggle_favorite(self, vehicle_id, favorite_btn):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM favorites WHERE user_id = %s AND vehicle_id = %s", (self.username, vehicle_id))
            favorite = cursor.fetchone()
            if favorite:
                cursor.execute("DELETE FROM favorites WHERE user_id = %s AND vehicle_id = %s", (self.username, vehicle_id))
                favorite_btn.setIcon(QIcon("not_favorite.png"))
            else:
                cursor.execute("INSERT INTO favorites (user_id, vehicle_id) VALUES (%s, %s)", (self.username, vehicle_id))
                favorite_btn.setIcon(QIcon("favorite.png"))
            conn.commit()
            conn.close()
            self.load_vehicles()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar favoritos: {e}")

    def buy_vehicle(self, vehicle_id, name, price):
        reply = QMessageBox.question(self, "Confirmar Compra",
                                     f"Deseja comprar {name} por R${price:,.2f}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                cursor.execute("UPDATE vehicles SET status = 'sold', buyer_id = %s WHERE id = %s", (self.username, vehicle_id))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Sucesso", f"{name} comprado com sucesso!")
                self.load_vehicles()
                self.load_history()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Erro", f"Erro ao comprar veículo: {e}")

    def browse_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg)")
        if file_name:
            dest_path = os.path.join("images", os.path.basename(file_name))
            os.makedirs("images", exist_ok=True)
            shutil.copy(file_name, dest_path)
            self.sell_image_path.setText(dest_path)
            pixmap = QPixmap(dest_path)
            self.image_preview.setPixmap(pixmap.scaled(280, 180, Qt.KeepAspectRatio))

    def submit_vehicle(self):
        name = self.sell_name.text().strip()
        price = self.sell_price.text().strip()
        desc = self.sell_desc.text().strip()
        image_path = self.sell_image_path.text().strip()

        if not name or not price:
            QMessageBox.warning(self, "Erro", "Nome e preço são obrigatórios!")
            return
        try:
            price = float(price.replace(",", "."))
            if price <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preço deve ser um número válido maior que zero!")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO vehicles (name, price, description, image_path) VALUES (%s, %s, %s, %s)",
                           (name, price, desc, image_path))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sucesso", "Veículo cadastrado com sucesso!")
            self.sell_name.clear()
            self.sell_price.clear()
            self.sell_desc.clear()
            self.sell_image_path.clear()
            self.image_preview.setText("Nenhuma imagem selecionada")
            self.tabs.setCurrentIndex(0)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar veículo: {e}")

    def filter_vehicles(self, filter_type=None):
        self.load_vehicles(filter_type=filter_type)

    def search_vehicles(self, text):
        self.load_vehicles(search_query=text)

    def logout(self):
        self.close()
        self.login_window.show()

    def edit_profile(self):
        self.edit_window = QMainWindow(self)
        self.edit_window.setWindowTitle("Editar Perfil")
        self.edit_window.setGeometry(300, 300, 450, 650)
        
        central_widget = QWidget()
        self.edit_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Editar Perfil")
        title.setFont(QFont("Roboto", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        edit_frame = QFrame()
        edit_frame.setStyleSheet("background-color: white; border-radius: 15px; padding: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);")
        edit_layout = QVBoxLayout(edit_frame)
        edit_layout.setSpacing(20)

        username_label = QLabel(f"Usuário: {self.username}")
        edit_layout.addWidget(username_label)

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT email, cpf FROM users WHERE username = %s", (self.username,))
            dados_usuario = cursor.fetchone()
            conn.close()
            email_atual, cpf_atual = dados_usuario if dados_usuario else ("", "")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados: {e}")
            return

        self.edit_email_input = QLineEdit()
        self.edit_email_input.setPlaceholderText("E-mail")
        self.edit_email_input.setText(email_atual)
        edit_layout.addWidget(self.edit_email_input)

        self.edit_cpf_input = QLineEdit()
        self.edit_cpf_input.setPlaceholderText("CPF (ex.: 123.456.789-00)")
        self.edit_cpf_input.setText(cpf_atual)
        edit_layout.addWidget(self.edit_cpf_input)

        self.current_password_input = QLineEdit()
        self.current_password_input.setPlaceholderText("Senha Atual")
        self.current_password_input.setEchoMode(QLineEdit.Password)
        edit_layout.addWidget(self.current_password_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Nova Senha")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        edit_layout.addWidget(self.new_password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirme a Nova Senha")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        edit_layout.addWidget(self.confirm_password_input)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Salvar")
        save_btn.setStyleSheet(estilo_botao())
        save_btn.clicked.connect(self.save_profile)
        btn_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet(estilo_botao())
        cancel_btn.clicked.connect(self.edit_window.close)
        btn_layout.addWidget(cancel_btn)

        edit_layout.addLayout(btn_layout)
        layout.addWidget(edit_frame)
        layout.addStretch()

        self.edit_window.show()

    def save_profile(self):
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        email = self.edit_email_input.text()
        cpf = self.edit_cpf_input.text()

        if not all([current_password, email, cpf]):
            QMessageBox.warning(self.edit_window, "Erro", "Preencha todos os campos obrigatórios!")
            return
        if new_password and new_password != confirm_password:
            QMessageBox.warning(self.edit_window, "Erro", "As senhas não coincidem!")
            return

        hashed_current = hash_password(current_password)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = %s", (self.username,))
            stored_password = cursor.fetchone()[0]
            if stored_password != hashed_current:
                QMessageBox.warning(self.edit_window, "Erro", "Senha atual incorreta!")
                conn.close()
                return
            if new_password:
                hashed_new = hash_password(new_password)
                cursor.execute("UPDATE users SET password = %s, email = %s, cpf = %s WHERE username = %s",
                               (hashed_new, email, cpf, self.username))
            else:
                cursor.execute("UPDATE users SET email = %s, cpf = %s WHERE username = %s",
                               (email, cpf, self.username))
            conn.commit()
            conn.close()
            QMessageBox.information(self.edit_window, "Sucesso", "Perfil atualizado com sucesso!")
            self.edit_window.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self.edit_window, "Erro", f"Erro ao atualizar perfil: {e}")

if __name__ == "__main__":
    # Criar o banco de dados antes de iniciar a aplicação
    criar_banco_de_dados()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QLineEdit {
            font-size: 16px;
            font-family: 'Roboto', 'Arial', 'Sans-Serif';
            border: 1px solid #bdc3c7;
            border-radius: 8px;
            padding: 10px;
            color: #2c3e50;
            background-color: white;
        }
        QLineEdit::placeholder {
            color: #7f8c8d;
            font-style: italic;
        }
        QLineEdit:focus {
            border: 1px solid #2c3e50;
            background-color: #f4f6f9;
        }
    """)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())