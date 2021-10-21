from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, array_to_img
from keras.models import load_model


def predict(path):
    """This functions returns predictions for a given input image

    Parameters: 
    path: path of the image to predict

    """
    #Creating a dictionary of classes as the predict function gives probablities
    actualClasses = { 0:'Cloudy',1:'Rain',2:'Shine',3:'Sunrise' }

    img = load_img(path, target_size=(250, 250))
    img_array = img_to_array(img)

    #Plotting the image
    plt.imshow(img_array/255)
    plt.show()
    img_array = np.expand_dims(img_array, axis=0)

    #Prediction
    pred = model.predict(img_array)
    classes = np.argmax(pred)
    return actualClasses[classes]

def main(path):
    model = load_model('final_model.h5')
    predict(path)

if __name__ == '__main__':
    main(path)