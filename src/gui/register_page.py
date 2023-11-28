""""Module for tkinter interface of register page."""
import customtkinter
from gui.abstract.page import Page

from gui.utils import SECONDARY_COLOR, SECONDARY_HOVER_COLOR
from database import user_queries

class register_page(Page):
    """Class of the register page."""

    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
        super().__init__(parent, app)

        self.show_page = app.show_page
        #self.login_page = login_page

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.grid_rowconfigure((0,2,3,4,5,7), weight=1)
        self.grid_rowconfigure((1,6), weight=4)

        self.register_label = customtkinter.CTkLabel(self, text="Register", font=("Arial", 30))
        self.register_label.grid(row=0, column=0, columnspan=2, pady=(10,0))

        self.pseudo_label = customtkinter.CTkLabel(self, text="Username")
        self.pseudo_label.grid(row=2, column=1, sticky="sw", columnspan=2)
        self.pseudo_entry = customtkinter.CTkEntry(self, width=200)
        self.pseudo_entry.grid(row=3, column=1, sticky="nw", columnspan=2)
        self.pseudo_entry.bind("<Return>", lambda event: self.register())


        self.password_label = customtkinter.CTkLabel(self, text="Password")
        self.password_label.grid(row=4, column=1, sticky="sw", columnspan=2)
        self.password_entry = customtkinter.CTkEntry(self, show="*", width=200)
        self.password_entry.grid(row=5, column=1, sticky="nw", columnspan=2)
        self.password_entry.bind("<Return>", lambda event: self.register())


        self.register_button = customtkinter.CTkButton(self, text="Register", fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR, command=self.register)
        self.register_button.grid(row=7, column=0, columnspan=2)

        self.back_button = customtkinter.CTkButton(self, text="Back", fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR, command=self.cancel)
        self.back_button.grid(row=7, column=2, columnspan=2)

    def register(self):
        """Register the user."""
        pseudo = self.pseudo_entry.get()
        password = self.password_entry.get()
        print(password)

        if pseudo not in self.__get_all_usernames():
            user_queries.create_user(pseudo, password)
        else :
            #TODO: afficher un message disant que l'user existe déjà
            print("User already exists")
        print(f"User {pseudo} registered !")
        self.app.show_login_page()

    def cancel(self):
        """Cancel the registration."""
        from gui.login_page import login_page

        if self.app is not None:
            self.app.show_page(login_page)

    def __get_all_usernames(self):
        username_list = []
        for user in user_queries.get_all_users():
            username_list.append(user.username)
        return username_list