# Real Time Object Detection using TensorFlow Object Detection API
Demo of object detection using this script can be found [here](https://vimeo.com/296105330). TensorFlow's ssd_mobilenet_v1_coco model is used in object detection ([other models](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)). [TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection) identifies multiple objects in a single image. For object detection on a real time video stream we can pass frames to the API and with the help of python's [multiprocessing library](https://docs.python.org/3.5/library/multiprocessing.html) increase performance for a better FPS.
## Executing the script
1. First you have to export the path of `local_execute.sh` in variable PATH_TO_CADRS.
```
export PATH_TO_CADRS=<path-to-this-repository>/object_detection
```
2. Change your directory to `object_detection`.
```
cd <path-to-this-repository>/object_detection
```
3. Build the docker image.
```
docker build -t tensorflow_object_detection .
```
4. Run `local_execute.sh`.
```
bash local_execute.sh
```
## Terminating the program
Press `e` to stop execution of the program.

## Passing arguments to python script
Usage along with default values are as follows:
1. Number of workers: `-w 2`
2. Size of the queue: `-q-size 5`
3. Should the object detection video be saved: `-o 0`
4. Name of the input file: `-i ''`

## Usage of python script from the docker image
### Real time - using WebCam
Note that this is tested on Ubuntu and executing this script on Windows or Mac may cause errors.
```
python script.py
```
### Input video
```
python3 script.py -o 1 -i inpvid.mp4 -w 10 -q-size 20
```
