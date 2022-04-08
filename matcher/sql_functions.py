from datetime import datetime
from metaphone import doublemetaphone


def concat(*args):
    return ''.join(args)


def Dmetaphone(input):
    return doublemetaphone(str(input))[0]


date_format = "%Y-%m-%d"


def datediff(d1, d2):
    a = datetime.strptime(d1, date_format)
    b = datetime.strptime(d2, date_format)
    delta = b - a
    return abs(delta.days)
