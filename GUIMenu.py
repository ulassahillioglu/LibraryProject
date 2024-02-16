import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from library import Library
from TerminalMenu import TerminalMenu
from PyQt5.QtCore import pyqtSignal,QRect
from PyQt5.QtWidgets import QHeaderView



class NonEditableTableWidget(QTableWidget):
    def mouseDoubleClickEvent(self, event):
        event.ignore()
        
class AltGUIMenu(QMainWindow):
    switch_to_terminal = pyqtSignal()
    def __init__(self, library):
        super().__init__()
        self.library = library
        self.initUI()
        self.window = QWidget()
        self.window_layout = QVBoxLayout()
        self.window.setLayout(self.window_layout)

    def initUI(self):
        self.setWindowTitle("Library Management System")

        list_button = QPushButton("List Books", self)
        list_button.clicked.connect(self.list_books)

        switch_button = QPushButton("Switch to Terminal", self)
        switch_button.clicked.connect(self.switch_to_terminal)

        self.title_entry = QLineEdit()
        title_label = QLabel("Title:")
        author_label = QLabel("Author:")
        release_year_label = QLabel("Release Year:")
        num_pages_label = QLabel("Number of Pages:")

        self.author_entry = QLineEdit()
        self.release_year_entry = QLineEdit()
        self.num_pages_entry = QLineEdit()

        add_button = QPushButton("Add Book", self)
        add_button.clicked.connect(self.add_book)

        remove_label = QLabel("Remove Book:")
        self.remove_entry = QLineEdit()
        remove_button = QPushButton("Remove", self)
        remove_button.clicked.connect(self.remove_book)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setGeometry(QRect(0, 0, 400, 300))
        layout.addWidget(list_button)
        layout.addWidget(switch_button)
        layout.addWidget(title_label)
        layout.addWidget(self.title_entry)
        layout.addWidget(author_label)
        layout.addWidget(self.author_entry)
        layout.addWidget(release_year_label)
        layout.addWidget(self.release_year_entry)
        layout.addWidget(num_pages_label)
        layout.addWidget(self.num_pages_entry)
        layout.addWidget(add_button)
        layout.addWidget(remove_label)
        layout.addWidget(self.remove_entry)
        layout.addWidget(remove_button)
        central_widget.setLayout(layout)

    def switch_to_terminal(self):
        self.close()

    def clear_entries(self):
        self.title_entry.clear()
        self.author_entry.clear()
        self.release_year_entry.clear()
        self.num_pages_entry.clear()
        self.remove_entry.clear()

    def add_book(self):
        book_title = self.title_entry.text()
        book_author = self.author_entry.text()
        release_year = self.release_year_entry.text()
        num_pages = self.num_pages_entry.text()

        if not book_title or not book_author or not release_year or not num_pages:
            QMessageBox.critical(self, "Missing Information", "Please fill all the fields")
            return
        
        
        self.library.add_book(book_title, book_author, release_year, num_pages)
        
        QMessageBox.information(self, "Book Added", "Book added successfully")
        self.clear_entries()

    def remove_book(self):
        book = self.remove_entry.text()
        if self.library.remove_book(book):
            QMessageBox.information(self, "Book Removed", "Book removed successfully")
        else:
            QMessageBox.critical(self, "Book Not Found", "Book not found")
        self.clear_entries()

    def list_books(self):
        
        books_info = self.library.book_list
        
        # Eğer pencere oluşturulmamışsa oluşturur, oluşturulmuşsa temizler
        if not self.window:
            self.window = QWidget()

        # Table widget oluşturur
        table = NonEditableTableWidget()
        table.setColumnCount(2)  # Sütun sayısını ayarlar

        # Tablo başlıklarını ayarlar
        headers = ["Title", "Author"]
        table.setHorizontalHeaderLabels(headers)

        # Arka plan rengini ayarlar ve başlık yazılarını kalın yapar
        header_style = "QHeaderView::section { background-color: gray; color: white; font-weight: bold; }"
        table.horizontalHeader().setStyleSheet(header_style)

        # Tablonun sütun genişliklerini ayarlar. İlk genişliği içeriğe göre ayarlar. İkinci sütunun genişliğini ise pencere genişliğine göre ayarlar
        # Pencere boyutu değiştiğinde sütun genişlikleri değişir
        table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        
        
        
        # Kitap bilgileri ile tabloyu doldurur
        table.setRowCount(len(books_info))
        for i, book in enumerate(books_info):
            if book.strip():
                book_info = book.split(",")
                title = book_info[0] + "    "
                author = book_info[1]
                table.setItem(i, 0, QTableWidgetItem(title))
                table.setItem(i, 1, QTableWidgetItem(author))
                
        # Son veriden başlayarak penceredeki tüm widgetları siler ve tabloyu ekler. 
        # Bu sayede her seferinde yeni bir tablo oluşturur ve güncellemeleri anlık olarak gösterir
        for i in reversed(range(self.window_layout.count())):
            widget = self.window_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Tabloyu layouta ekler
        self.window_layout.addWidget(table)

        # Pencereyi gösterir
        self.window.show()
        

    def start_gui_menu(self):
        app = QApplication(sys.argv)
        gui = AltGUIMenu()
        gui.show()
        app.exec_()

    def start_terminal_menu(self):
        terminal_menu = TerminalMenu(self.library)
        terminal_menu.run()
            
    
    
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        app = QApplication(sys.argv)
        gui = AltGUIMenu()
        gui.show()
        sys.exit(app.exec_())
    else:
        terminal_menu = TerminalMenu(Library())
        terminal_menu.run()
    

# Assuming library object is defined somewhere before calling main()
