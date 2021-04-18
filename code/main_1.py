# main.py

from junglebook import Jungle, RateJungle


def main():
    j = Jungle("Ase")
    j.welcomeMessage()

    r = RateJungle(3)
    r.printRating()

    r._staffRating = 30  # directly change the _staffRating

    print("Guide rating :", r._RateJungle__jungleGuideRating)


if __name__ == '__main__':
    main()
