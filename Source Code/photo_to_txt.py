class PhotoToTxt:

    def __init__(self, image=None):
        self.__set_image(image)

    def __set_image(self, image):
        self.__image = image

    def __get_image(self):
        return self.__image

    image = property(__get_image, __set_image)

    def upload_image(self, image):
        self.__set_image(image)

    def image_recognition(self):
        pass
