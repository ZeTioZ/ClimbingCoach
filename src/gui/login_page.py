"""Module for tkinter interface of the login page."""
import tkinter as tk
import customtkinter
from gui.page import page
from gui.register_page import register_page
import os.path
from PIL import Image
from database import user_queries
from gui.trail_page import trail_page


DEFAULT_FONT = ("Helvetica", 16)
TITLE_FONT = ("Helvetica", 24)
DF = DEFAULT_FONT
TF = TITLE_FONT

DEFAULT_FONT_BIG = ("Helvetica", 32)
DFB = DEFAULT_FONT_BIG

v = lambda x, view: x * (view/100)

class login_page(page):
    """Class for the login page."""

    RI_TITLE = 1
    RI_USERNAME_LABEL =2
    RI_USERNAME = 3
    RI_PASSWORD_LABEL = 4
    RI_PASSWORD = 5
    RI_LOGIN = 6

    CI_LEFT = 1
    CI_RIGHT = 2

    __sizeState = None

    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
        """Constructor. Singleton then init executed only once."""
        super().__init__(parent)  # Call the __init__ method of the parent class
        app_path = os.path.dirname(os.path.abspath(__file__))
        app_path = app_path[:app_path.rfind("src")] # was \\src --> check if it works on windows

        if app is not None: 
            app.title("Login Page")
            self.toggle_menu = app.toggle_menu
            self.show_page = app.show_page
            latest_width = app.winfo_width()
            latest_height = app.winfo_height()
        else: 
            self.toggle_menu = lambda: print("Toggle menu")
        
        #Frame configure
        parent.grid_rowconfigure(0, weight=1) 
        parent.grid_columnconfigure(0, weight=1) # Use to align the frame in the center of the window

        self.grid_rowconfigure((self.RI_TITLE, self.RI_LOGIN), weight=2, minsize=100)
        self.grid_rowconfigure((self.RI_USERNAME,self.RI_PASSWORD), weight=1)
        self.grid_rowconfigure((self.RI_USERNAME_LABEL, self.RI_PASSWORD_LABEL), weight=0)
        self.grid_rowconfigure((0,7), weight=6)

        self.grid_columnconfigure((self.CI_LEFT,self.CI_RIGHT), weight=1)
        self.grid_columnconfigure((0,3), weight=4)

        #Title
        self.app_image = customtkinter.CTkImage(Image.open(os.path.join(app_path, "resources", "images", "incroyable_logo_climbing_coach.png")), size=(100,100))
        self.title = customtkinter.CTkLabel(self, text="", font=TF, image=self.app_image)
        self.title.bind("<Enter>", lambda e: self.title.configure(text="Logo", image=customtkinter.CTkImage(Image.frombytes("RGBA", (1,1), b"\x00\x00\x00\x00"))))
        self.title.bind("<Leave>", lambda e: self.title.configure(text="", image=self.app_image))
        self.title.grid(row = self.RI_TITLE, column = self.CI_LEFT, columnspan=2)
        
        #Username
        self.username_label = customtkinter.CTkLabel(self, text="Username", font=DF)
        self.username_combobox = customtkinter.CTkComboBox(self, values=self.__get_all_usernames(), font=DF, dropdown_font=DF) #Faire appel a la fonction qui permet de choper tous les users
        self.username_combobox.set("")
        self.username_label.grid(row = self.RI_USERNAME_LABEL, column = self.CI_LEFT, sticky="sw", columnspan=2)       
        self.username_combobox.grid(row = self.RI_USERNAME, column = self.CI_LEFT, sticky="nwe", columnspan=2)
        
        #Password
        self.password_label = customtkinter.CTkLabel(self, text="Password", font=DF)
        self.password_entry = customtkinter.CTkEntry(self, show="*")
        self.password_label.grid(row = self.RI_PASSWORD_LABEL, column = self.CI_LEFT, sticky="sw", columnspan=2)
        self.password_entry.grid(row = self.RI_PASSWORD, column = self.CI_LEFT, sticky="nwe", columnspan=2)
        
        #Login button
        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login, font=DF)
        self.login_button.grid(row = self.RI_LOGIN, column = self.CI_LEFT, columnspan=2)

        self.guest_button = customtkinter.CTkButton(self, text="Guest", font=DF, fg_color="#027148", hover_color="#013220")
        self.guest_button.grid(row = self.RI_LOGIN, column = self.CI_LEFT, columnspan=2)

        self.register_button = customtkinter.CTkButton(self, text="Register", command=lambda:self.show_page(register_page), font=DF)
        self.register_button.grid(row = self.RI_LOGIN, column = self.CI_RIGHT, columnspan=2)


    def login(self):
        username = self.username_combobox.get()
        password = self.password_entry.get()
        self.__get_usernames(username)
        success, user = user_queries.user_can_connect(username, password)
        print(user_queries.user_can_connect(username, password))
        if success:
            self.toggle_menu()
            self.show_page(trail_page)
        # Add your login logic here
        print(f"You'r logged in as {username}")

    def __get_usernames(self, username: str):
        self.user = user_queries.get_user_by_name(username)
        return self.user

    def __get_all_usernames(self):
        username_list = []
        for user in user_queries.get_all_users():
            username_list.append(user.username)
        return username_list

    def __setup_smallScreen(self):
        """Setup the container for small screen."""
        self.grid_rowconfigure((0,7), weight=6)

        self.login_button.grid(row = self.RI_LOGIN, column = self.CI_LEFT, columnspan=1, sticky="nw", pady=(10, 4))
        self.register_button.grid(row = self.RI_LOGIN, column = self.CI_RIGHT, columnspan=1, sticky="ne", pady=(10, 4))
        self.guest_button.grid(row = self.RI_LOGIN, column = self.CI_LEFT, columnspan=2, sticky="swe")
    
    def __setup_bigScreen(self):
        """Setup the container for big screen."""
        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((7), weight=1)

        self.login_button.grid(row = self.RI_LOGIN, column = self.CI_LEFT, columnspan=1, sticky="nw", pady=0)
        self.guest_button.grid(row = self.RI_LOGIN, column = self.CI_RIGHT, columnspan=1, sticky="ne")
        self.register_button.grid(row = self.RI_LOGIN, column = self.CI_LEFT, columnspan=1, sticky="w", pady=0)

    def onSizeChange(self, width, height):
        """Called when the windows size change."""

        # Change grid structure
        if width > 800 and height > 600 and self.__sizeState != "big":
            self.__sizeState = "big"
            self.__setup_bigScreen()
        elif width and height <= 600 and self.__sizeState != "small":
            self.__sizeState = "small"
            self.__setup_smallScreen()

        default_font = ("Helvetica", min(int(v(4, height)), 24))
        title_font = ("Helvetica", min(int(v(6, height)), 32))

        self.app_image.configure(size=(
            max(100, min(int(v(10, width)), 200)), 
            max(100, min(int(v(10, width)), 200))
        ))

        self.title.configure(
            width=max(100, min(int(v(10, width)), 200)),
            height=max(100, min(int(v(10, width)), 200))
        )

        self.username_label.configure(font=default_font)
        self.password_label.configure(font=default_font)
        self.login_button.configure(
            font=default_font,
            width=v(20, width)
        )
        self.register_button.configure(
            font=default_font,
            width=v(20, width)
        )
        self.guest_button.configure(
            font=default_font,
            width=v(20, width)
        )

        self.title.configure(font=title_font)

        self.password_entry.configure(font=default_font)
        self.username_combobox.configure(font=default_font, dropdown_font=default_font)
    
