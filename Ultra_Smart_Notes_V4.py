
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys
import os
import ctypes
import json


# ================= APP ID WINDOWS =================
myappid = "smart.notes.ultra.v4"

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    myappid
)


# ================= APP =================
app = QApplication(sys.argv)


# ================= ICON PATH =================
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ICON_PATH = os.path.join(
    BASE_DIR,
    "smart_notes.ico"
)


# ================= WINDOW =================
notes_win = QWidget()

notes_win.setWindowTitle(
    "Smart Notes Ultra V4"
)

notes_win.resize(1500, 850)


# ================= SET ICON =================
icon = QIcon(ICON_PATH)

app.setWindowIcon(icon)

notes_win.setWindowIcon(icon)









# ================= FILE =================
FILE_NAME = "notes_data.json"
LOCK_FILE = "lock_data.json"

BACKUP_FOLDER = "backup"
BACKUP_FILE = "backup/notes_backup.json"



# ================= DATA =================
notes = {}
pinned_notes = []
recent_notes = []

recycle_bin = {}


note_colors = {}
favorite_notes = []

locked = False
note_password = ""

last_opened_note = ""
current_theme = "dark"

loading_note = False

unsaved_changes = False


# ================= WIDGETS =================
list_notes = QListWidget()
list_notes.setMinimumWidth(250)

search_bar = QLineEdit()
search_bar.setPlaceholderText("🔍 Find notes...")


btn_new = QPushButton("➕ New")
btn_delete = QPushButton("🗑 Delete")
btn_save = QPushButton("💾 Save")
btn_rename = QPushButton("✏ Rename")

btn_dark = QPushButton("🌙 Dark")
btn_light = QPushButton("☀ Light")

btn_pin = QPushButton("📌 Pin")
btn_color = QPushButton("🎨 Color")
btn_favorite = QPushButton("⭐ Favorite")

btn_blue = QPushButton("💙 Blue")
btn_red = QPushButton("❤️ Red")
btn_hacker = QPushButton("💻 Hacker")

btn_copy = QPushButton("📋 Copy")
btn_paste = QPushButton("📥 Paste")

btn_bold = QPushButton("𝐁 Bold")
btn_italic = QPushButton("𝘐 Italic")
btn_underline = QPushButton("U̲ Underline")

btn_todo = QPushButton("✅ Todo")
btn_check = QPushButton("☑ Check")
btn_uncheck = QPushButton("🔲 Uncheck")

btn_lock = QPushButton("🔒 Lock")
btn_date = QPushButton("📅 Date")

btn_clear = QPushButton("🧹 Clear")

btn_export = QPushButton("📄 Export TXT")

btn_restore = QPushButton(
    "♻ Restore"
)




# ================= STATUS =================
font_size = QSpinBox()
font_size.setRange(8, 40)
font_size.setValue(14)

word_count = QLabel("Words: 0")
status_label = QLabel("✅ Ready")


# ================= TABS =================
tabs = QTabWidget()

editors = []

for i in range(1, 5):

    editor = QTextEdit()

    editor.setFont(
        QFont(
            "Consolas",
            14
        )
    )

    editor.setPlaceholderText(
        f"Tulis sesuatu di Tab {i}..."
    )

    tabs.addTab(
        editor,
        f"Tab {i}"
    )

    editors.append(editor)


# ================= LEFT LAYOUT =================
left_layout = QVBoxLayout()

left_layout.addWidget(
    QLabel("📚 List Notes")
)

left_layout.addWidget(search_bar)
left_layout.addWidget(list_notes)

left_layout.addWidget(btn_new)
feature_layout_2 = QHBoxLayout()

feature_layout_2.addWidget(btn_rename)
feature_layout_2.addWidget(btn_delete)
feature_layout_2.addWidget(btn_save)

left_layout.addLayout(
    feature_layout_2
)

feature_layout_1 = QHBoxLayout()

feature_layout_1.addWidget(btn_pin)
feature_layout_1.addWidget(btn_color)
feature_layout_1.addWidget(btn_favorite)

left_layout.addLayout(
    feature_layout_1
)

todo_layout = QHBoxLayout()

todo_layout.addWidget(btn_todo)
todo_layout.addWidget(btn_check)
todo_layout.addWidget(btn_uncheck)

left_layout.addLayout(todo_layout)

left_layout.addWidget(btn_lock)
left_layout.addWidget(btn_date)

left_layout.addWidget(btn_clear)
left_layout.addWidget(btn_export)
left_layout.addWidget(btn_restore)


theme_layout = QHBoxLayout()

theme_layout.addWidget(btn_blue)
theme_layout.addWidget(btn_red)
theme_layout.addWidget(btn_hacker)

left_layout.addLayout(theme_layout)


# ================= RIGHT LAYOUT =================
right_layout = QVBoxLayout()

toolbar = QHBoxLayout()

toolbar.addWidget(QLabel("Font Size:"))
toolbar.addWidget(font_size)

toolbar.addWidget(btn_dark)
toolbar.addWidget(btn_light)

toolbar.addWidget(btn_copy)
toolbar.addWidget(btn_paste)

toolbar.addWidget(btn_bold)
toolbar.addWidget(btn_italic)
toolbar.addWidget(btn_underline)

toolbar.addStretch()

toolbar.addWidget(word_count)
toolbar.addWidget(status_label)

right_layout.addLayout(toolbar)
right_layout.addWidget(tabs)


# ================= MAIN LAYOUT =================
main_layout = QHBoxLayout()

main_layout.addLayout(left_layout, 25)
main_layout.addLayout(right_layout, 75)

notes_win.setLayout(main_layout)


# ================= FUNCTIONS =================
def get_real_note_name(name):


    prefixes = [
        "⭐ ",
        "📌 ",
        "🕒 "
    ]

    changed = True

    while changed:

        changed = False

        for prefix in prefixes:

            if name.startswith(prefix):

                name = name.replace(
                    prefix,
                    "",
                    1
                )

                changed = True

    return name




def refresh_notes_list():


    current_note = None

    selected = list_notes.currentItem()

    if selected:
        current_note = get_real_note_name(
            selected.text()
        )

    list_notes.blockSignals(True)

    list_notes.clear()

    # PINNED
    for note in pinned_notes:

        if note not in notes:
            continue

        display_name = "📌 " + note

        if note in favorite_notes:
            display_name = "⭐ " + display_name

        item = QListWidgetItem(display_name)

        if note in note_colors:
            item.setForeground(
                QColor(note_colors[note])
            )

        list_notes.addItem(item)

    # RECENT
    for note in recent_notes:

        if note not in notes:
            continue

        if note in pinned_notes:
            continue

        display_name = "🕒 " + note

        if note in favorite_notes:
            display_name = "⭐ " + display_name

        item = QListWidgetItem(display_name)

        if note in note_colors:
            item.setForeground(
                QColor(note_colors[note])
            )

        list_notes.addItem(item)

    # NORMAL
    for note in notes:

        if note in pinned_notes:
            continue

        if note in recent_notes:
            continue

        display_name = note

        if note in favorite_notes:
            display_name = "⭐ " + display_name

        item = QListWidgetItem(display_name)

        if note in note_colors:
            item.setForeground(
                QColor(note_colors[note])
            )

        list_notes.addItem(item)

    list_notes.blockSignals(False)

    if current_note:

        for i in range(list_notes.count()):

            item = list_notes.item(i)

            if current_note in item.text():

                list_notes.setCurrentItem(item)

                break










def create_backup():

    if not os.path.exists(
        BACKUP_FOLDER
    ):

        os.makedirs(
            BACKUP_FOLDER
        )

    data = {

    "notes": notes,
    "pinned": pinned_notes,
    "recent": recent_notes,
    "favorites": favorite_notes,
    "colors": note_colors,
    "recycle_bin": recycle_bin,
    "last_opened": last_opened_note,
    "theme": current_theme

}

    with open(
        BACKUP_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def save_data():

    data = {

        "notes": notes,
        "pinned": pinned_notes,
        "last_opened": last_opened_note,
        "theme": current_theme

    }

    with open(
        FILE_NAME,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

    lock_data = {

        "locked": locked,
        "password": note_password

    }

    with open(
        LOCK_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            lock_data,
            file,
            ensure_ascii=False,
            indent=4
        )

        
        create_backup()




def load_data():

    global notes
    global pinned_notes
    global recycle_bin
    global recent_notes
    global favorite_notes
    global note_colors
    global locked
    global note_password
    global last_opened_note
    global current_theme

    # ================= NOTES DATA =================
    if os.path.exists(FILE_NAME):

        try:

            with open(
                FILE_NAME,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                notes = data.get(
                    "notes",
                    {}
                )

                pinned_notes = data.get(
                    "pinned",
                    []
                )

                recycle_bin = data.get(
                    "recycle_bin",
                    {}
                )

                recent_notes = data.get(
                    "recent",
                    []
                )

                favorite_notes = data.get(
                    "favorites",
                    []
                )

                note_colors = data.get(
                    "colors",
                    {}
                )

                last_opened_note = data.get(
                    "last_opened",
                    ""
                )

                current_theme = data.get(
                    "theme",
                    "dark"
                )

        
        except Exception as e:

            print("ERROR JSON:", e)

            notes = {}
            pinned_notes = []
            last_opened_note = ""
            current_theme = "dark"

            save_data()



    # ================= LOCK DATA =================
    if os.path.exists(LOCK_FILE):

        try:

            with open(
                LOCK_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                lock_data = json.load(file)

                locked = lock_data.get(
                    "locked",
                    False
                )

                note_password = lock_data.get(
                    "password",
                    ""
                )

        except:

            print("ERROR: lock_data.json rusak!")

            locked = False
            note_password = ""




# ================= NOTE =================
def add_note():

    note_name, ok = QInputDialog.getText(
        notes_win,
        "New Note",
        "Masukkan nama note:"
    )

    if ok and note_name.strip() != "":

        note_name = note_name.strip()

        if note_name not in notes:

            notes[note_name] = [
                "",
                "",
                "",
                ""
            ]

            print("NOTES SEKARANG:", notes)

            refresh_notes_list()

            update_word_count()

            save_data()

            status_label.setText(
                "➕ New Note Added"
            )



def delete_note():

    selected = list_notes.currentItem()

    if not selected:

        QMessageBox.warning(
            notes_win,
            "Error",
            "⚠ Pilih note dulu!"
        )

        return

    note_name = get_real_note_name(
        selected.text()
    )

    confirm = QMessageBox.question(
        notes_win,
        "Delete Note",
        f"Yakin mau hapus '{note_name}' ?",
        QMessageBox.Yes | QMessageBox.No
    )

    if confirm != QMessageBox.Yes:
        return

    # HAPUS NOTE
    if note_name in notes:

        recycle_bin[note_name] = notes[note_name]

    del notes[note_name]

    # HAPUS PIN
    if note_name in pinned_notes:
        pinned_notes.remove(note_name)

    # CLEAR EDITOR
    for editor in editors:

        editor.blockSignals(True)

        editor.clear()

        editor.blockSignals(False)

    # HAPUS SELECTION
    list_notes.clearSelection()

    refresh_notes_list()

    update_word_count()

    save_data()

    status_label.setText(
        "🗑 Note Deleted"
    )


def restore_note():

    if not recycle_bin:

        QMessageBox.information(
            notes_win,
            "Restore",
            "Trash kosong."
        )

        return

    note_name, ok = QInputDialog.getItem(
        notes_win,
        "Restore Note",
        "Pilih note:",
        list(recycle_bin.keys()),
        0,
        False
    )

    if ok:

        notes[note_name] = recycle_bin.pop(
            note_name
        )

        refresh_notes_list()

        save_data()

        status_label.setText(
            "♻ Note Restored"
        )



def rename_note():

    selected = list_notes.currentItem()

    if not selected:
        return

    old_name = get_real_note_name(
        selected.text()
    )

    new_name, ok = QInputDialog.getText(
        notes_win,
        "Rename",
        "Nama baru:"
    )

    if ok and new_name.strip() != "":

        new_name = new_name.strip()

        notes[new_name] = notes.pop(old_name)

        refresh_notes_list()

        save_data()


def pin_note():

    selected = list_notes.currentItem()

    if not selected:
        return

    note_name = get_real_note_name(
        selected.text()
    )

    if note_name in pinned_notes:

        pinned_notes.remove(note_name)

    else:

        pinned_notes.append(note_name)

    refresh_notes_list()

    save_data()


def color_note():

    selected = list_notes.currentItem()

    if not selected:
        return

    note_name = get_real_note_name(
        selected.text()
    )

    color = QColorDialog.getColor()

    if color.isValid():

        note_colors[note_name] = color.name()

        refresh_notes_list()

        save_data()


def favorite_note():

    selected = list_notes.currentItem()

    if not selected:
        return

    note_name = get_real_note_name(
        selected.text()
    )

    note_name = note_name.replace(
        "⭐ ",
        ""
    )

    if note_name in favorite_notes:

        favorite_notes.remove(
            note_name
        )

    else:

        favorite_notes.append(
            note_name
        )

    refresh_notes_list()

    save_data()


def show_note():

    global loading_note
    global last_opened_note

    selected = list_notes.currentItem()

    if not selected:
        return

    note_name = get_real_note_name(
        selected.text()
    )

    if note_name not in notes:
        return

    loading_note = True

    data = notes[note_name]

    for i in range(4):

        editors[i].setHtml(data[i])

        editors[i].setReadOnly(
            locked
        )

    loading_note = False

    last_opened_note = note_name

    if note_name in recent_notes:
        recent_notes.remove(note_name)

        recent_notes.insert(0, note_name)

    if len(recent_notes) > 10:
        recent_notes.pop()

    save_data()

    update_word_count()


def save_note():

    selected = list_notes.currentItem()

    if not selected:
        return

    note_name = get_real_note_name(
        selected.text()
    )

    notes[note_name] = [

        editor.toHtml()

        for editor in editors
    ]

    save_data()

    status_label.setText(
        "✅ Saved"
    )


def auto_save():

    global loading_note

    if loading_note:
        return

    selected = list_notes.currentItem()

    if not selected:
        return

    note_name = get_real_note_name(
        selected.text()
    )

    notes[note_name] = [

        editor.toHtml()

        for editor in editors
    ]

    save_data()

    global unsaved_changes

unsaved_changes = False

time_now = QTime.currentTime().toString(
    "HH:mm:ss"
)

status_label.setText(
    f"💾 Auto Saved ({time_now})"
)

notes_win.setWindowTitle(
    "Smart Notes Ultra V4"
)


# ================= UTIL =================
def copy_current_tab():

    current_editor = tabs.currentWidget()

    text = current_editor.toPlainText()

    QApplication.clipboard().setText(text)

    status_label.setText(
        "📋 Copied"
    )


def paste_to_current_tab():

    current_editor = tabs.currentWidget()

    clipboard_text = QApplication.clipboard().text()

    current_editor.insertPlainText(
        clipboard_text
    )

    status_label.setText(
        "📥 Pasted"
    )


def update_word_count():

    total = 0

    for editor in editors:

        total += len(
            editor.toPlainText().split()
        )

    word_count.setText(
        f"Words: {total} | Notes: {len(notes)}"
    )

def search_notes():

    text = search_bar.text().lower()

    for i in range(list_notes.count()):

        item = list_notes.item(i)

        item.setHidden(
            text not in item.text().lower()
        )


def change_font_size():

    size = font_size.value()

    for editor in editors:

        editor.setFont(
            QFont(
                "Consolas",
                size
            )
        )


def clear_current_tab():

    current_editor = tabs.currentWidget()

    current_editor.clear()


# ================= THEMES =================
def set_dark_mode():

    global current_theme

    current_theme = "dark"

    notes_win.setStyleSheet("""

        QWidget {
            background-color: #1e1e1e;
            color: white;
            font-size: 14px;
        }

        QPushButton {
            background-color: #3a3a3a;
            color: white;
            border-radius: 10px;
            padding: 8px;
        }

        QTextEdit {
            background-color: #2a2a2a;
            color: white;
        }

    """)

    save_data()


def set_light_mode():

    global current_theme

    current_theme = "light"

    notes_win.setStyleSheet("""

        QWidget {
            background-color: white;
            color: black;
        }

    """)

    save_data()


def blue_theme():

    global current_theme

    current_theme = "blue"

    notes_win.setStyleSheet("""

        QWidget {
            background-color: #cfe8ff;
            color: black;
        }

    """)

    save_data()


def red_theme():

    global current_theme

    current_theme = "red"

    notes_win.setStyleSheet("""

        QWidget {
            background-color: #ffd6d6;
            color: black;
        }

    """)

    save_data()


def hacker_theme():

    global current_theme

    current_theme = "hacker"

    notes_win.setStyleSheet("""

        QWidget {
            background-color: black;
            color: #00ff00;
            font-family: Consolas;
        }

    """)

    save_data()


# ================= TEXT STYLE =================
def make_bold():

    tabs.currentWidget().setFontWeight(
        QFont.Bold
    )


def make_italic():

    tabs.currentWidget().setFontItalic(True)


def make_underline():

    tabs.currentWidget().setFontUnderline(True)


# ================= TODO =================
def add_todo():

    current_editor = tabs.currentWidget()

    text, ok = QInputDialog.getText(
        notes_win,
        "Todo",
        "Isi checklist:"
    )

    if ok and text:

        current_editor.append(
            f"☐ {text}"
        )


def check_todo():

    current_editor = tabs.currentWidget()

    cursor = current_editor.textCursor()

    selected_text = cursor.selectedText()

    cursor.insertText(
        selected_text.replace(
            "☐",
            "☑"
        )
    )


def uncheck_todo():

    current_editor = tabs.currentWidget()

    cursor = current_editor.textCursor()

    selected_text = cursor.selectedText()

    cursor.insertText(
        selected_text.replace(
            "☑",
            "☐"
        )
    )


# ================= LOCK =================
def lock_note():

    global locked
    global note_password

    if not locked:

        password, ok = QInputDialog.getText(
            notes_win,
            "Set Password",
            "Buat password:",
            QLineEdit.Password
        )

        if ok and password != "":

            note_password = password

            locked = True

            for editor in editors:
                editor.setReadOnly(True)

            btn_lock.setText(
                "🔓 Unlock"
            )

    else:

        password, ok = QInputDialog.getText(
            notes_win,
            "Unlock",
            "Masukkan password:",
            QLineEdit.Password
        )

        if ok and password == note_password:

            locked = False

            for editor in editors:
                editor.setReadOnly(False)

            btn_lock.setText(
                "🔒 Lock"
            )

    save_data()


# ================= DATE =================
def insert_date():

    current_editor = tabs.currentWidget()

    date = QDate.currentDate().toString()

    current_editor.append(
        f"\n📅 {date}\n"
    )

def export_txt():

    selected = list_notes.currentItem()

    if not selected:

        QMessageBox.warning(
            notes_win,
            "Error",
            "⚠ Pilih note dulu!"
        )

        return

    note_name = get_real_note_name(
        selected.text()
    )

    content = ""

    for i, editor in enumerate(editors):

        content += f"===== TAB {i+1} =====\n\n"

        content += editor.toPlainText()

        content += "\n\n"

    file_name, _ = QFileDialog.getSaveFileName(
        notes_win,
        "Export TXT",
        f"{note_name}.txt",
        "Text Files (*.txt)"
    )

    if file_name:

        with open(
            file_name,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        status_label.setText(
            "📄 Exported TXT"
        )



# ================= AUTO SAVE TIMER =================
auto_save_timer = QTimer()

auto_save_timer.setSingleShot(True)

auto_save_timer.timeout.connect(
    auto_save
)


def start_auto_save_timer():

    global unsaved_changes

    unsaved_changes = True

    status_label.setText(
        "✏ Editing..."
    )

    notes_win.setWindowTitle(
        "Smart Notes Ultra V4 *"
    )

    auto_save_timer.start(3000)


# ================= CONNECTIONS =================
btn_copy.clicked.connect(copy_current_tab)
btn_paste.clicked.connect(paste_to_current_tab)

btn_new.clicked.connect(add_note)
btn_delete.clicked.connect(delete_note)
btn_restore.clicked.connect(
    restore_note
)
btn_save.clicked.connect(save_note)
btn_rename.clicked.connect(rename_note)

btn_pin.clicked.connect(pin_note)
btn_color.clicked.connect(
    color_note
)
btn_favorite.clicked.connect(
    favorite_note
)

btn_dark.clicked.connect(set_dark_mode)
btn_light.clicked.connect(set_light_mode)

btn_blue.clicked.connect(blue_theme)
btn_red.clicked.connect(red_theme)
btn_hacker.clicked.connect(hacker_theme)

btn_bold.clicked.connect(make_bold)
btn_italic.clicked.connect(make_italic)
btn_underline.clicked.connect(make_underline)

btn_todo.clicked.connect(add_todo)
btn_check.clicked.connect(check_todo)
btn_uncheck.clicked.connect(uncheck_todo)

btn_lock.clicked.connect(lock_note)

btn_date.clicked.connect(insert_date)

btn_clear.clicked.connect(clear_current_tab)

btn_export.clicked.connect(
    export_txt
)

btn_restore.clicked.connect(
    restore_note
)


list_notes.itemSelectionChanged.connect(show_note)

search_bar.textChanged.connect(
    search_notes
)

font_size.valueChanged.connect(
    change_font_size
)

for editor in editors:

    editor.textChanged.connect(
        update_word_count
    )

    
    editor.textChanged.connect(
    start_auto_save_timer
)



# ================= SHORTCUTS =================
QShortcut(
    QKeySequence("Ctrl+S"),
    notes_win,
    save_note
)

QShortcut(
    QKeySequence("Ctrl+E"),
    notes_win,
    export_txt
)

QShortcut(
    QKeySequence("Ctrl+N"),
    notes_win,
    add_note
)

QShortcut(
    QKeySequence("Ctrl+D"),
    notes_win,
    delete_note
)

QShortcut(
    QKeySequence("Ctrl+L"),
    notes_win,
    lock_note
)

QShortcut(
    QKeySequence("Ctrl+P"),
    notes_win,
    pin_note
)

QShortcut(
    QKeySequence("Ctrl+F"),
    notes_win,
    search_bar.setFocus
)

QShortcut(
    QKeySequence("Ctrl+B"),
    notes_win,
    make_bold
)

QShortcut(
    QKeySequence("Ctrl+I"),
    notes_win,
    make_italic
)

QShortcut(
    QKeySequence("Ctrl+U"),
    notes_win,
    make_underline
)

QShortcut(
    QKeySequence("Ctrl+Shift+C"),
    notes_win,
    copy_current_tab
)

QShortcut(
    QKeySequence("Ctrl+Shift+V"),
    notes_win,
    paste_to_current_tab
)

QShortcut(
    QKeySequence("Ctrl+T"),
    notes_win,
    add_todo
)

QShortcut(
    QKeySequence("Ctrl+Shift+T"),
    notes_win,
    check_todo
)

QShortcut(
    QKeySequence("Ctrl+Alt+T"),
    notes_win,
    uncheck_todo
)

QShortcut(
    QKeySequence("Ctrl+Tab"),
    notes_win,
    lambda: tabs.setCurrentIndex(
        (tabs.currentIndex() + 1)
        % tabs.count()
    )
)

QShortcut(
    QKeySequence("Ctrl+Shift+Tab"),
    notes_win,
    lambda: tabs.setCurrentIndex(
        (tabs.currentIndex() - 1)
        % tabs.count()
    )
)

QShortcut(
    QKeySequence("Ctrl+R"),
    notes_win,
    rename_note
)

QShortcut(
    QKeySequence("Ctrl+Shift+R"),
    notes_win,
    restore_note
)

QShortcut(
    QKeySequence("Ctrl+Shift+P"),
    notes_win,
    color_note
)

QShortcut(
    QKeySequence("Ctrl+Shift+F"),
    notes_win,
    favorite_note
)

QShortcut(
    QKeySequence("Ctrl+Shift+D"),
    notes_win,
    set_dark_mode
)

QShortcut(
    QKeySequence("Ctrl+Shift+L"),
    notes_win,
    set_light_mode
)

QShortcut(
    QKeySequence("Ctrl+Shift+B"),
    notes_win,
    blue_theme
)

QShortcut(
    QKeySequence("Ctrl+Shift+M"),
    notes_win,
    red_theme
)

QShortcut(
    QKeySequence("Ctrl+Shift+H"),
    notes_win,
    hacker_theme
)


def closeEvent(event):

    auto_save()

    event.accept()


# ================= START =================
load_data()

refresh_notes_list()

if len(notes) == 0:

    notes["Quick Notes"] = [
        "",
        "",
        "",
        ""
    ]

    save_data()

    refresh_notes_list()

if current_theme == "dark":
    set_dark_mode()

elif current_theme == "light":
    set_light_mode()

elif current_theme == "blue":
    blue_theme()

elif current_theme == "red":
    red_theme()

elif current_theme == "hacker":
    hacker_theme()


if last_opened_note in notes:

    for i in range(list_notes.count()):

        item = list_notes.item(i)

        if get_real_note_name(
            item.text()
        ) == last_opened_note:

            list_notes.setCurrentItem(item)

            show_note()

            break

notes_win.closeEvent = closeEvent


if list_notes.count() > 0:

    list_notes.setCurrentRow(0)

    show_note()


notes_win.show()






app.exec_()

