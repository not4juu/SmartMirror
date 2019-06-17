# Table of Contents
1. [Smart Mirror](#smart-mirror)
2. [Getting Started](#getting-started)
3. [Requirements](#requirements)
4. [Running](#running)
5. [Runtime logs](#runtime-logs)
6. [Author](#author)
7. [Api License](#license)

# Smart Mirror

Smart Mirror application has been created for Raspberry Pi 3 deployment using biometric aspects to communicate and control running app.

## Getting Started

Application is using:
* User Authorization based on biometric face recognition, options implemented
    * [opencv face](https://docs.opencv.org/3.4/dd/d65/classcv_1_1face_1_1FaceRecognizer.html)
    * [face_recognition](https://pypi.org/project/face_recognition/)
* Voice Command based on biometric [voice recognition](https://pypi.org/project/SpeechRecognition/)
* [Application Window](https://docs.python.org/3/library/tk.html)
    * date & clock time 
    * weather - working with [darksky api](https://darksky.net/dev)
    * news - collected from [google_news](https://news.google.com/rss)
    * user login
    * menu connections (containing camera, microphone, network)
* Multithreading architecture to optimize application process on Raspberry Pi 3 (all cores usage)    
    
Application was developed and tests under Windows 10 and Raspberry Pi 3 (Raspbian GNU/Linux 8.0 (jessie)
) systems.

## Requirements

First, make sure you have all the requirements listed in the "Requirements" section.

The easiest way to install this is using

```
pip3 install SmartMirror
```


* Python 3.3+ (required)
* OpenCV 
* Dlib > 19.7.0
* CMake
* eSpeak
* Pillow (please fallow pillow [dependencies](https://github.com/python-pillow/Pillow/tree/master/dependse)

### Windows 10 

Please ensure which dlib version is supported by your python interpreter (64bit/32bit architecture) and choose the proper one

recommended (tested one): 
 * windows [python 3.5.0 interpreter](https://www.python.org/ftp/python/3.5.0/python-3.5.0.exe) 
 * dlib - [dlib-19.7.0.tar.gz](https://pypi.org/simple/dlib/)
 
 ```
    pip3 install https://files.pythonhosted.org/packages/e2/79/6aba1d2b3f9fbcf34d583188d8ff6818952ea875dceedf7c34a869637573/dlib-19.7.0.tar.gz#sha256=8728d820094f8df4a7c66fa5d8b4c944921ae79c56a094e33f2684122133fe6d
 ```

OpenCV can be easly installed via pip

### Raspberry Pi OS

*Please be patient checkout repos and compilation process take a lot of time.*
    
Before you start the compile process, you should increase your swap space size. This enables OpenCV to compile with all four cores of the Raspberry PI without the compile hanging due to memory problems.
```
cat /etc/dphys-swapfile
# set size to absolute value, leaving empty (default) then uses computed value
# you most likely don't want this, unless you have an special disk situation
# CONF_SWAPSIZE=100
CONF_SWAPSIZE=1024

sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
```

eSpeak lib (libspeak.so required by pyttsx3): 
```
   sudo apt-get install espeak
```

#####OpenCV

Firstly, please install all dependencies

```
[compiler] sudo apt-get install build-essential
[required] sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
[required] sudo apt-get install python-tk tk8.5-dev tcl8.5-dev tk8.5 tcl8.5  zlib1g-dev liblcms2-dev
[optional] sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
```

When all openCV dependencies have been installed. Checkout openCV source code and compile it (please remember to set `ENABLE_NEON=ON` flag) [NEON_Benchmark](https://medium.com/@ghalfacree/benchmarking-the-raspberry-pi-3-b-plus-44122cf3d806)

```
    cd ~/
    git clone https://github.com/opencv/opencv.git
    git clone https://github.com/opencv/opencv_contrib.git
    cd opencv
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/bin \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules/ \
        -D ENABLE_NEON=ON \
        -D ENABLE_VFPV3=ON \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_EXAMPLES=OFF 
        
    make j4
```

#####DLib

Install all dlib dependencies
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-pip \
    zip
sudo apt-get clean
```

```
sudo apt-get install python3-picamera
sudo pip3 install --upgrade picamera[array]
```
When all dLib dependencies have been installed. Checkout proper version of dlib source code and compile it (please remember to set `-mfpu=neon` flag) [NEON_Benchmark](https://medium.com/@ghalfacree/benchmarking-the-raspberry-pi-3-b-plus-44122cf3d806)

```
mkdir -p dlib
git clone -b 'v19.8' --single-branch https://github.com/davisking/dlib.git dlib/
cd ./dlib
sudo python3 setup.py install --compiler-flags "-mfpu=neon"
```

finally install `face_recognition` module
```
sudo pip3 install face_recognition
```
## Running

At the beginning prepares a images frames with users which can by authorized in application (run only once when images do not exist)

### Capture user face & model training
* Capture user image frames
```
    python3 tools/face_sample_collector.py
```
it will capture a default summary  30 image frames with user face recognition where (10 frames need only face detection, 10 frames beside face need to detect eyes & next 10 beside face need to detect smile)

* Train model

```
    python3 tools/face_training.py
```

two way of training are available, default one `face_recognition` which are much more confidence with final face authorization buy working slower then second option `face_opencv` 

```
    python3 tools/face_training.py -t face_opencv 
```

### Running app

```
    python3 -m smartmirror
```

## Runtime logs

Api provide functionality with step by step runtime logs collection 

```log
[2019-06-13 23:05:24,298:MainThread:Logger:39:INFO] Logger has been created successfully outfile: True verbose: None
[2019-06-13 23:05:24,298:MainThread:__main__:27:DEBUG] Initialization of properties finish successfully
[2019-06-13 23:05:24,298:MainThread:messages_handler:16:DEBUG] Initialized a Messages Handler object
[2019-06-13 23:05:24,299:MainThread:ui_thread:29:DEBUG] Initialization of User Interface Thread class
[2019-06-13 23:05:24,299:UI_Thread:ui_thread:157:INFO] User_Interface thread runs
[2019-06-13 23:05:24,299:MainThread:uc_thread:22:DEBUG] Initialization of User Command Thread class
[2019-06-13 23:05:24,360:UC_Thread:uc_thread:77:INFO] User_Command thread runs
[2019-06-13 23:05:24,360:MainThread:__main__:48:DEBUG] Threads starts successfully
[2019-06-13 23:05:24,360:UC_Thread:uc_thread:25:INFO] Waiting for initialization network and window
[2019-06-13 23:05:24,361:MainThread:__main__:63:INFO] __main__ ends
[2019-06-13 23:05:25,588:UI_Thread:connections_menu:59:DEBUG] Initialization of Connections class
[2019-06-13 23:05:25,600:UI_Thread:clock:41:DEBUG] Initialization of Clock class
[2019-06-13 23:05:25,693:UI_Thread:user:25:DEBUG] Initialization of User class
[2019-06-13 23:05:25,704:UI_Thread:pulse_text:21:DEBUG] Initialization of PulseText class
[2019-06-13 23:05:25,704:UI_Thread:api_window:71:DEBUG] Initialization of Application Window class
[2019-06-13 23:05:25,704:UI_Thread:messages_handler:23:DEBUG] Sends : API_WINDOW_INITIALIZED
[2019-06-13 23:05:25,704:UC_Thread:messages_handler:33:DEBUG] Received : API_WINDOW_INITIALIZED
[2019-06-13 23:05:25,704:UC_Thread:uc_thread:64:DEBUG] handler_window_success
[2019-06-13 23:05:27,401:UI_Thread:speaker:13:DEBUG] Speaker Class initialized correctly
[2019-06-13 23:05:27,407:UI_Thread:camera:27:DEBUG] Find camera connection
[2019-06-13 23:05:27,653:UI_Thread:connections_menu:69:DEBUG] Camera has been enabled
[2019-06-13 23:05:27,658:UI_Thread:messages_handler:23:DEBUG] Sends : API_WINDOW_INITIALIZED
[2019-06-13 23:05:27,658:UC_Thread:messages_handler:33:DEBUG] Received : API_WINDOW_INITIALIZED
[2019-06-13 23:05:27,658:UI_Thread:pulse_text:43:DEBUG] Set pulse text animation: Autoryzacja
[2019-06-13 23:05:27,658:UC_Thread:uc_thread:64:DEBUG] handler_window_success
[2019-06-13 23:05:27,682:UI_Thread:pulse_text:49:DEBUG] Start pulse text animation
[2019-06-13 23:05:27,721:UI_Thread:authorization:149:DEBUG] Start authorization thread: dlib_face_recognition
[2019-06-13 23:05:27,727:UI_Thread:ui_thread:64:DEBUG] Start authorization process
[2019-06-13 23:05:28,672:UI_Thread:ui_thread:102:DEBUG] Close thread : "API_USER_QUIT"
[2019-06-13 23:05:28,678:UI_Thread:messages_handler:23:DEBUG] Sends : API_USER_QUIT
[2019-06-13 23:05:28,678:UI_Thread:authorization:164:DEBUG] Stop authorization thread
[2019-06-13 23:05:28,678:UC_Thread:messages_handler:33:DEBUG] Received : API_USER_QUIT
[2019-06-13 23:05:28,678:UC_Thread:uc_thread:64:DEBUG] handler_api_window_close
[2019-06-13 23:05:28,678:UC_Thread:uc_thread:81:INFO] User_Command thread ends
[2019-06-13 23:05:28,678:UI_Thread:pulse_text:54:DEBUG] Stop pulse text animation
[2019-06-13 23:05:28,678:UI_Thread:ui_thread:69:DEBUG] Stop authorization process
[2019-06-13 23:05:28,678:UI_Thread:ui_thread:164:INFO] User_Interface thread ends

```
## Author

* **Sebastian Kałużny** --- [not4juu](https://github.com/not4juu/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


