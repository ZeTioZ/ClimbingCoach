import numpy as np
import PIL.Image as Image
import time
import customtkinter

from threading import Thread
from utils import draw_utils


class Playback(Thread):
    def __init__(self, image: np.ndarray, frame_rate: int, skeletons_list: list, label_img: customtkinter.CTkLabel, runtime: int = 0, video_progressbar ):
        self.__init__(self)
        self.daemon = True
        self.frame_rate = frame_rate
        self.skeletons_list = skeletons_list
        self.image = image
        self.label_img = label_img
        self.runtime = runtime
        self.video_progressbar = video_progressbar


    def start(self):

        for skeletons in self.skeletons_list:
            image_copy = self.image.copy()

            for skeleton in skeletons:
                #take the skeleton and start at the runtime*frame_rate index
                skeleton = skeleton[self.runtime*self.frame_rate:]
                image_copy = draw_utils.skeleton_visualizer(image_copy, skeleton)

            draw_image = customtkinter.CTkImage(Image.fromarray(image_copy))
            self.label_img.configure(image=draw_image)
            time.sleep(1/self.frame_rate)
            self.video_progressbar.configure(value=(index_of()/self.runtime)*100)


    def stop(self):
        pass