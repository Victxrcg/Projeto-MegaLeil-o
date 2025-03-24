def button_style():
    return """
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
            background-color: #34495e;
        }
        QPushButton:pressed {
            background-color: #1a252f;
        }
    """
