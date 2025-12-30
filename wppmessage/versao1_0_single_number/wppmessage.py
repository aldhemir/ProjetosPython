import sys
import pywhatkit as kit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurações iniciais da janela
        self.setObjectName("MainWindow")
        self.resize(664, 700)
        self.setMinimumSize(QtCore.QSize(500, 700))
        self.setStyleSheet("background-color: rgb(41,175,135);")
        
        # Variáveis de Estilo (Constants)
        self.STYLE_POPUP_ERROR = "background-color: rgb(252, 2, 20); border-radius: 10px;"
        self.STYLE_POPUP_OK = "background-color: rgb(0, 25, 123); border-radius: 10px;"
        
        self.STYLE_INPUT_OK = """
            border: 2px solid rgb(45,45,45);
            border-radius: 10px;
            padding: 15px;
            background-color: rgb(238, 238, 238);
            color: rgb(0, 0, 0);
        """
        
        self.STYLE_INPUT_ERROR = """
            border: 2px solid rgb(255,85,127);
            border-radius: 10px;
            padding: 15px;
            background-color: rgb(255,85,127);
            color: rgb(0, 0, 0);
        """
        
        self.STYLE_BUTTON = """
            QPushButton{
                border: 2px solid rgb(45,45,45);
                border-radius: 10px;
                padding: 15px;
                background-color: rgb(41,175,135);
                color: rgb(255, 255, 255);
            }
            QPushButton:hover{
                border: 3px solid rgb(55,55,55);
            }
        """

        # Inicializa a Interface
        self.setup_ui()
        self.retranslate_ui()
        
        # Conexões de Eventos (Signals & Slots)
        self.connect_signals()

    def setup_ui(self):
        # Widget Central
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        # --- Top Bar ---
        self.top_bar = QtWidgets.QFrame(self.centralwidget)
        self.top_bar.setMaximumSize(QtCore.QSize(16777215, 40))
        self.horizontalLayout_top = QtWidgets.QHBoxLayout(self.top_bar)
        self.horizontalLayout_top.setContentsMargins(0, 5, 0, 0)
        
        # Frame de Erro/Sucesso (Popup)
        self.frame_error = QtWidgets.QFrame(self.top_bar)
        self.frame_error.setMaximumSize(QtCore.QSize(400, 16777215))
        self.frame_error.setStyleSheet(self.STYLE_POPUP_ERROR)
        self.horizontalLayout_error = QtWidgets.QHBoxLayout(self.frame_error)
        self.horizontalLayout_error.setContentsMargins(10, 3, 10, 3)
        
        self.label_error = QtWidgets.QLabel(self.frame_error)
        self.label_error.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_error.addWidget(self.label_error)
        
        self.pushButton_closepopup = QtWidgets.QPushButton("X", self.frame_error)
        self.pushButton_closepopup.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_closepopup.setStyleSheet("QPushButton{border-radius: 5px; background-color: rgba(0,0,0,0.2); color: white;}")
        self.horizontalLayout_error.addWidget(self.pushButton_closepopup)
        
        self.horizontalLayout_top.addWidget(self.frame_error)
        self.frame_error.hide() # Começa oculto
        self.verticalLayout.addWidget(self.top_bar)

        # --- Conteúdo Principal ---
        self.content = QtWidgets.QFrame(self.centralwidget)
        self.layout_content = QtWidgets.QHBoxLayout(self.content)
        
        self.login_area = QtWidgets.QFrame(self.content)
        self.login_area.setMaximumSize(QtCore.QSize(450, 550))
        self.login_area.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 15px;")
        
        # Elementos do Formulário (Layout Manual mantido para preservar design original)
        self.label_titulo = QtWidgets.QLabel("WPPMESSAGE", self.login_area)
        self.label_titulo.setGeometry(QtCore.QRect(60, 20, 331, 31))
        font = QtGui.QFont("Muna", 13)
        self.label_titulo.setFont(font)
        self.label_titulo.setAlignment(QtCore.Qt.AlignCenter)

        self.label_subtitulo = QtWidgets.QLabel("Agende o envio de mensagem para o WhatsApp", self.login_area)
        self.label_subtitulo.setGeometry(QtCore.QRect(60, 50, 331, 31))
        self.label_subtitulo.setStyleSheet("color: rgb(209, 209, 209); font-size: 10pt;")
        self.label_subtitulo.setAlignment(QtCore.Qt.AlignCenter)

        self.input_numero = QtWidgets.QLineEdit(self.login_area)
        self.input_numero.setGeometry(QtCore.QRect(70, 100, 321, 50))
        self.input_numero.setStyleSheet(self.STYLE_INPUT_OK)
        self.input_numero.setMaxLength(11)
        self.input_numero.setPlaceholderText("DDD + Número (Ex: 11999999999)")

        self.input_mensagem = QtWidgets.QPlainTextEdit(self.login_area)
        self.input_mensagem.setGeometry(QtCore.QRect(70, 160, 321, 221))
        self.input_mensagem.setStyleSheet(self.STYLE_INPUT_OK)
        self.input_mensagem.setPlaceholderText("Digite sua mensagem ...")

        self.input_horario = QtWidgets.QLineEdit(self.login_area)
        self.input_horario.setGeometry(QtCore.QRect(70, 400, 321, 51))
        self.input_horario.setStyleSheet(self.STYLE_INPUT_OK)
        self.input_horario.setMaxLength(5)
        self.input_horario.setInputMask("00:00")
        self.input_horario.setPlaceholderText("Horário: 00:00")

        self.btn_enviar = QtWidgets.QPushButton("ENVIAR MENSAGEM", self.login_area)
        self.btn_enviar.setGeometry(QtCore.QRect(70, 480, 331, 51))
        self.btn_enviar.setStyleSheet(self.STYLE_BUTTON)
        self.btn_enviar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.layout_content.addWidget(self.login_area)
        self.verticalLayout.addWidget(self.content)

        # --- Rodapé ---
        self.bottom = QtWidgets.QFrame(self.centralwidget)
        self.bottom.setMaximumSize(QtCore.QSize(16777215, 35))
        self.layout_bottom = QtWidgets.QVBoxLayout(self.bottom)
        
        self.label_creditos = QtWidgets.QLabel(self.bottom)
        self.label_creditos.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_creditos.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.layout_bottom.addWidget(self.label_creditos)
        
        self.verticalLayout.addWidget(self.bottom)
        self.setCentralWidget(self.centralwidget)

    def retranslate_ui(self):
        self.setWindowTitle("WPP Message - Aldhemir Macedo")
        self.label_creditos.setText("Desenvolvido por Aldhemir Macedo | https://github.com/aldhemir")

    def connect_signals(self):
        self.pushButton_closepopup.clicked.connect(lambda: self.frame_error.hide())
        self.btn_enviar.clicked.connect(self.validar_e_enviar)

    def show_popup(self, message, is_error=True):
        self.label_error.setText(message)
        if is_error:
            self.frame_error.setStyleSheet(self.STYLE_POPUP_ERROR)
        else:
            self.frame_error.setStyleSheet(self.STYLE_POPUP_OK)
        self.frame_error.show()

    def limpar_campos(self):
        self.input_numero.setText("")
        self.input_mensagem.setPlainText("")
        self.input_horario.setText("")

    def validar_e_enviar(self):
        numero = self.input_numero.text().strip()
        mensagem = self.input_mensagem.toPlainText().strip()
        horario = self.input_horario.text().strip()

        erros = []

        # Validação Visual
        if not numero:
            self.input_numero.setStyleSheet(self.STYLE_INPUT_ERROR)
            erros.append("Número vazio")
        else:
            self.input_numero.setStyleSheet(self.STYLE_INPUT_OK)

        if not mensagem:
            self.input_mensagem.setStyleSheet(self.STYLE_INPUT_ERROR)
            erros.append("Mensagem vazia")
        else:
            self.input_mensagem.setStyleSheet(self.STYLE_INPUT_OK)

        if not horario or horario == ":":
            self.input_horario.setStyleSheet(self.STYLE_INPUT_ERROR)
            erros.append("Horário vazio")
        else:
            self.input_horario.setStyleSheet(self.STYLE_INPUT_OK)

        # Processamento
        if erros:
            self.show_popup(" | ".join(erros), is_error=True)
        else:
            try:
                # Tratamento do número
                full_number = f"+55{numero}"
                
                # Tratamento do horário
                hora_split = horario.split(':')
                h = int(hora_split[0])
                m = int(hora_split[1])

                # Envio (Nota: isso vai travar a UI por alguns segundos, comportamento padrão do pywhatkit)
                kit.sendwhatmsg(full_number, mensagem, h, m, 15, True, 3)
                
                self.show_popup("Mensagem Agendada/Enviada com Sucesso!", is_error=False)
                self.limpar_campos()
                
            except Exception as e:
                self.show_popup(f"Erro ao agendar: {str(e)}", is_error=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())