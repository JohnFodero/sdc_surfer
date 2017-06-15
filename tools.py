import csv
import cv2
import numpy as np

def map_range(x, min_x, max_x, min_y, max_y):
    return ( (x - min_x) * ((max_y - min_y) / (max_x - min_x)) ) + min_y

def import_data(directory):

    raw_X = []
    raw_y = []
    data_path = '../inloop'
    with open(data_path + '/capture_log.csv', 'r') as f:
        reader = csv.reader(f)
        iterreader = iter(reader)
        next(iterreader)
        for row in iterreader:
            path = data_path + row[0][1:]
            img = cv2.imread(path)
            if img is not None:
                raw_X.append(img) 
                raw_y.append(float(row[2]))
    return np.array(raw_X), np.array(raw_y)

def shuffle_data(X, y):
    assert len(X) == len(y)
    p = np.random.permutation(len(X))
    return X[p], y[p]

def split_data(X, y, train_mark, val_mark):
    train_mark = int(len(X) * train_mark)
    val_mark = train_mark + int(len(X) * val_mark)

    train_X, train_y = X[:train_mark], y[:train_mark]
    val_X, val_y = X[train_mark:val_mark], y[train_mark:val_mark]
    test_X, test_y = X[val_mark:], y[val_mark:]
    
    return train_X, train_y, val_X, val_y, test_X, test_y

def process_image(image):
    # crop out the horizon
    img = image[35:,:,:]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img = cv2.resize(img, (200, 66)) 
    return img

def normalize(images):
    return images.astype('float32') / 255




