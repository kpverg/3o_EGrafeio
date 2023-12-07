 
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor

def apply_style(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 165, 0))  # Πορτοκαλί φόντο
    palette.setColor(QPalette.Button, QColor(0, 191, 255))  # Γαλάζιο χρώμα για τα κουμπιά
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # Άσπρο κείμενο για τα κουμπιά
    app.setPalette(palette)