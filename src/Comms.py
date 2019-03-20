from Mode import Mode


class Comm:
    __instance = None

    def get_instance():
        if Comm.__instance == None:
            Comm()
        return Comm.__instance

    def __init__(self):
        if Comm.__instance != None:
            raise Exception("Constructor should not be called")
        else:
            Comm.__instance = CommSingleton()


class CommSingleton:
    def __init__(self):
        self.__mode = Mode.STANDBY

    def standby(self):
        self.__mode = Mode.STANDBY

    def testing(self):
        self.__mode = Mode.TESTING

    def flight(self):
        self.__mode = Mode.FLIGHT

    def send(self, command):
        if self.__mode == Mode.STANDBY:
            # discard command
            print("Standby")

        if self.__mode == Mode.TESTING:
            print(command)

        if self.__mode == Mode.FLIGHT:
            print("Flight")
            # TODO Send command
