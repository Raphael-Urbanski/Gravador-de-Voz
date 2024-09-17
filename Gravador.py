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

    def interface(self):
        self.setWindowTitle("Amplay Gratuito")
        self.setGeometry(200, 200, 650, 250)
        self.setMinimumSize(650, 250)
        # Adicionar icon

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

        self.button_gravar = QPushButton("GRAVAR")

        self.button_pasta = QPushButton("GRAVAÇÕES")

        fundo_gravador_layout.addWidget(self.title)

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

    def resizeEvent(self, event):
        tamanho = self.size()

        self.fundo_gravador.setFixedSize(tamanho.width() - 20, tamanho.height() - 35)

    def gravar(self):
        pass

    def ver_pasta(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gravador()
    ex.show()
    sys.exit(app.exec_())
