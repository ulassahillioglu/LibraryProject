# Library.py
from TerminalMenu import TerminalMenu
import sys

class Library:
    def __init__(self):
        self.file = open("books.txt", "a+", encoding="utf-8")
        self.file.seek(0)  # Kursörü dosyanın başına al
        self.book_list = self.file.read().splitlines()
        print("Welcome to the Library. What would you like to do?", end="\n\n")

    def add_book(self, title=None, author=None, release_year=None, num_pages=None):
        if title is None:
            title = input("Enter the book title: ")
        if author is None:
            author = input("Enter the book author: ")
        if release_year is None:
            release_year = input("Enter the first release year: ")
        if num_pages is None:
            num_pages = input("Enter the number of pages: ")

        book_info = f"{title},{author},{release_year},{num_pages}\n"
        self.file.write(book_info.upper())
        self.file.flush()  # Verileri dosyaya yazmak için arabelleği boşaltır
        self.book_list.append(book_info.upper())  # Kitap listesinin sonuna yeni kitabı ekler

    def list_books(self):
        books_info = ""
        for book in self.book_list:
            if book.strip():  # Boşlukları temizledikten sonra satırın boş olup olmadığını kontrol eder
                book_info = book.split(",")  # Kitap bilgilerini virgül olan yerlerden ayırır
                book_name = book_info[0]
                book_author = book_info[1]
                books_info += f"Book Title: {book_name}, Author: {book_author}\n"
        print(books_info)
        return books_info

    def remove_book(self, book=None):
        if book is None:
            book = input("Enter the book title to remove: ")

        books_list = self.book_list

        index = -1
        for i, b in enumerate(books_list):
            book_title = b.split(",")[0]
            if book_title.upper() == book.upper():
                index = i
                break

        if index != -1:
            books_list.pop(index)

            self.file.seek(0)
            self.file.truncate()

            for b in books_list:
                if b.strip():  
                    self.file.write(b + "\n")
            self.file.flush()
            print("Book removed successfully", "*********", sep="\n")
            return True
        else:
            print("Book not found", "*********", sep="\n")
            return False

    def start_terminal_menu(self):
        terminal_menu = TerminalMenu(self)
        terminal_menu.run()

    

    def start_gui_menu(self):
        from GUIMenu import AltGUIMenu
        from PyQt5.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        gui = AltGUIMenu(self)
        gui.show()
        app.exec_()
    
        
    def choice(self):
        print(
            "Please choose how to continue : ",
            "1) Terminal Menu",
            "2) GUI Menu",
        )
        menu_choice = input("Enter your choice: ")
        if menu_choice == "1":
            self.start_terminal_menu()
        elif menu_choice == "2":
            self.start_gui_menu()
        else:
            print("Invalid choice, please try again.", "*********", sep="\n")

    def __del__(self):
        self.file.close()
