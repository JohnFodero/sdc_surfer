from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import datetime

class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True)
        
        self.frame = None
        self.stopped = False
        
    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        for f in self.stream:
            self.frame - f.array
            self.rawCapture.truncate(0)
            
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
            
    def read(self):
        return self.frame
    
    def stop(self):
        self.stopped = True

class FPS:
    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0
    
    def start(self):
        self._start = datetime.datetime.now()
        
    def stop(self):
        self._end = datetime.datetime.now()
    
    def update(self):
        self._numFrames += 1
    
    def elapsed(self):
        return (self._end - self._start).total_seconds()
    
    def fps(self):
        return self._numFrames / self.elapsed()