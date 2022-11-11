import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWebEngineWidgets import QWebEngineView

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QWidget):
    # constructor
    def __init__(self, chartable):
        # QWidget constructor
        QWidget.__init__(self)

        self.character_table = chartable

        # buttons
        self.search_button = QPushButton("Search")
        self.search_button.setMaximumWidth(200)
        self.replay_button = QPushButton("Replay")
        self.replay_button.setMaximumWidth(200)

        # character input field
        self.char_input = QLineEdit()
        self.char_input.setMaxLength(1)
        self.char_input.setMaximumWidth(50)
        self.char_input.setText('')

        self.svg_viewer = QWebEngineView()
        self.svg_viewer.setFixedHeight(250)
        self.svg_viewer.setFixedWidth(250)
        # enabled by default
        # self.svgView.settings().setAttribute(
        #       QWebEngineSettings.LocalContentCanAccessFileUrls,
        #       True
        # )

        # form layout for character input
        self.f_layout = QFormLayout()
        self.f_layout.addRow("Input character: ", self.char_input)
        self.f_layout.setAlignment(Qt.AlignCenter)
        
        self.def_title = QLabel()
        self.def_title.setText("Definition:")
        self.def_title.setWordWrap(False)

        self.def_str = QLabel()
        self.def_str.setText('')
        self.def_str.setWordWrap(True)

        # self.definition_f_layout = QFormLayout()
        # self.definition_f_layout.addRow("Definition:", self.def_str)
        # self.definition_f_layout.setAlignment(Qt.AlignBaseline)

        self.pinyin_title = QLabel()
        self.pinyin_title.setText("Pinyin:")
        self.pinyin_title.setWordWrap(False)

        self.pinyin_str = QLabel()
        self.pinyin_str.setText('')
        self.pinyin_str.setWordWrap(True)

        # self.pinyin_f_layout = QFormLayout()
        # self.pinyin_f_layout.addRow("Pinyin:", self.pinyin_str)
        # self.pinyin_f_layout.setAlignment(Qt.AlignBaseline)

        # main grid layout (layout/widget, row num, col num, row span, col span)
        self.g_layout = QGridLayout()
        self.g_layout.setAlignment(Qt.AlignCenter)
        self.g_layout.setColumnStretch(0,1)
        self.g_layout.setColumnStretch(1,3)
        self.g_layout.addLayout(self.f_layout, 0, 0, 1, 2, Qt.AlignHCenter)
        self.g_layout.addWidget(self.search_button, 1, 0, 1, 2)
        self.g_layout.addWidget(self.replay_button, 1, 2, 1, 2)
        self.g_layout.addWidget(self.svg_viewer, 2, 0, 1, 4, Qt.AlignCenter)
        self.g_layout.addWidget(self.pinyin_title, 3, 0, 1, 1)
        self.g_layout.addWidget(self.pinyin_str, 3, 1, 1, 3)
        self.g_layout.addWidget(self.def_title, 4, 0, 1, 1)
        self.g_layout.addWidget(self.def_str, 4, 1, 1, 3)
        

        # load layout
        self.setLayout(self.g_layout)

        # connections/signals
        self.search_button.clicked.connect(self.load_new)
        self.replay_button.clicked.connect(self.replay)

    def load_new(self):
        #html = "<!DOCTYPE html>
        #        <html>
        #           <body style=\"overflow: hidden\">
        #               <object type = \"image/svg+xml\" data =\"" + url.toString() + "\">
        #               </object>
        #           </body>
        #        </html>"
        #htmlBytesArray = QByteArray(bytes(html, 'utf8'))
        # self.svgView.setHtml(html)

        # write html to the svgviewer window as a message to the user
        # if there is no character to view

        old_size = self.sizeHint()
        if self.char_input.text() == '':
            html = """
                <!DOCTYPE html>
                <html>
                    <body style=\"font-family:sans-serif\">
                        <h2>Type in a character above to view the stroke order...</h2>
                    </body>
                </html>
                """
            self.svg_viewer.setHtml(html)
            self.pinyin_str.setText('')
            self.def_str.setText('')
        # show the character stroke svg if there is a character in the box
        else:
            path = os.path.join(
                    os.path.split(os.path.abspath(__file__))[0], 
                    'svgs',
                    str(ord(self.char_input.text())) + '.svg')
            url  = QUrl().fromLocalFile(path)
            self.svg_viewer.load(url)
            self.get_data(self.char_input.text())
            
        self.resizeEvent(QResizeEvent(old_size, self.sizeHint()))           
        self.resize(self.sizeHint())
        
        
        

    # reload the svgviewer window to simulate replaying the stroke order
    def replay(self):
        self.svg_viewer.reload()

    def get_data(self, char):
        data = self.character_table.get_character_data(char)
        self.def_str.setText(data[0])
        self.pinyin_str.setText(data[1])