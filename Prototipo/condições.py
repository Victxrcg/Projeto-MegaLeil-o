import mysql.connector
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton, QScrollArea, QMessageBox,
                               QFileDialog, QTabWidget, QToolButton, QGridLayout)
from PySide6.QtGui import QPixmap, Qt, QFont, QIcon, QImage
from PySide6.QtCore import QSize
from MegaLeilaoBD import *
from janelaprincipal import determine_condition

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