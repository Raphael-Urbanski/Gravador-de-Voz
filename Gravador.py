import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyaudio
import wave
import threading
import time
import os
import subprocess


class Gravador(QMainWindow):
    def __init__(self):
        super().__init__()

        self.interface()
        self.design()

        self.gravando = False

    def interface(self):
        self.setWindowTitle("Amplay Gratuito")
        self.setFixedSize(650, 250)
        self.setWindowIcon(QIcon("imagens\\Rec.ico"))

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        widget_central = QWidget()

        # --------------------------------------------------------------------------------------------------------------

        self.title = QLabel("AmPlay [Versão Teste]")
        self.title.setMaximumSize(3000, 25)
        self.title.setAlignment(Qt.AlignCenter)

        self.frame_buttons = QFrame()
        frame_buttons_layout = QHBoxLayout()
        self.frame_buttons.setLayout(frame_buttons_layout)

        self.button_gravar = QPushButton()
        self.button_gravar.setIcon(QIcon("imagens\\Rec.ico"))
        self.button_gravar.setIconSize(QSize(90, 90))
        self.button_gravar.setFixedSize(100, 100)
        self.button_gravar.clicked.connect(self.gravar_parar)

        self.button_pasta = QPushButton()
        self.button_pasta.setIcon(QIcon("imagens\\Pasta.ico"))
        self.button_pasta.setIconSize(QSize(90, 90))
        self.button_pasta.setFixedSize(100, 100)

        frame_buttons_layout.addWidget(self.button_gravar)
        frame_buttons_layout.addWidget(self.button_pasta)

        # --------------------------------------------------------------------------------------------------------------

        self.frame_final = QFrame()
        frame_final_layout = QHBoxLayout()
        self.frame_final.setLayout(frame_final_layout)

        layout_principal = QVBoxLayout(widget_central)
        layout_principal.addWidget(self.title)
        layout_principal.addWidget(self.frame_buttons)
        widget_central.setLayout(layout_principal)

        self.setCentralWidget(widget_central)

    def design(self):
        self.title.setStyleSheet("""
        QLabel {
            border: 1px solid black;
            background-color: #144E5E;
            color: white;
            }
        """)

        self.frame_buttons.setStyleSheet("""
        QFrame {
            border: 1px solid black;
            }
        """)

        self.button_gravar.setStyleSheet("""
        QPushButton {
            border-radius: 5px;
            background-color: #8DA7BE;
            }
            
        QPushButton:hover {
            border: 1px solid black;
            }
        """)

        self.button_pasta.setStyleSheet("""
        QPushButton {
            border-radius: 5px;
            background-color: #8DA7BE;
            }

        QPushButton:hover {
            border: 1px solid black;
            }
        """)

    def gravar_parar(self):
        if not self.gravando:
            self.statusbar.showMessage("Gravando")
            self.button_gravar.setIcon(QIcon("imagens\\Stop.ico"))
            self.gravando = True
        else:
            self.statusbar.showMessage("Gravação Terminada")
            self.button_gravar.setIcon(QIcon("imagens\\Rec.ico"))
            self.gravando = False

    def ver_pasta(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gravador()
    ex.show()
    sys.exit(app.exec_())
