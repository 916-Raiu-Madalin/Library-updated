class Settings:
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__list = []
        self.__repository = None
        self.__books = None
        self.__clients = None
        self.__rentals = None

    def settings(self):
        try:
            with open(self.__file_name, "r") as f:
                for i in range(0, 4):
                    line = f.readline()
                    line = line.split('=')
                    line[-1] = line[-1][:-1]
                    self.__list.append(line[1])
        except IOError as ie:
            raise IOError(ie)

    def get_the_settings(self):
        self.settings()
        self.__rentals = self.__list.pop()
        self.__clients =self.__list.pop()
        self.__books =self.__list.pop()
        self.__repository = self.__list.pop()
        return [self.__repository,self.__books,self.__clients,self.__rentals]
