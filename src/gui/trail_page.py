""""Module for tkinter interface of trail page."""
import tkinter as tk
import customtkinter
from gui.page import page
from PIL import Image
import os.path

from gui.utils import LIGHT_GREEN, DARK_GREEN, SECONDARY_COLOR, SECONDARY_HOVER_COLOR



class trail_page(page):
    """Class of the trail page."""
    
    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
        super().__init__(parent)

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=7)
        self.grid_rowconfigure(0, weight=1)

        self.trail_list_frame = customtkinter.CTkScrollableFrame(self)
        self.trail_list_frame.grid(row=0, column=0, sticky="nswe")
        self.trail_list_frame.grid_columnconfigure(0, weight=1)

        self.trail_detail_frame = customtkinter.CTkFrame(self)
        self.trail_detail_frame.grid(row=0, column=1, sticky="nswe")

        self.trail_detail_frame.grid_columnconfigure(0, weight=1)
        self.trail_detail_frame.grid_rowconfigure((0,1), weight=1)
        self.trail_detail_frame.grid_rowconfigure((2,3), weight=1)

        self.trail_image = customtkinter.CTkImage(Image.open(self.__get_trail_image_path("trail_1.jpg")), size=(200, 200))
        self.trail_label = customtkinter.CTkLabel(self.trail_detail_frame,text="", image=self.trail_image)
        self.trail_label.grid(row=1, column=0)

        self.choose_index = 0 #page dans laquelle on est
        self.selected_trail = None #page selectionnée
        self.trail_selection_button = customtkinter.CTkButton(self.trail_detail_frame,text="Select", command=lambda : self.selection_trail(self.choose_index))
        self.trail_selection_button.grid(row=2, column=0)

        #get all the trails in the db
        test_list= ["piste 1","piste 2","piste 3","piste 4","piste 5","piste 6"]
    
        self.button_list: list[customtkinter.CTkButton] = []
        for trail in test_list:
            self.trail_button = self.create_button(trail, test_list.index(trail))
            self.button_list.append(self.trail_button)
            
        
    def create_button(self, display_text, index):
        """Creates a button with the given text."""
        if index == 0:
            self.button = customtkinter.CTkButton(
                self.trail_list_frame,
                text=display_text,
                fg_color=SECONDARY_COLOR,
                hover_color=SECONDARY_HOVER_COLOR,
                border_spacing=17, 
                command=lambda : self.show_trail_detail(index)
            )
            self.button.grid(row=index, column=0, padx=10, sticky="nswe")
            return self.button
        
        else :
            self.button = customtkinter.CTkButton(
                self.trail_list_frame,
                text=display_text,
                fg_color="transparent",
                hover_color=SECONDARY_HOVER_COLOR,
                #corner_radius=0,
                border_spacing=17, 
                command=lambda trail_choosed=index: self.show_trail_detail(trail_choosed)
            )
            self.button.grid(row=index, column=0, padx=10, sticky="ew")
            return self.button
        

    def selection_trail(self,choose_index):
        """Select the trail."""
        button_text = self.trail_selection_button.cget("text")
        if button_text == "Select":
            self.trail_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
            self.selected_trail = self.choose_index
        else :
            self.trail_selection_button.configure(text="Select", fg_color="#0b7687", hover_color="#0b7687")
            self.selected_trail = 0

        #faire le back-end pour enregistrer le choix de l'utilisateur

    def show_trail_detail(self, trail_choosed):
        """Shows the trail detail page."""
        if not self.button_list or trail_choosed == self.choose_index:
            return
        
        for button in self.button_list:
            button.configure(fg_color="transparent")
        
        self.choose_index = trail_choosed
        if trail_choosed == self.selected_trail:
            self.trail_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
        else :
            self.trail_selection_button.configure(text="Select", fg_color="#0b7687", hover_color="#0b7687")

        self.button_list[trail_choosed].configure(fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR)
        
        #afficher a droite
        self.trail_label.grid_forget()
        #self.trail_label.configure(image=self.__image_loader("trail_" + str(trail_choosed+1)),size=(300, 300))
        self.__image_loader("trail_" + str(trail_choosed+1))
        self.trail_label.grid(row=1, column=0)

    def __image_loader(self, image_name: str):
        """Loads an image from the given path."""
        image = customtkinter.CTkImage(Image.open(self.__get_trail_image_path(image_name+".jpg")), size=(200, 200))
        self.trail_label.configure(image=image)
    
    def __get_trail_image_path(self, trail_image_name: str):
        """Return the path of the icon passed in parameter."""
        parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(parent_path, 'resources', 'images', trail_image_name)
        if os.path.exists(path):
            return path
        return os.path.join(parent_path, 'resources', 'images', "trail_1.jpg")
