import arcade
import math

def lerp(start,end,ratio):
    compare = (start-end)
    if compare == 0:
        return start
    else:
        if ratio >= 0 and ratio <= 1:
            final = (ratio*start) + ((1-ratio)*end)
        else:
            return None
        return final
