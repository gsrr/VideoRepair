# https://zulko.github.io/moviepy/crash_course/crash_course.html
import os
import sys
from moviepy.editor import *
import copy


def start_split(name, interval, index):
        # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
        clip = VideoFileClip(name).subclip(interval[0], interval[1])

        # Composite video clips
        video = concatenate([clip])

        # Write the result to a file
        dest = "files/movie_part%d.mp4" % index
        print "Generate : %s" % dest
        video.write_videofile(dest)

def split4():
    for i in range(4):
        start = i * 60 + 1
        end = ( i + 1 ) * 60
        start_split("0KRt1FCSpIQ.mp4", (start, end), i)

def split_movie_with_reminder(name, interval, index):
        ignore_index = [0]
        print "start to split movie:(%s, %s, %d)" %(name, str(interval), index)
        clip = VideoFileClip(name)
        duration_orig = clip.duration

        subclip1 = VideoFileClip(name).subclip(interval[0], interval[1])
        subclip2 = VideoFileClip(name).subclip(interval[1], duration_orig)
        video1 = concatenate([subclip1])
        video2 = concatenate([subclip2])
        movie_part = "files/movie_part_%d.mp4" % index
        next_name = os.path.splitext(name)[0]
        next_name = "./%s_%d.mp4"%(next_name, index)
        if index not in ignore_index:
            print "Generate part from %s" % movie_part
            video1.write_videofile(movie_part)
            print "Remove part from %s" % next_name
            video2.write_videofile(next_name)
        return next_name

def get_video_duration(name):
    clip = AudioFileClip(name)
    return clip.duration
    
def split_audio_with_reminder(name, interval, index):
        ignore_index = []
        print "start to split audio:(%s, %s, %d)" %(name, str(interval), index)
        clip = AudioFileClip(name)
        duration_orig = clip.duration

        subclip1 = AudioFileClip(name).subclip(interval[0], interval[1])
        subclip2 = AudioFileClip(name).subclip(interval[1], duration_orig)
        basename = os.path.splitext(name)[0].split("_")[0]
        audio_part = "files/part_%s_%d.wav" % (basename, index)
        next_name = "%s_%d.wav"%(basename, index)
        if index not in ignore_index:
            print "Generate part from %s" % audio_part
            subclip1.write_audiofile(audio_part, fps=22050)
            print "Remove part from %s" % next_name
            subclip2.write_audiofile(next_name, fps=22050)
        return next_name


def audio_moviepy_convert(audio_file, index):
    name = "audio%d.wav"%index
    clip = AudioFileClip(audio_file)
    clip.write_audiofile(name, fps=22050)
    return name

def split_wav_file():
    clip = AudioFileClip("video124WAV.wav")
    print clip.duration
    subclip = clip.subclip(60, 70)
    subclip.write_audiofile("/tmp/test.wav", fps=44100)

def split_video_test():
    video = sys.argv[1]     # video name
    start = 0
    end = float(sys.argv[2])      # end time
    i = int(sys.argv[3])     # index
    split_with_reminder(video, (start, end), i)
    
def splitAll(video1, video2, time_list):
    split_list = []
    cur_video = 0
    time_video = [[0,0], [0,0]]
    for item in time_list:
        if item[0] == 'both':
            if cur_video == 0:
                time_video[0][1] += item[1]
                time_video[1][1] += item[1]
            elif cur_video == 1:
                time_video[0][1] += item[1]
                time_video[1][0] += item[1]
                time_video[1][1] += item[1]
            elif cur_video == 2:
                time_video[0][0] += item[1]
                time_video[0][1] += item[1]
                time_video[1][1] += item[1]
                
        elif item[0] == 1:
            time_video[0][1] += item[1]
            if cur_video == 2:
                split_list.append((cur_video, copy.deepcopy(time_video[cur_video-1])))
            cur_video = 1
        elif item[0] == 2:
            time_video[1][1] += item[1]
            if cur_video == 1:
                split_list.append((cur_video, copy.deepcopy(time_video[cur_video-1])))
            cur_video = 2
            
    split_list.append((cur_video, time_video[cur_video-1]))
    print split_list
    for i in range(len(split_list)):
        item = split_list[i]
        if item[0] == 1:
            start_split(video1, item[1], i) 
        else:
            start_split(video2, item[1], i) 
            

def test_splitAll():
    time_list = eval("[[1, 39.68], ['both', 10], ['both', 10], ['both', 10], ['both', 10], [2, 26.6453], ['both', 10], ['both', 10], ['both', 10], ['both', 10]]")
    splitAll("p124.mp4", "p234.mp4", time_list)

def main():
    test_splitAll()


if __name__ == "__main__":
    main()
