import cv2
import numpy as np
from sklearn.cluster import KMeans

def prepare_(path):
    '''
    Takes path to image, return resized image in RGB
    '''
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #
    modified_img = cv2.resize(image, (900, 600), interpolation = cv2.INTER_AREA)
    modified_img = modified_img.reshape(modified_img.shape[0]*modified_img.shape[1], 3)
    
    return modified_img

def colors_(modified_img):
    clf = KMeans(n_clusters = 7, random_state = 17)
    color_labels = clf.fit_predict(img)
    center_colors = clf.cluster_centers_
    counts = Counter(color_labels) # Counts of pixels for clusters
    ordered_colors = [center_colors[i] for i in counts.keys()] # RGB coordinates
    cols_ = {}
    for i, j in enumerate(counts):
         cols_.update({counts[j]: center_colors[i]})
    result = sorted(cols_.items(), key=lambda x: x[0], reverse=True) # Sorts by counts
    
    return result

def key_color(colors_):
    '''
    Finds 'key' color - the farthest color for the most popular cluster (shadows, background)
    '''
    colors = [] # List with coordinates (we need to throw away counts)
    for i in range(len(colors_)):
        colors.append(colors_[i][1])
    colors = np.array(colors)
    color = colors[0][1]
    distances = np.sqrt(np.sum((colors-color)**2,axis=1)) # Euclid distance between colors
    index_of_key_color = np.where(distances==np.amax(distances))
    max_distance = colors[index_of_key_color]
    return max_distance

def main(path):
    img = prepare_(path)
    img_col = colors_(img)
    key_col = key_color(img_col)

if __name__ == '__main__':
    main(path)