

class Maths:

    @staticmethod
    def subtract_percent(num, percent) -> int:
        percent = 100 - percent
        num = num * percent / 100
        return int(num)
