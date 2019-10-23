# coding=utf-8
# Scripts to try and detect key frames that represent scene transitions
# in a video. Has only been tried out on video of slides, so is likely not
# robust for other types of video.

# 1. 基于图像信息
# 2. 基于运动分析(光流分析)

import cv2
import argparse
import json
import os
import numpy as np
import errno

def getInfo(sourcePath):
    cap = cv2.VideoCapture(sourcePath)
    info = {
        "framecount": cap.get(cv2.CAP_PROP_FRAME_COUNT),
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "heigth": int(cap.get(cv2.CAP_PROP_FRAME_Heigth)),
        "codec": int(cap.get(cv2.CAP_PROP_FOURCC))
    }
    cap.release()
    return info


def scale(img, xScale, yScale):
    res = cv2.resize(img, None,fx=xScale, fy=yScale, interpolation = cv2.INTER_AREA)
    return res

def resize(img, width, heigth):
    res = cv2.resize(img, (width, heigth), interpolation = cv2.INTER_AREA)
    return res

#
# Extract [numCols] domninant colors from an image
# Uses KMeans on the pixels and then returns the centriods
# of the colors
#
def extract_cols(image, numCols):
    # convert to np.float32 matrix that can be clustered
    Z = image.reshape((-1,3))
    Z = np.float32(Z)

    # Set parameters for the clustering
    max_iter = 20
    epsilon = 1.0
    K = numCols
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, epsilon)
    labels = np.array([])
    # cluster
    compactness, labels, centers = cv2.kmeans(Z, K, labels, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    clusterCounts = []
    for idx in range(K):
        count = len(Z[labels == idx])
        clusterCounts.append(count)

    #Reverse the cols stored in centers because cols are stored in BGR
    #in opencv.
    rgbCenters = []
    for center in centers:
        bgr = center.tolist()
        bgr.reverse()
        rgbCenters.append(bgr)

    cols = []
    for i in range(K):
        iCol = {
            "count": clusterCounts[i],
            "col": rgbCenters[i]
        }
        cols.append(iCol)

    return cols


#
# Calculates change data one one frame to the next one.
#
def calculateFrameStats(sourcePath, verbose=False, after_frame=0):  # 提取相邻帧的差别
    cap = cv2.VideoCapture(sourcePath)#提取视频

    data = {
        "frame_info": []
    }

    lastFrame = None
    while(cap.isOpened()):
        ret, frame = cap.read()
        if frame == None:
            break

        frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1

        # Convert to grayscale, scale down and blur to make
        # calculate image differences more robust to noise
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      # 提取灰度信息
        gray = scale(gray, 0.25, 0.25)      # 缩放为原来的四分之一
        gray = cv2.GaussianBlur(gray, (9,9), 0.0)   # 做高斯模糊

        if frame_number < after_frame:
            lastFrame = gray
            continue


        if lastFrame != None:

            diff = cv2.subtract(gray, lastFrame)        # 用当前帧减去上一帧

            diffMag = cv2.countNonZero(diff)        # 计算两帧灰度值不同的像素点个数

            frame_info = {
                "frame_number": int(frame_number),
                "diff_count": int(diffMag)
            }
            data["frame_info"].append(frame_info)

            if verbose:
                cv2.imshow('diff', diff)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # Keep a ref to this frame for differencing on the next iteration
        lastFrame = gray

    cap.release()
    cv2.destroyAllWindows()

    #compute some states
    diff_counts = [fi["diff_count"] for fi in data["frame_info"]]
    data["stats"] = {
        "num": len(diff_counts),
        "min": np.min(diff_counts),
        "max": np.max(diff_counts),
        "mean": np.mean(diff_counts),
        "median": np.median(diff_counts),
        "sd": np.std(diff_counts)   # 计算所有帧之间, 像素变化个数的标准差
    }
    greater_than_mean = [fi for fi in data["frame_info"] if fi["diff_count"] > data["stats"]["mean"]]
    greater_than_median = [fi for fi in data["frame_info"] if fi["diff_count"] > data["stats"]["median"]]
    greater_than_one_sd = [fi for fi in data["frame_info"] if fi["diff_count"] > data["stats"]["sd"] + data["stats"]["mean"]]
    greater_than_two_sd = [fi for fi in data["frame_info"] if fi["diff_count"] > (data["stats"]["sd"] * 2) + data["stats"]["mean"]]
    greater_than_three_sd = [fi for fi in data["frame_info"] if fi["diff_count"] > (data["stats"]["sd"] * 3) + data["stats"]["mean"]]

    # 统计其他信息
    data["stats"]["greater_than_mean"] = len(greater_than_mean)
    data["stats"]["greater_than_median"] = len(greater_than_median)
    data["stats"]["greater_than_one_sd"] = len(greater_than_one_sd)
    data["stats"]["greater_than_three_sd"] = len(greater_than_three_sd)
    data["stats"]["greater_than_two_sd"] = len(greater_than_two_sd)

    return data



#
# Take an image and write it out at various sizes.
#
# TODO: Create output directories if they do not exist.
#
def writeImagePyramid(destPath, name, seqNumber, image):
    fullPath = os.path.join(destPath, "full", name + "-" + str(seqNumber) + ".png")
    halfPath = os.path.join(destPath, "half", name + "-" + str(seqNumber) + ".png")
    quarterPath = os.path.join(destPath, "quarter", name + "-" + str(seqNumber) + ".png")
    eigthPath = os.path.join(destPath, "eigth", name + "-" + str(seqNumber) + ".png")
    sixteenthPath = os.path.join(destPath, "sixteenth", name + "-" + str(seqNumber) + ".png")

    hImage = scale(image, 0.5, 0.5)
    qImage = scale(image, 0.25, 0.25)
    eImage = scale(image, 0.125, 0.125)
    sImage = scale(image, 0.0625, 0.0625)

    cv2.imwrite(fullPath, image)
    cv2.imwrite(halfPath, hImage)
    cv2.imwrite(quarterPath, qImage)
    cv2.imwrite(eigthPath, eImage)
    cv2.imwrite(sixteenthPath, sImage)



#
# Selects a set of frames as key frames (frames that represent a significant difference in
# the video i.e. potential scene chnges). Key frames are selected as those frames where the
# number of pixels that changed from the previous frame are more than 1.85 standard deviations
# times from the mean number of changed pixels across all interframe changes.
#
def detectScenes(sourcePath, destPath, data, name, verbose=False):
    destDir = os.path.join(destPath, "images")

    # TODO make sd multiplier externally configurable
    #diff_threshold = (data["stats"]["sd"] * 1.85) + data["stats"]["mean"]
    diff_threshold = (data["stats"]["sd"] * 2.05) + (data["stats"]["mean"])

    cap = cv2.VideoCapture(sourcePath)
    for index, fi in enumerate(data["frame_info"]):
        if fi["diff_count"] < diff_threshold:
            continue

        cap.set(cv2.CAP_PROP_POS_FRAMES, fi["frame_number"])
        ret, frame = cap.read()

        # extract dominant color
        small = resize(frame, 100, 100)
        cols = extract_cols(small, 5)
        data["frame_info"][index]["dominant_cols"] = cols


        if frame != None:
            writeImagePyramid(destDir, name, fi["frame_number"], frame)

            if verbose:
                cv2.imshow('extract', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    cap.release()
    cv2.destroyAllWindows()
    return data


def makeOutputDirs(path):
    try:
        #todo this doesn't quite work like mkdirp. it will fail
        #fi any folder along the path exists. fix
        os.makedirs(os.path.join(path, "metadata"))
        os.makedirs(os.path.join(path, "images", "full"))
        os.makedirs(os.path.join(path, "images", "half"))
        os.makedirs(os.path.join(path, "images", "quarter"))
        os.makedirs(os.path.join(path, "images", "eigth"))
        os.makedirs(os.path.join(path, "images", "sixteenth"))
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # parser.add_argument('-s','--source', help='source file', required=True)
    # parser.add_argument('-d', '--dest', help='dest folder', required=True)
    # parser.add_argument('-n', '--name', help='image sequence name', required=True)
    # parser.add_argument('-a','--after_frame', help='after frame', default=0)
    # parser.add_argument('-v', '--verbose', action='store_true')
    # parser.set_defaults(verbose=False)

    parser.add_argument('-s','--source', help='source file', default="video.mp4")
    parser.add_argument('-d', '--dest', help='dest folder', default="key frame")
    parser.add_argument('-n', '--name', help='image sequence name', default="")
    parser.add_argument('-a','--after_frame', help='after frame', default=0)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.set_defaults(verbose=False)

    args = parser.parse_args()

    if args.verbose:
        info = getInfo(args.source)
        print("Source Info: ", info)

    makeOutputDirs(args.dest)

    # Run the extraction
    data = calculateFrameStats(args.source, args.verbose, int(args.after_frame))
    data = detectScenes(args.source, args.dest, data, args.name, args.verbose)
    keyframeInfo = [frame_info for frame_info in data["frame_info"] if "dominant_cols" in frame_info]

    # Write out the results
    data_fp = os.path.join(args.dest, "metadata", args.name + "-meta.json")
    with open(data_fp, 'w') as f:
        data_json_str = json.dumps(data, indent=4)
        f.write(data_json_str)

    keyframe_info_fp = os.path.join(args.dest, "metadata", args.name + "-keyframe-meta.json")
    with open(keyframe_info_fp, 'w') as f:
        data_json_str = json.dumps(keyframeInfo, indent=4)
        f.write(data_json_str)