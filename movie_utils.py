import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *

'''
paras[0] = video path
paras[1] = start
paras[2] = end
'''
def split1():
    paras = sys.argv[2:]
    vpath = paras[0]
    st = int(paras[1])
    et = int(paras[2])
    if len(paras) < 3:
        print "error parameters"
        return
    ffmpeg_extract_subclip(vpath, st, et, targetname="example1.mp4")

def split2():
    paras = sys.argv[2:]
    vpath = paras[0]
    st = int(paras[1])
    et = int(paras[2])
    if len(paras) < 3:
        print "error parameters"
        return
    clip = VideoFileClip(vpath).subclip(st, et)
    video = concatenate([clip])
    video.write_videofile("example2.mp4")



def main():
    func = getattr(sys.modules[__name__], sys.argv[1])
    func()

if __name__ == "__main__":
    main()
