import random


def get_phone():
    num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187',
                 '188',
                 '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
    s = ""
    for i in range(8):
        s += str(random.randint(0, 9))
    string =random.choice(num_start) + s
    return string
