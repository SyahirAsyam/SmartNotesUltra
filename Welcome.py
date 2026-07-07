from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
print("WELCOME.PY VERSI BARU LOADED")

class WelcomeScreen(QWidget):

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        self.setWindowTitle(
            "Ultra Smart Notes V5"
        )

        self.setFixedSize(
            560,
            420
        )

        self.setWindowFlag(
            Qt.FramelessWindowHint
        )

        self.setStyleSheet("""

        QWidget{

            background:#202124;
            color:white;

        }

        QLabel{

            color:white;

        }

        QProgressBar{

            border:1px solid #505050;

            border-radius:12px;

            text-align:center;

            height:24px;

            font-size:13px;

            background:#2B2B2B;

        }

        QProgressBar::chunk{

            background:#00C853;

            border-radius:12px;

        }

        """)

        layout = QVBoxLayout()

        layout.setSpacing(20)

        layout.setAlignment(
            Qt.AlignCenter
        )

        logo = QLabel("📝")

        logo.setAlignment(Qt.AlignCenter)

        logo.setStyleSheet("""

        font-size:72px;

        """)

        title = QLabel(
            "Ultra Smart Notes"
        )

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

        font-size:30px;
        font-weight:bold;

        """)

        version = QLabel(
            "Version 5 Official"
        )

        version.setAlignment(Qt.AlignCenter)

        version.setStyleSheet("""

        font-size:16px;
        color:#A0A0A0;

        """)

        developer = QLabel(

            "Developed by\nSyahir Asyam"

        )

        developer.setAlignment(Qt.AlignCenter)

        developer.setStyleSheet("""

        font-size:14px;
        color:#C0C0C0;

        """)

        build = QLabel(

            "Build 2026.06"

        )

        build.setAlignment(Qt.AlignCenter)

        build.setStyleSheet("""

        font-size:11px;
        color:#808080;

        """)

        version.setStyleSheet(
            "font-size:16px;"
        )

        self.status = QLabel(
            "Initializing..."
        )

        self.progress = QProgressBar()

        self.progress.setValue(0)
        self.percent = QLabel("0%")

        self.percent.setAlignment(Qt.AlignCenter)

        self.percent.setStyleSheet("""

        font-size:14px;
        color:#B0B0B0;

        """)

        layout.addWidget(logo)

        layout.addWidget(title)

        layout.addWidget(version)

        layout.addSpacing(5)

        layout.addWidget(developer)

        layout.addWidget(build)

        layout.addSpacing(15)

        layout.addWidget(self.progress)

        layout.addWidget(self.percent)

        layout.addWidget(self.status)

        self.setLayout(layout)

        self.value = 0

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.loading
        )

        self.timer.start(35)

    def loading(self):

        self.value += 1

        self.progress.setValue(self.value)

        self.percent.setText(f"{self.value}%")

        if self.value < 15:

            self.status.setText("Loading Notes Engine...")

        elif self.value < 30:

            self.status.setText("Loading Theme Engine...")

        elif self.value < 50:

            self.status.setText("Loading Backup System...")

        elif self.value < 70:

            self.status.setText("Loading Recycle Bin...")

        elif self.value < 90:

            self.status.setText("Preparing Editor...")

        else:

            self.status.setText("Launching Ultra Smart Notes...")

        if self.value >= 100:

            self.timer.stop()

            self.close()

            self.close()

            self.main_window.show()