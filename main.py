import requests
import shutil
import os
import cv2 as cv
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import numpy as np


def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist



def plot_colors(hist, centroids):
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0

	for (percent, color) in zip(hist, centroids):
		endX = startX + (percent * 300)
		cv.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	
	return bar



def DownloadImages(gameImages, gameDirectory):

    for screenshotUrl in gameImages:
        imageResponse = requests.get(screenshotUrl['path_full'], stream=True)
        
        imageNameRaw = screenshotUrl['path_full'].rsplit('/', 1)[-1]
        imageNameClean = imageNameRaw.split('?')[0]

        with open(gameDirectory + '\\' + imageNameClean, 'wb') as out_file:
            shutil.copyfileobj(imageResponse.raw, out_file)
        del imageResponse
    
    print('Images Downloaded')



def ResizeImage(image, imageScale):

    width = int(image.shape[1] * imageScale / 100)
    height = int(image.shape[0] * imageScale / 100)
    dim = (width, height)
  
    resized = cv.resize(image, dim, interpolation = cv.INTER_AREA)

    return resized



def DownloadImages(gameId):
    gameId = str(gameId)
    requestResponse = requests.get('https://store.steampowered.com/api/appdetails?appids=' +  gameId)

    try:
        gameData = requestResponse.json()[gameId]['data']
    except:
        print('Error Game Not Found')

    gameImages = gameData['screenshots']

    gameName = gameData['name'] + '-' +str(gameId)
    gameDirectory = 'screenshots\\' + ''.join(x for x in gameName if x.isalnum())

    if not os.path.exists(gameDirectory):
        os.makedirs(gameDirectory)
        print('Game Directory Created')

        DownloadImages(gameImages, gameDirectory)
    else: 
        print('Game Directory Already Exists. Checking for images.')

        if len(os.listdir(gameDirectory)) <= 3:
            for f in os.listdir(gameDirectory):
                os.remove(os.path.join(gameDirectory, f))

            DownloadImages(gameImages, gameDirectory)
        else:
            print('Images already present, skipping download.')
    
    return gameDirectory



def main(gameId, numClusters, imageScale = 20): 
    
    gameDirectory = DownloadImages(gameId)

    vectorOfImages = []

    for img in os.scandir(gameDirectory):
        if (img.path.endswith('.jpg')):
            imageOriginal = cv.imread(img.path)
            image = cv.cvtColor(imageOriginal, cv.COLOR_BGR2RGB)
            image = ResizeImage(image, imageScale)
            image = image.reshape((image.shape[0] * image.shape[1], 3))
            vectorOfImages.extend(image)

    kMeansCluster = KMeans(n_clusters = numClusters)
    kMeansCluster.fit(vectorOfImages)

    hist = centroid_histogram(kMeansCluster)
    bar = plot_colors(hist, kMeansCluster.cluster_centers_)

    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.show()



if __name__ == "__main__":
    gameId = 1079800
    numClusters = 10
    imageScale = 20 #percentage scale to reduce the image to

    main(gameId, numClusters, imageScale)