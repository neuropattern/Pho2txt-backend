class ImageProcessing:

    def __init__(self):
        self.__source_image = None

    def __set_source_image(self, image):
        self.__source_image = image

    def __get_source_image(self):
        return self.__source_image

    source_image = property(__get_source_image)

    def prefiltration(self, image):
        pass

    def binarization(self, image):
        pass
