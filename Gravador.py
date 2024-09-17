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

    def interface(self):
        self.setWindowTitle("Amplay Gratuito")
        self.setGeometry()

    def design(self):
        pass

    def ajustar_tela(self):
        pass

    def gravar(self):
        pass

    def ver_pasta(self):
        pass
