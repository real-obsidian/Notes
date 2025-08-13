from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QInputDialog, \
    QListWidget, \
    QMenuBar, QMenu, QAction, QHBoxLayout, QSplitter, QTabWidget
from PyQt5.QtCore import Qt
import sys


class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        self.setGeometry(20, 40, 1200, 600)
        self.setStyleSheet("""
                    QWidget {
                        color: black;
                        background-color: #000000;
                        font-family: Arial;
                        font-size: 14px;
                    }
                    QPushButton {
                        background-color: #0fd1c1;
                        color: #000000;
                        border: 2px solid #3e7502;
                        padding: 10px 20px;
                        text-align: center;
                        font-size: 16px;
                        margin: 4px 2px;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #3dfced;
                        border: 1px solid #3e7502;
                    }
                    QPushButton:pressed{
                        background-color: #3b8781;
                        border: 2px solid #3e7502;
                    }
                    QTextEdit, QListWidget {
                        color: white;
                        border: 1px solid #0fd1c1;
                        padding: 5px;
                        border-radius: 10px;
                    }
                """)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Tabs
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        # Menu bar
        menu_bar = self.menuBar()
        file = menu_bar.addMenu("File")
        new_action = QAction("Open", self)
        new_action.triggered.connect(self.setFileName)
        file.addAction(new_action)

        # Main splitter for text_edit and list_widget
        splitter = QSplitter(Qt.Horizontal)
        self.text_edit = QTextEdit(self)
        splitter.addWidget(self.text_edit)
        splitter.setSizes([300, 1066])  # Set initial sizes for the panes

        self.main_layout.addWidget(splitter)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.add_note = QPushButton("Add Note")
        buttons_layout.addWidget(self.add_note)

        self.new_tab_button = QPushButton("New Tab")
        buttons_layout.addWidget(self.new_tab_button)

        self.save_button = QPushButton("Save Note")
        buttons_layout.addWidget(self.save_button)

        self.delete_button = QPushButton("Delete")
        buttons_layout.addWidget(self.delete_button)


        self.main_layout.addLayout(buttons_layout)

        # Signals and Slots
        self.add_note.clicked.connect(self.setFileName)
        self.save_button.clicked.connect(self.update_data)
        self.delete_button.clicked.connect(self.deleteItem)

        # Connect the new tab button to the new method
        self.new_tab_button.clicked.connect(self.prompt_for_new_tab)

    def prompt_for_new_tab(self):
        tab_name, ok = QInputDialog.getText(self, "New Tab", "Enter new tab name:")
        if ok and tab_name:
            self.add_new_tab(tab_name)

    def add_new_tab(self, tab_name):
        # Create a new widget to hold the QListWidget
        tab_content_widget = QWidget()
        tab_layout = QHBoxLayout(tab_content_widget)

        # Create a QListWidget for the new tab
        list_widget = QListWidget()
        tab_layout.addWidget(list_widget)

        # Add the new tab content to the QTabWidget
        self.tab_widget.addTab(tab_content_widget, tab_name)

        # Set this new QListWidget as the one to be used by other functions
        self.list_widget = list_widget

        # Connect the itemClicked signal for the newly created QListWidget
        self.list_widget.itemClicked.connect(self.displaySelectedNote)

    def setFileName(self):
        text, okPressed = QInputDialog.getText(self, "Add Item", "Enter File Name, Nigga:")
        if okPressed and text:
            self.list_widget.addItem(text)

    def displaySelectedNote(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            note_content = selected_item.data(Qt.UserRole)
            self.text_edit.setText(note_content)

    def update_data(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            new_text = self.text_edit.toPlainText()
            selected_item.setData(Qt.UserRole, new_text)

    def deleteItem(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            row = self.list_widget.row(selected_item)
            self.list_widget.takeItem(row)
        else:
            print("No item selected to delete.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec_())