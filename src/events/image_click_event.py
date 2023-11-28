from interfaces.event import Event


class ImageClickEvent(CTk.CTkLabel, Event):
    def __init__(self, parent: CTk.CTkFrame, model: HoldDetector,  image: Image, width: int = None, height: int = None):
        """Constructor."""

        self.model = model
        self.image = image
        self.default_size_width, self.default_size_height = image.size # (width, height)
        image_processed = self.model.apply_model_on_image(image)

        if(width is None or height is None):
            width, height = self.default_size_width, self.default_size_height

        self.ctkimage = CTk.CTkImage(image_processed, size= (width, height))

        super().__init__(parent, text= "", image= self.ctkimage)
        Event.__init__(self)

        self.bind("<Button-1>", self.__click_left)
        self.bind("<Button-3>", self.__click_right)


    def change_image(self, image: Image):
        del self.ctkimage
        self.__load_image(image=image)

    
    def __load_image(self, image: Image):
        self.image = image
        self.default_size_width, self.default_size_height = image.size # (width, height)
        self.ctkimage = CTk.CTkImage(image, size= (self.winfo_width(), self.winfo_height()))
        self.configure(image= self.ctkimage)

    
    def refresh_image(self, path: list[Box]):
        """Refresh the image."""
        self.change_image(self.model.apply_model_on_image(self.image, path= path))


    def register(self, listener: Listener):
        """Register an listener. Override from CTkLabel."""
        Event.register(self, listener)

    
    def change_size(self, width: int, height: int):
        """Change the size of the image."""
        self.configure(width= width, height= height)
        self.__resize_image(width, height)

    
    def __resize_image(self, width: int, height: int):
        """Resize the image."""
        self.ctkimage.configure(size= (width, height))
        self.configure(image= self.ctkimage)


    def __click_right(self, event):
        """Called when the image is clicked."""
        self.__click(event, ClickType.RIGHT_CLICK)


    def __click_left(self, event):
        """Called when the image is clicked."""
        self.__click(event, ClickType.LEFT_CLICK)


    def __click(self, event, click_type: ClickType):
        """Called when the image is clicked."""
        print("click appended")
        default_X = int(self.default_size_width * event.x / self.winfo_width())
        default_Y = int(self.default_size_height * event.y / self.winfo_height())
        self.notify([ImageEventType.CLICK_EVENT], click_type, default_X, default_Y)