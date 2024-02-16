# TerminalMenu.py

class TerminalMenu:
    def __init__(self, library):
        self.library = library

    def run(self):
        print("*** MENU ***")
        while True:
            menu_choice = input(
                "1) List Books\n"
                "2) Add Book\n"
                "3) Remove Book\n"
                "4) Exit\n"
                "5) Switch to GUI\n"
                "Enter your choice: "
            )
            if menu_choice == "1":
                self.library.list_books()
                print("*********")
            elif menu_choice == "2":
                self.library.add_book()
                print("Book added successfully", "*********", sep="\n")
            elif menu_choice == "3":
                self.library.remove_book()
            elif menu_choice == "4":
                print("Have a nice day!")
                exit()
            elif menu_choice == "5":
                self.library.start_gui_menu()              
            else:
                print("Invalid choice, please try again.", "*********", sep="\n")
