"""Module for tkinter interface of the login page."""
import tkinter as tk
import customtkinter
from gui.singleton_metaclass import singleton_page

class login_page(customtkinter.CTkFrame, singleton_page):
    """Class for the login page."""
    
    def __init__(self, parent):
        """Constructor. Singleton then init executed only once."""
        super().__init__(parent)  # Call the __init__ method of the parent class

        parent.title("Login Page")
        
        self.username_label = customtkinter.CTkLabel(self, text="Username:")
        self.username_combobox = customtkinter.CTkComboBox(self, values=["Admin", "User", "Guest"]) #Faire appel a la fonction qui permet de choper tous les users

        # For password purpose
        #self.password_label = customtkinter.CTkLabel(self, text="Password:")
        #self.password_entry = customtkinter.CTkEntry(self, show="*")

        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login)

        self.username_label.grid(row = 0, column = 1)
        self.username_combobox.grid(row = 1, column = 1)
        # self.password_label.grid(row = 0, column = 0)
        # self.password_entry.grid(row = 0, column = 0)
        self.login_button.grid(row = 2, column = 1)

        #frame.grid(row = 0, column = 0, sticky = "nsew")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Add your login logic here
    
    def get_frame(self):
        """Return the frame of the login page."""
        return self.__frame