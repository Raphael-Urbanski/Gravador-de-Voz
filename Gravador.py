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

# Tentei deixar o mais organizado possível, algumas linhas de código até eu tenho problema para entender, então se
# ficou muito difícil de entender, perdão!


class AnimatedButton(QPushButton):
    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.setIcon(icon)
        self.setIconSize(QSize(90, 90))
        self.setFixedSize(100, 100)
        self.default_icon_size = QSize(90, 90)

        self.animation = QPropertyAnimation(self, b"iconSize")
        self.animation.setDuration(200)

    def enterEvent(self, event):
        self.animation.stop()
        enlarged_icon_size = self.default_icon_size + QSize(10, 10)
        self.animation.setStartValue(self.iconSize())
        self.animation.setEndValue(enlarged_icon_size)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.iconSize())
        self.animation.setEndValue(self.default_icon_size)
        self.animation.start()
        super().leaveEvent(event)


class RenomearDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Renomear Gravação")
        self.setFixedSize(300, 100)
        self.new_name = ""

        layout = QVBoxLayout()

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Digite o novo nome do arquivo")
        layout.addWidget(self.input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )

        self.input.setStyleSheet("""
        QLineEdit {
            border: 1px solid black;
            border-bottom-right-radius: 10px;
            border-top-left-radius: 10px;
            padding: 5px;
            }
        """)

        ok_button = buttons.button(QDialogButtonBox.Ok)
        ok_button.setMaximumSize(100, 100)
        ok_button.setStyleSheet("""
        QPushButton {
            padding: 5px;
            }
        """)

        cancel_button = buttons.button(QDialogButtonBox.Cancel)
        cancel_button.setMaximumSize(100, 100)
        cancel_button.setStyleSheet("""
        QPushButton {
            padding: 5px;
            }
        """)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_new_name(self):
        return self.input.text()


class Gravador(QMainWindow):
    def __init__(self):
        super().__init__()

        self.interface()
        self.design()

        self.gravando = False
        self.frames = []
        self.stream = None
        self.stop_recording = False

    def interface(self):
        self.setWindowTitle("Amplay | Versão aberta")
        self.setFixedSize(650, 250)
        self.setWindowIcon(QIcon("imagens\\Rec.ico"))

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        widget_central = QWidget()

        # --------------------------------------------------------------------------------------------------------------

        self.title = QLabel("AmPlay [0.0.2]")
        self.title.setMaximumSize(650, 35)
        self.title.setAlignment(Qt.AlignCenter)

        self.frame_buttons = QFrame()
        frame_buttons_layout = QHBoxLayout()
        self.frame_buttons.setLayout(frame_buttons_layout)

        self.button_gravar = AnimatedButton(QIcon("imagens\\Rec.ico"), self)
        self.button_gravar.clicked.connect(self.gerenciar_button)

        self.button_pasta = AnimatedButton(QIcon("imagens\\Pasta.ico"), self)
        self.button_pasta.clicked.connect(self.ver_pasta)

        frame_buttons_layout.addWidget(self.button_gravar)
        frame_buttons_layout.addWidget(self.button_pasta)

        # --------------------------------------------------------------------------------------------------------------

        self.label_ampliato = QLabel("Acesse nosso site: <a href='https://www.ampliatodesign.com/gravador'>AmpliatoIdev</a>"
                                     " | Todos os direitos reservados")
        self.label_ampliato.setAlignment(Qt.AlignCenter)
        self.label_ampliato.setOpenExternalLinks(True)
        self.label_ampliato.setMaximumSize(650, 20)

        layout_principal = QVBoxLayout(widget_central)
        layout_principal.addWidget(self.title)
        layout_principal.addWidget(self.frame_buttons)
        layout_principal.addWidget(self.label_ampliato)
        widget_central.setLayout(layout_principal)

        title_font = QFont()
        title_font.setFamily("fixedsys")
        title_font.setPointSize(15)
        self.title.setFont(title_font)

        self.setCentralWidget(widget_central)

    def design(self):
        self.title.setStyleSheet("""
        QLabel {
            border: 1px solid black;
            background-color: #144E5E;
            color: white;
            border-top-left-radius: 10px;
            border-bottom-right-radius: 10px;
            }
        """)

        self.frame_buttons.setStyleSheet("""
        QFrame {
            border: 1px solid black;
            border-top-left-radius: 10px;
            border-bottom-right-radius: 10px;
            }
        """)

        self.button_gravar.setStyleSheet("""
        QPushButton {
            border-radius: 5px;
            }
        """)

        self.button_pasta.setStyleSheet("""
        QPushButton {
            border-radius: 5px;
            }
        """)

    def gerenciar_button(self):
        if not self.gravando:
            self.gravar()
        else:
            self.parar()

    def config_input(self):
        while not self.stop_recording and self.stream.is_active():
            try:
                bloco = self.stream.read(1024)
                self.frames.append(bloco)
            except Exception as e:
                print(f"Erro ao ler o stream: {e}")
                break

    def gravar(self):
        if not self.gravando:

            try:
                self.audio = pyaudio.PyAudio()
                info = self.audio.get_host_api_info_by_index(0)
                numdevices = info.get("deviceCount")

                for i in range(0, numdevices):
                    if self.audio.get_device_info_by_host_api_device_index(0, i).get("maxInputChannels") > 0:
                        self.statusbar.showMessage("Gravando")
                        self.button_gravar.setIcon(QIcon("imagens\\Stop.ico"))
                        self.gravando = True
                        self.stream = self.audio.open(
                            format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            frames_per_buffer=1024,
                            input=True,
                            input_device_index=i
                        )
                        break
                else:
                    QMessageBox.critical(self, "Erro", "Nenhum microfone detectado!")
                    return

                self.frames = []
                self.thread_gravacao = threading.Thread(target=self.config_input)
                self.thread_gravacao.start()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Algo inesperado aconteceu! Erro: {e}")
                if self.stream:
                    self.stream.stop_stream()
                    self.stream.close()

    def parar(self):
        self.statusbar.showMessage("Gravação Terminada")
        self.button_gravar.setIcon(QIcon("imagens\\Rec.ico"))
        self.gravando = False

        self.stop_recording = True

        # Salve o arquivo como temporário
        videos_path = os.path.join(os.path.expanduser("~"), "Music")
        temp_file_path = os.path.join(videos_path, "Gravação_temp.wav")

        file = QFile(temp_file_path)
        if not file.open(QIODevice.WriteOnly):
            QMessageBox.critical(self, "Erro", "Não foi possível salvar a gravação.")
            return

        out_file = wave.open(file.fileName(), 'wb')
        out_file.setnchannels(1)
        out_file.setframerate(44100)
        out_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        out_file.writeframes(b"".join(self.frames))
        out_file.close()
        file.close()

        # Agora, abra o diálogo de renomeação
        self.abrir_renomear_dialog(temp_file_path)

        if self.thread_gravacao.is_alive():
            self.thread_gravacao.join()

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.audio.terminate()

        self.stop_recording = False

    def abrir_renomear_dialog(self, temp_file_path):
        dialog = RenomearDialog(self)
        while True:
            if dialog.exec_() == QDialog.Accepted:
                new_name = dialog.get_new_name()
                if new_name:
                    new_name += ".wav" if not new_name.endswith(".wav") else ""
                    new_file_path = os.path.join(os.path.dirname(temp_file_path), new_name)
                    file = QFile(temp_file_path)

                    if os.path.exists(new_file_path):
                        reply = QMessageBox.question(self, 'Sobrescrever',
                                                     f'O arquivo "{new_name}" já existe. Deseja sobrescrevê-lo?',
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if reply == QMessageBox.No:
                            continue
                        elif reply == QMessageBox.Yes:
                            os.remove(new_file_path)
                            file.rename(new_file_path)
                            QMessageBox.information(self, "Sucesso", f"Arquivo {new_name} substituído.")
                            break
                    else:
                        if not file.rename(new_file_path):
                            QMessageBox.critical(self, "Erro", f"Falha ao renomear o arquivo: {file.errorString()}")
                        else:
                            QMessageBox.information(self, "Sucesso", f"Arquivo salvo como {new_file_path}")
                        break
            else:
                break

    def ver_pasta(self):
        videos_path = os.path.join(os.path.expanduser("~"), "Music")
        subprocess.Popen(f'explorer "{videos_path}"')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gravador()
    ex.show()
    sys.exit(app.exec_())
