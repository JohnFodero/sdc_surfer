def map_range(x, min_x, max_x, min_y, max_y):
    return ( (x - min_x) * ((max_y - min_y) / (max_x - min_x)) ) + min_y

