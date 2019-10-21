import numpy as np
import torchvision
from PIL import Image

trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True)
images = trainset.data # 50000, 32, 32, 3
choices = [159,1107,2026,3721,3857,3878,4303,7764,11150,11875,11974,14712,16883,17130,17377,22274,24496,26202,26499,27803,30136,31948,32186,34493,36462,37445,37885,39326,42358,43145,45626,47921,48116]
targets = images[choices]
averaged = np.mean(targets, axis=0).astype(np.uint8)
Image.fromarray(averaged).save("averaged.png")

# test
averaged = np.array(Image.open("averaged.png"))
averaged = averaged.reshape(-1).astype(np.float)
images = images.reshape(len(images), -1).T
from sklearn import linear_model
clf = linear_model.Lasso(alpha=1, positive=True)
clf.fit(images, averaged)

# cliff search
sorted_coef = np.sort(clf.coef_)[::-1]
prev = sorted_coef[0]
for i, coef in enumerate(sorted_coef):
    if prev / coef > 10:
        break
    prev = coef
secret = np.sort(np.argsort(clf.coef_)[::-1][:i])
print(secret)
assert np.array_equal(secret, choices)
