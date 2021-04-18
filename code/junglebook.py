# junglebook.py


class Jungle():
    def __init__(self, name="Uknown"):  # construct with default value
        self.visitorName = name

    def welcomeMessage(self):
        print("Hello %s, welcome to the Jungle" % self.visitorName)


class RateJungle():
    def __init__(self, feedback):
        self.feedback = feedback  # public attribute
        self._staffRating = 50  # public attribute author does not want to accesse it directly
        self.__jungleGuideRating = 100  # private attribute
        self.updateStaffRating()
        self.updateGuideRating()

    def printRating(self):
        print("Feedback : %s \tGuide Rating: %s \tStaff Rating %s " %
              (self.feedback, self.__jungleGuideRating, self._staffRating))

    def updateStaffRating(self):
        if self.feedback < 5:
            self._staffRating += 50
        else:
            self._staffRating -= 5

    def updateGuideRating(self):
        if self.feedback < 5:
            self.__jungleGuideRating += 10
        else:
            self.__jungleGuideRating -= 10
