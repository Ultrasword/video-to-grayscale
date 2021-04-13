#this file will be a demonstration on how to use this, or the python files

#I will use pygame for this because visual representations are good
import pygame
#now import the two files
import vtot, vtoa
#asyncio because its cool
import asyncio
#os to check if the file exists
from os.path import exists


pygame.init()
dimensions = (1080,720)
display = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()

#some important functions to display the file, the BW colors
async def textwrap(text):
    return [str(x) for x in text.split("\n")]

#get rendered text to display onto pygame window
async def getRendered(font, buffered, iter):
    x = []
    #for y in textwrap(buffered[iter]):
    for y in buffered:
        x.append(font.render(y,False,(255,255,255)))
    return x

#a class to access a bunch of functions
class ReadFile:
    def __init__(self, directory, **kwargs):
        self.font = pygame.font.Font('lucida-console.ttf',5)
        self.file = open(directory,"r")
        if "dim" in kwargs:
            self.dim = kwargs["dim"]
            self.file.readline()
        else:
            x, y = [x for x in self.file.readline()]
            self.dim = (int(x),int(y.split("\n")[0]))
        if "fps" in kwargs:
            self.fps = kwargs["fps"]
        else:
            self.fps = float(self.file.readline())
        
    async def readFrame(self):
        l = []
        self.file.readline()
        for x in range(self.dim[1]-2):
            l.append(self.file.readline())
        return await getRendered(self.font,l,0)

    def close(self):
        self.file.close()

"""

Because Github doesn't allow the upload of files over 25 Mb, this will be an example on how to use vtot to make the text version of the video

"""

path = ""
#path = r'Videos\pokemon.mp4'
#path = r'Videos\manhera chan.gif'
#path = r'D:\FDY Sans Hard Mode Full Fight Re-balanced Completed!.mp4'
save = r'videoplayback (1).mp4'

ss = ["#","%","&","$","@",'!',"[","{","(","*","."]
"""
MUST CHANGE TO THIS IF YOU WANT TO SAVE TO A TXT FILE!!!
THE ORIGINAL VERSION uses characters which aren't in ascii as it was originally made for console output.

The shading scheme must be set to a different set if you want to save the file.
rendering the text may take a while, please be patient! :D
"""

#checks if the file exists
if not exists("videoplayback (1)-240-100.txt"):
    v = vtot.VtoT()
    v.setVideo(path)
    v.setDim((240,100))
    v.setOutputDir(save)
    v.fps = v.getFps(path,'C:\\ffmpeg\\bin\\ffprobe')
    v.playFile()
    v.setShadingScheme(ss)
    v.getInformation()
    v.getinfo()
    v.play()

#load the file
temp = ReadFile("videoplayback (1)-240-100.txt",dim=(240,100))

#here are some of the functions to make this faster, using buffers

FrameBuffer = []
#a buffer of size 200

apath = "Bad Apple Song.mp3"

#sound
channel = pygame.mixer.Channel(0)
audio = pygame.mixer.music.load(apath)

async def startLoadingBuffers():
    global temp
    if len(FrameBuffer) > 200:
        return
    FrameBuffer.append(await temp.readFrame())
    FrameBuffer.append(await temp.readFrame())

async def playVideo():
    #input("anything to start :D\nHold the stream hostage XD")
    run = True
    pygame.mixer.music.play()
    while run:
        #print(pygame.mixer.music.get_pos(), frame%temp.fps)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
        display.fill((0,0,0))

        await startLoadingBuffers()
        for x in range(len(FrameBuffer[0])):
            display.blit(FrameBuffer[0][x], (0,5*x))
        FrameBuffer.pop(0)

        pygame.display.flip()
        clock.tick(temp.fps)

    temp.close()


asyncio.run(playVideo())

pygame.quit()
