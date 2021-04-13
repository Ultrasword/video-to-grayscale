import cv2
import time
import sys
import subprocess
import multiprocessing

class VtoT:
    def __init__(self):
        self.file = ""
        self.bw = ["█","▓","▒","░","$","{","(","*","."]
        self.frames = 0
        self.dim = (1080, 720)
        self.st = time.time()
        self.buffer = None
        self.saving = False
        self.outputd = None
        self.doExample = False
        self.flush = True
        self.sleepTime = 0
    
    def ProgressBar(self, total, frame):
        percent = "{:.2f}".format(100 * (frame/float(total)))
        filledLength = int(100 * frame // total)
        bar = '█' * filledLength + '-' * (100 - filledLength)
        print("{} |{}| {}% {}".format("|:D|", bar, percent, "|:D|"), end='\r')

    def setSleepTime(self, time):
        self.sleepTime = time

    def setVideo(self, directory):
        #the directory needs to be from root, from C:\
        #or you can do it like "pokemon.mp4"
        self.file = directory

    def getFps(self, path, ffprobe='ffprobe'):
        out = subprocess.check_output(f'"{ffprobe}" -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate -i "{path}"').decode('utf-8')
        top, bottom = [int(x) for x in out.split('/')]
        return top/bottom

    def getInformation(self):
        self.video = cv2.VideoCapture(self.file)
        self.fps = self.getFps(self.file,r'C:\ffmpeg\bin\ffprobe')  #usually 29.203910390219031903 but int() changes it to an int
        self.timebetweenframe = 1/self.fps
        self.outputd = (self.file.split("\\")[-1]).split(".")[0]+f"-{self.dim[0]}-{self.dim[1]}"+".txt"
        self.flushL = self.fps*10
        self.sleepTime = 1/self.fps
        print(self.sleepTime)
        #make sure that you call self.setOutputDir() after calling this function

    def setShadingScheme(self, scheme=["█","▓","▒","░","&",'%',"$","{","(","*","."]): #
        self.bw = scheme

    def setDim(self, dim):
        self.dim = dim

    def changeToChar(self, i):
        if i < 30:
            return self.bw[-1]
        if i < 60:
            return self.bw[-2]
        if i < 90:
            return self.bw[-3]
        if i < 120:
            return self.bw[-4]
        if i < 140:
            return self.bw[-5]
        if i < 170:
            return self.bw[-6]
        if i < 200:
            return self.bw[-7]
        if i < 220:
            return self.bw[-8]
        if i < 240:
            return self.bw[-9]
        if i < 255:
            return self.bw[0]
        else:
            return self.bw[0]

    def setOutputDir(self, outputdir):
        self.outputd = outputdir

    def getinfo(self):
        fp = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        with open(self.outputd, "w") as save:
            save.write(str(self.fps) + "\n")
            while self.frames < fp-1:
                #info is the whole image
                #contains all the characters that make up the image
                info = []
                success, image = self.video.read()
                img = cv2.resize(image, self.dim)
                self.ProgressBar(fp, self.frames)
                for y in range(self.dim[1]):
                    info.append([])
                    for x in range(self.dim[0]):
                        c = img[y][x]
                        #get the mean value of all of the colors
                        c = sum(c)//3
                        #c is the mean of the RGB values
                        info[y].append(self.changeToChar(c))
                #print("\n".join(["".join(v) for v in info]))
                save.write("\n".join(["".join(v) for v in info]))
                self.frames+=1
            save.close()
        self.timetaken = time.time()-self.st
        print(f"Rendering the video took {self.timetaken:.6f} seconds!")
        time.sleep(3)

    def printExample(self):
        for x in range(self.dim[1]):
            print('-'*self.dim[0])
        
    def setPrintExample(self, oui):
        self.doExample = oui

    def play(self):
        #GETTING all the images from the getinfo() command
        if self.buffer == None and self.saving:
            self.buffer = TOut(self.outputd).getBufferedText()
        else:
            print("process is finished")
            time.sleep(2)
            return
        if self.doExample:
            self.printExample()
        input("Input something to continue\n")
        #get how much time to wait after each frame
        """
        This section pretty much expalins how saving works
        currently, the files will save to the current directory, but in the future, people will be able to specify the directory where these files are saved
        """
        """        
        if self.saving:
            with open(self.outputd, "w") as save:
                iter = 0
                save.write(str(self.fps) + "\n")
                save.write(str(self.dim[0]) + ' ' + str(self.dim[1]) + '\n')
                for img in self.buffer:
                    iter += 1
                    self.ProgressBar(len(self.buffer),iter)
                    save.write(img)
                    save.write("\n" + r"\\s+" + "\n")
                save.close()"""
        #so we can keep the framerate consistent and clean :D
        #the loop that plays/prints out the images into console
        i = 0
        for image in self.buffer:
            i+=1
            print(image,end='\r')
            if self.flush and i%self.flushL==0:
                sys.stdout.flush()
            time.sleep(self.sleepTime)
    
    def changeBuffer(self):
        #make sure to change the directory to the video file
        self.buffer = self.getinfo()
    
    def loadFile(self):
        i = input("Directory to the saved file:\n")
        i = "\\".join(i.split("\\"))
        self.setVideo(i)
    
    def playFile(self):
        self.saving = True

    def inputDir(self):
        i = input("Input the directory! Copy and paste from Documents!\n")
        i = i.split("\\")
        i = "\\".join(i)
        self.file= i
    
    def setFlush(self, bol):
        self.flush = bol

class TOut:
    def __init__(self, dire):
        st = time.time()
        with open(f"{dire}","r") as buffered:
            self.dim = [int(x) for x in buffered.readline().split()]
            self.fps = float(buffered.readline())
            self.data = buffered.read().split(r"\\s+")
            buffered.close()
            print(f"This process took {time.time()-st:.2f}s")
        self.flush = True
        self.doExample = False
        self.flushL = self.fps * 10
        self.sleepTime = 1/self.fps
    
    def getBufferedText(self):
        return self.data

    def playBuffer(self):
        i = 0
        if self.doExample:
            self.printExample()
        input("Any buton to start")
        for frame in self.data:
            i += 1
            print("\r",frame)
            if self.flush and i%self.flushL==0:
                sys.stdout.flush()
            time.sleep(self.sleepTime)

    def setSleepTime(self, time):
        self.sleepTime = time
        
    def setFlush(self, bol):
        self.flush = bol

    def printExample(self):
        print(self.data[0])

    def setExample(self, bol):
        self.doExample = bol

    def ProgressBar(self, total, frame):
        percent = "{:.2f}".format(100 * (frame/float(total)))
        filledLength = int(100 * frame // total)
        bar = '█' * filledLength + '-' * (100 - filledLength)
        print("{} |{}| {}% {}".format("|:D|", bar, percent, "|:D|"), end='\r')

    def getFPS(self):
        return self.fps
