def lerp(i, speed, start, end, smooth = True):
    speed -= 1
    p = 1.0/speed*i
    if smooth:
        p = ((p) * (p) * (3 - 2 * (p)))
    return start + (end - start) * p
