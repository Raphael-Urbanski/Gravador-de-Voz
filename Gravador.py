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

        self.fundo_gravador = QFrame()
        fundo_gravador_layout = QVBoxLayout()
        self.fundo_gravador.setLayout(fundo_gravador_layout)

        self.title = QLabel("AmPlay [Versão Teste]")
        self.title.setMaximumSize(3000, 25)
        self.title.setAlignment(Qt.AlignCenter)

        frame_buttons = QFrame()
        frame_buttons_layout = QHBoxLayout()
        frame_buttons.setLayout(frame_buttons_layout)

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

        fundo_gravador_layout.addWidget(self.title)
        fundo_gravador_layout.addWidget(frame_buttons)

        layout_principal = QVBoxLayout(widget_central)
        layout_principal.addWidget(self.fundo_gravador)
        widget_central.setLayout(layout_principal)

        self.setCentralWidget(widget_central)

    def design(self):
        self.title.setStyleSheet("""
        QLabel {
            border: 1px solid black;
            }
        """)

        self.fundo_gravador.setStyleSheet("""
        QFrame {
             border: 1px solid black;
            }
        """)

        self.button_gravar.setStyleSheet("""
        QPushButton {
            border-radius: 5px;
            }
            
        QPushButton:hover {
            border: 1px solid black;
            }
        """)

        self.button_pasta.setStyleSheet("""
        QPushButton {
            border-radius: 5px;
            }

        QPushButton:hover {
            border: 1px solid black;
            }
        """)

    def resizeEvent(self, event):
        tamanho = self.size()

        self.fundo_gravador.setFixedSize(tamanho.width() - 20, tamanho.height() - 35)

    def gravar_parar(self):
        if not self.gravando:
            print("gravando")
            self.button_gravar.setIcon(QIcon("imagens\\Stop.ico"))
            self.gravando = True
        else:
            print("Parando")
            self.button_gravar.setIcon(QIcon("imagens\\Rec.ico"))
            self.gravando = False

    def ver_pasta(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gravador()
    ex.show()
    sys.exit(app.exec_())
