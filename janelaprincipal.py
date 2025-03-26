import mysql.connector
import shutil
import os
from MegaLeilaoBD import *
from estilizacao import button_style
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox,
                               QFileDialog, QTabWidget, QToolButton, QGridLayout, QComboBox)
from PySide6.QtGui import QPixmap, Qt, QFont, QIcon, QImage
from PySide6.QtCore import QSize

from condition import determine_condition

# Nova classe para a janela de detalhes de pagamento
class PaymentDetailsWindow(QMainWindow):
    def __init__(self, vehicle_id, vehicle_name, vehicle_price, vehicle_desc, vehicle_image_path, username, parent=None):
        super().__init__(parent)
        self.vehicle_id = vehicle_id
        self.vehicle_name = vehicle_name
        self.vehicle_price = vehicle_price
        self.vehicle_desc = vehicle_desc
        self.vehicle_image_path = vehicle_image_path
        self.username = username
        self.setWindowTitle("Detalhes de Pagamento - MegaLeilão")
        
        # Definir o tamanho fixo da janela (não redimensionável)
        self.setFixedSize(900, 650)  # Aumentei um pouco para melhor espaçamento
        
        # Desabilitar o botão de maximizar
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        
        # Centralizar a janela na tela
        self.center_on_screen()
        
        self.setup_ui()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def setup_ui(self):
        # Estilo geral da janela
        self.setStyleSheet("background-color: #f5f7fa;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Título da janela
        title_label = QLabel("Finalizar Compra")
        title_label.setFont(QFont("Roboto", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # Container principal para o formulário de compra
        buy_form_frame = QFrame()
        buy_form_frame.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        """)
        form_layout = QHBoxLayout(buy_form_frame)
        form_layout.setSpacing(30)
        form_layout.setContentsMargins(20, 20, 20, 20)

        # Lado esquerdo: Imagem, Preço, Nome do Veículo e Descrição
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        # Imagem
        self.buy_image = QLabel()
        self.buy_image.setFixedSize(350, 250)  # Aumentei o tamanho da imagem
        self.buy_image.setStyleSheet("border: 1px solid #e0e4e8; border-radius: 10px; background-color: #f9f9f9;")
        self.buy_image.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(self.vehicle_image_path if self.vehicle_image_path else "default.png")
        if not pixmap.isNull():
            self.buy_image.setPixmap(pixmap.scaled(350, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.buy_image.setText("Sem Imagem")
            self.buy_image.setStyleSheet("color: #7f8c8d; font-size: 16px;")
        left_layout.addWidget(self.buy_image)

        # Preço
        price_frame = QFrame()
        price_frame.setStyleSheet("background-color: #ecf0f1; border-radius: 8px; padding: 10px;")
        price_layout = QHBoxLayout(price_frame)
        price_label = QLabel("Preço:")
        price_label.setFont(QFont("Roboto", 14, QFont.Bold))
        price_label.setStyleSheet("color: #2c3e50;")
        price_layout.addWidget(price_label)
        self.buy_price = QLabel(f"R$ {self.vehicle_price:,.2f}")
        self.buy_price.setFont(QFont("Roboto", 14, QFont.Bold))
        self.buy_price.setStyleSheet("color: #e74c3c;")
        price_layout.addWidget(self.buy_price)
        price_layout.addStretch()
        left_layout.addWidget(price_frame)

        # Nome do Veículo
        name_frame = QFrame()
        name_layout = QVBoxLayout(name_frame)
        name_label = QLabel("Nome do Veículo:")
        name_label.setFont(QFont("Roboto", 14, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        name_layout.addWidget(name_label)
        self.vehicle_name_input = QLineEdit()
        self.vehicle_name_input.setStyleSheet("""
            font-size: 16px;
            border: 1px solid #d1d5db;
            border-radius: 5px;
            padding: 10px;
            background-color: #f9f9f9;
        """)
        self.vehicle_name_input.setFixedHeight(40)
        self.vehicle_name_input.setText(self.vehicle_name)
        self.vehicle_name_input.setReadOnly(True)
        name_layout.addWidget(self.vehicle_name_input)
        left_layout.addWidget(name_frame)

        # Descrição
        desc_frame = QFrame()
        desc_layout = QVBoxLayout(desc_frame)
        desc_label = QLabel("Descrição:")
        desc_label.setFont(QFont("Roboto", 14, QFont.Bold))
        desc_label.setStyleSheet("color: #2c3e50;")
        desc_layout.addWidget(desc_label)
        self.vehicle_desc_input = QLineEdit()
        self.vehicle_desc_input.setStyleSheet("""
            font-size: 16px;
            border: 1px solid #d1d5db;
            border-radius: 5px;
            padding: 10px;
            background-color: #f9f9f9;
        """)
        self.vehicle_desc_input.setFixedHeight(40)
        self.vehicle_desc_input.setText(self.vehicle_desc if self.vehicle_desc else "Nenhuma descrição disponível")
        self.vehicle_desc_input.setReadOnly(True)
        desc_layout.addWidget(self.vehicle_desc_input)
        left_layout.addWidget(desc_frame)

        form_layout.addLayout(left_layout)

        # Lado direito: Formulário
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)

        # Título do formulário
        form_title = QLabel("Informações do Comprador")
        form_title.setFont(QFont("Roboto", 22, QFont.Bold))
        form_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        right_layout.addWidget(form_title)

        # Nome
        name_frame = QFrame()
        name_layout = QVBoxLayout(name_frame)
        name_label = QLabel("Nome Completo:*")
        name_label.setFont(QFont("Roboto", 14))
        name_label.setStyleSheet("color: #2c3e50;")
        name_layout.addWidget(name_label)
        self.buyer_name = QLineEdit()
        self.buyer_name.setPlaceholderText("Digite seu nome completo")
        self.buyer_name.setStyleSheet("""
            font-size: 16px;
            border: 1px solid #d1d5db;
            border-radius: 5px;
            padding: 10px;
        """)
        self.buyer_name.setFixedHeight(40)
        name_layout.addWidget(self.buyer_name)
        right_layout.addWidget(name_frame)

        # Email
        email_frame = QFrame()
        email_layout = QVBoxLayout(email_frame)
        email_label = QLabel("Email:*")
        email_label.setFont(QFont("Roboto", 14))
        email_label.setStyleSheet("color: #2c3e50;")
        email_layout.addWidget(email_label)
        self.buyer_email = QLineEdit()
        self.buyer_email.setPlaceholderText("Digite seu email")
        self.buyer_email.setStyleSheet("""
            font-size: 16px;
            border: 1px solid #d1d5db;
            border-radius: 5px;
            padding: 10px;
        """)
        self.buyer_email.setFixedHeight(40)
        email_layout.addWidget(self.buyer_email)
        right_layout.addWidget(email_frame)

        # Telefone
        phone_frame = QFrame()
        phone_layout = QVBoxLayout(phone_frame)
        phone_label = QLabel("Telefone:*")
        phone_label.setFont(QFont("Roboto", 14))
        phone_label.setStyleSheet("color: #2c3e50;")
        phone_layout.addWidget(phone_label)
        self.buyer_phone = QLineEdit()
        self.buyer_phone.setPlaceholderText("Digite seu telefone")
        self.buyer_phone.setStyleSheet("""
            font-size: 16px;
            border: 1px solid #d1d5db;
            border-radius: 5px;
            padding: 10px;
        """)
        self.buyer_phone.setFixedHeight(40)
        phone_layout.addWidget(self.buyer_phone)
        right_layout.addWidget(phone_frame)

        # Forma de Pagamento
        payment_frame = QFrame()
        payment_layout = QVBoxLayout(payment_frame)
        payment_label = QLabel("Forma de Pagamento:*")
        payment_label.setFont(QFont("Roboto", 12))
        payment_label.setStyleSheet("color: #2c3e50;")
        payment_layout.addWidget(payment_label)
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Selecione uma opção", "Débito", "Crédito", "Pix"])
        self.payment_method.setStyleSheet("""
            font-size: 14px;
            border: 1px solid #d1d5db;
            border-radius: 5px;
            padding: 5px;
        """)
        self.payment_method.setFixedHeight(40)
        payment_layout.addWidget(self.payment_method)
        right_layout.addWidget(payment_frame)

        right_layout.addStretch()  # Para empurrar os campos para o topo

        form_layout.addLayout(right_layout)

        main_layout.addWidget(buy_form_frame)

        # Botões Confirmar e Cancelar
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet("""
            QPushButton {
            background-color: #2c3e50;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-family: 'Roboto', 'Sans';
            font-weight: bold;
            padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)

        confirm_btn = QPushButton("Confirmar Compra")
        confirm_btn.setStyleSheet("""
            QPushButton {
            background-color: #2c3e50;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-family: 'Roboto', 'Sans';
            font-weight: bold;
            padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        confirm_btn.clicked.connect(self.confirm_purchase)
        button_layout.addWidget(confirm_btn)

        main_layout.addLayout(button_layout)

    def confirm_purchase(self):
        buyer_name = self.buyer_name.text().strip()
        buyer_email = self.buyer_email.text().strip()
        buyer_phone = self.buyer_phone.text().strip()
        payment_method = self.payment_method.currentText()
        vehicle_name = self.vehicle_name_input.text().strip()

        # Validação dos campos
        if not all([buyer_name, buyer_email, buyer_phone, vehicle_name]) or payment_method == "Selecione uma opção":
            # Destacar campos não preenchidos
            if not buyer_name:
                self.buyer_name.setStyleSheet("""
                    font-size: 14px;
                    border: 1px solid #e74c3c;
                    border-radius: 8px;
                    padding: 10px;
                """)
            if not buyer_email:
                self.buyer_email.setStyleSheet("""
                    font-size: 14px;
                    border: 1px solid #e74c3c;
                    border-radius: 8px;
                    padding: 10px;
                """)
            if not buyer_phone:
                self.buyer_phone.setStyleSheet("""
                    font-size: 14px;
                    border: 1px solid #e74c3c;
                    border-radius: 8px;
                    padding: 10px;
                """)
            if payment_method == "Selecione uma opção":
                self.payment_method.setStyleSheet("""
                    font-size: 14px;
                    border: 1px solid #e74c3c;
                    border-radius: 8px;
                    padding: 10px;
                """)
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios!")
            return

        # Validação de email
        if '@' not in buyer_email or '.' not in buyer_email.split('@')[1]:
            self.buyer_email.setStyleSheet("""
                font-size: 14px;
                border: 1px solid #e74c3c;
                border-radius: 8px;
                padding: 10px;
            """)
            QMessageBox.warning(self, "Erro", "Email inválido!")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Buscar o id do usuário com base no username
            cursor.execute("SELECT id FROM usuarios WHERE nome = %s", (self.username,))
            user = cursor.fetchone()

            if not user:
                QMessageBox.critical(self, "Erro", "Usuário não encontrado!")
                conn.close()
                return

            user_id = user[0]

            # Atualizar o veículo como vendido
            cursor.execute("UPDATE veiculos SET status = 'vendido', buyer_id = %s WHERE id = %s", (user_id, self.vehicle_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Sucesso", f"Compra de {vehicle_name} realizada com sucesso!")
            self.close()
            # Atualizar as abas no MainWindow
            self.parent().load_vehicles()
            self.parent().load_history()
            self.parent().tabs.setCurrentIndex(2)  # Vai para a aba Histórico

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao confirmar compra: {e}")

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
        self.btn_novo.setStyleSheet(button_style())
        self.btn_novo.setFixedHeight(50)
        self.btn_novo.clicked.connect(lambda: self.filter_vehicles("Novo"))
        menu_layout.addWidget(self.btn_novo)

        self.btn_usado = QPushButton("Usado")
        self.btn_usado.setStyleSheet(button_style())
        self.btn_usado.setFixedHeight(50)
        self.btn_usado.clicked.connect(lambda: self.filter_vehicles("Usado"))
        menu_layout.addWidget(self.btn_usado)

        menu_layout.addSpacing(30)

        opcoes_label = QLabel("Opções")
        opcoes_label.setFont(QFont("Roboto", 20, QFont.Bold))
        opcoes_label.setStyleSheet("color: #ecf0f1;")
        menu_layout.addWidget(opcoes_label)

        self.btn_comprar = QPushButton("Comprar")
        self.btn_comprar.setStyleSheet(button_style())
        self.btn_comprar.setFixedHeight(50)
        self.btn_comprar.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        menu_layout.addWidget(self.btn_comprar)

        self.btn_vender = QPushButton("Vender")
        self.btn_vender.setStyleSheet(button_style())
        self.btn_vender.setFixedHeight(50)
        self.btn_vender.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        menu_layout.addWidget(self.btn_vender)

        self.btn_historico = QPushButton("Histórico")
        self.btn_historico.setStyleSheet(button_style())
        self.btn_historico.setFixedHeight(50)
        self.btn_historico.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
        menu_layout.addWidget(self.btn_historico)

        self.btn_editar_perfil = QPushButton("Editar Perfil")
        self.btn_editar_perfil.setStyleSheet(button_style())
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
        self.search_bar.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.search_bar.setFixedHeight(40)
        self.search_bar.setMaximumWidth(400)
        self.search_bar.textChanged.connect(self.search_vehicles)
        header_layout.addWidget(self.search_bar)

        welcome_label = QLabel(f"Bem-vindo, {self.username}")
        welcome_label.setFont(QFont("Roboto", 14))
        welcome_label.setStyleSheet("color: #7f8c8d;")
        header_layout.addWidget(welcome_label)

        sair_btn = QPushButton("Sair")
        sair_btn.setStyleSheet(button_style())
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
        self.sell_name.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.sell_name.setFixedHeight(45)
        form_layout.addWidget(self.sell_name)

        self.sell_price = QLineEdit()
        self.sell_price.setPlaceholderText("Preço (R$)")
        self.sell_price.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.sell_price.setFixedHeight(45)
        form_layout.addWidget(self.sell_price)

        self.sell_desc = QLineEdit()
        self.sell_desc.setPlaceholderText("Descrição")
        self.sell_desc.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.sell_desc.setFixedHeight(45)
        form_layout.addWidget(self.sell_desc)

        self.sell_image_path = QLineEdit()
        self.sell_image_path.setPlaceholderText("Caminho da Imagem")
        self.sell_image_path.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        self.sell_image_path.setFixedHeight(45)
        form_layout.addWidget(self.sell_image_path)

        self.image_preview = QLabel()
        self.image_preview.setFixedSize(280, 180)
        self.image_preview.setStyleSheet("border: 1px solid #ecf0f1; border-radius: 5px; background-color: white;")
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setText("Nenhuma imagem selecionada")
        form_layout.addWidget(self.image_preview)

        browse_btn = QPushButton("Escolher Imagem")
        browse_btn.setStyleSheet(button_style())
        browse_btn.setFixedSize(170, 45)
        browse_btn.clicked.connect(self.browse_image)
        form_layout.addWidget(browse_btn)

        submit_btn = QPushButton("Enviar Veículo")
        submit_btn.setStyleSheet(button_style())
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
            query = "SELECT id, nome, preco, descricao, imagem_caminho FROM veiculos WHERE status = 'disponivel'"
            params = []
            if filter_type:
                if filter_type == "Novo":
                    query += " AND preco > 100000"
                elif filter_type == "Usado":
                    query += " AND preco <= 100000"
            if search_query:
                query += " AND (nome LIKE %s OR descricao LIKE %s)"
                params.extend([f"%{search_query}%", f"%{search_query}%"])
            cursor.execute(query, params)
            vehicles = cursor.fetchall()

            if not vehicles:
                no_vehicles_label = QLabel("Nenhum veículo encontrado!")
                no_vehicles_label.setStyleSheet("font-size: 20px; color: #7f8c8d;")
                self.grid_layout.addWidget(no_vehicles_label, 0, 0, alignment=Qt.AlignCenter)
                return

            for idx, (vehicle_id, name, price, desc, image_path) in enumerate(vehicles):
                condition = determine_condition(price)
                card = self.create_vehicle_card(vehicle_id, name, price, desc, image_path, condition)
                row = idx // 3
                col = idx % 3
                self.grid_layout.addWidget(card, row, col, alignment=Qt.AlignCenter)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar veículos: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def load_history(self):
        while self.history_grid.count():
            item = self.history_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Buscar o ID do usuário com base no username
            cursor.execute("SELECT id FROM usuarios WHERE nome = %s", (self.username,))
            user = cursor.fetchone()

            if not user:
                QMessageBox.critical(self, "Erro", "Usuário não encontrado!")
                conn.close()
                return

            user_id = user[0]  # Obtém o id do usuário

            # Buscar veículos com status 'vendido' e buyer_id correspondente ao user_id
            cursor.execute("SELECT id, nome, preco, descricao, imagem_caminho FROM veiculos WHERE status = 'vendido' AND buyer_id = %s", (user_id,))
            vehicles = cursor.fetchall()

            if not vehicles:
                no_history_label = QLabel("Nenhum veículo comprado ainda!")
                no_history_label.setStyleSheet("font-size: 20px; color: #7f8c8d;")
                self.history_grid.addWidget(no_history_label, 0, 0, alignment=Qt.AlignCenter)
                return

            for idx, (vehicle_id, name, price, desc, image_path) in enumerate(vehicles):
                condition = determine_condition(price)
                card = self.create_vehicle_card(vehicle_id, name, price, desc, image_path, condition, is_history=True)
                row = idx // 3
                col = idx % 3
                self.history_grid.addWidget(card, row, col, alignment=Qt.AlignCenter)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar histórico: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

    def create_vehicle_card(self, vehicle_id, name, price, desc, image_path, condition, is_history=False):
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

        name_label = QLabel(f"{name} ({condition})")
        name_label.setFont(QFont("Roboto", 16, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(name_label)

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
            buy_btn.setStyleSheet(button_style())
            buy_btn.clicked.connect(lambda: self.show_payment_details(vehicle_id, name, price, desc, image_path))
            layout.addWidget(buy_btn, alignment=Qt.AlignCenter)

        return card

    def show_payment_details(self, vehicle_id, name, price, desc, image_path):
        self.payment_window = PaymentDetailsWindow(vehicle_id, name, price, desc, image_path, self.username, self)
        self.payment_window.show()

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
            cursor.execute("INSERT INTO veiculos (nome, preco, descricao, imagem_caminho) VALUES (%s, %s, %s, %s)",
                           (name, price, desc, image_path))
            conn.commit()
            QMessageBox.information(self, "Sucesso", "Veículo cadastrado com sucesso!")
            self.sell_name.clear()
            self.sell_price.clear()
            self.sell_desc.clear()
            self.sell_image_path.clear()
            self.image_preview.setText("Nenhuma imagem selecionada")
            self.tabs.setCurrentIndex(0)
            self.load_vehicles()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar veículo: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

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
        self.edit_window.setGeometry(300, 300, 450, 550)
        
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

        self.current_password_input = QLineEdit()
        self.current_password_input.setPlaceholderText("Senha Atual")
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        edit_layout.addWidget(self.current_password_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Nova Senha")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        edit_layout.addWidget(self.new_password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirme a Nova Senha")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("font-size: 16px; border: 1px solid #bdc3c7; border-radius: 8px; padding: 10px;")
        edit_layout.addWidget(self.confirm_password_input)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Salvar")
        save_btn.setStyleSheet(button_style())
        save_btn.clicked.connect(self.save_profile)
        btn_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet(button_style())
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

        if not all([current_password, new_password, confirm_password]):
            QMessageBox.warning(self.edit_window, "Erro", "Preencha todos os campos!")
            return
        if new_password != confirm_password:
            QMessageBox.warning(self.edit_window, "Erro", "As senhas não coincidem!")
            return

        hashed_current = hash_password(current_password)
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT senha FROM usuarios WHERE nome = %s", (self.username,))
            stored_password = cursor.fetchone()[0]
            if stored_password != hashed_current:
                QMessageBox.warning(self.edit_window, "Erro", "Senha atual incorreta!")
                conn.close()
                return
            hashed_new = hash_password(new_password)
            cursor.execute("UPDATE usuarios SET senha = %s WHERE nome = %s", (str(hashed_new), self.username))
            conn.commit()
            QMessageBox.information(self.edit_window, "Sucesso", "Perfil atualizado com sucesso!")
            self.edit_window.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self.edit_window, "Erro", f"Erro ao atualizar perfil: {e}")
        finally:
            if 'conn' in locals():
                conn.close()