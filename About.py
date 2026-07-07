from PyQt5.QtWidgets import QMessageBox


def show_about(notes_win):

    QMessageBox.information(

        notes_win,

        "About Ultra Smart Notes",

        """
Ultra Smart Notes V5

Developer:
Syahir Asyam

Features:
✅ Folder
✅ Recycle Bin
✅ Favorites
✅ Themes
✅ Backup
✅ Welcome Screen

Built with Python + PyQt5

© 2026

        """
    )