import pyaudio
import numpy as np
import pygame
import random
from project1_classes import rand_circ
from project1_classes import color_square

# define pygame window size
win_height = 600 # set the windows height
win_width = 600 # set the windows width

# define variables for pyaudio stream object
CHUNK = 4096                    # audio samples per frame
FORMAT = pyaudio.paInt16        # bytes per sample
CHANNELS = 1                    # input channels
RATE = 44100                    # samples per second (Hz)

# define variables for onset object
threshold = 10                # input threshold
circ_lst = []                 # define list for circles to be saved in

# define variables for squares
squares_lst = []  # define list for squares to be saved in

# audio input as array
p = pyaudio.PyAudio()                       # create Pyaudio object
stream = p.open(                            # create a stream object with the specified variables:
              format = FORMAT,              # 16 bytes per sample
              channels = CHANNELS,          # 1 input channels (mono)
              rate = RATE,                  # 44100 samples per second
              input = True,                 # specifies this is an input stream
              output = True,                # specifies this is an output stream
              frames_per_buffer = CHUNK     # 4096 audio samples per frame
              )

# start pygame window
pygame.init()                                           # initialize pygame
win = pygame.display.set_mode((win_height, win_width))  # set window size
pygame.display.set_caption('graphic synthesizer')       # set window caption


run = True # set condition by which the game will run (as long as 'run' == True)

while run:                      # start an infinite loop (as long as 'run' == True)

    pygame.time.delay(1)                  # set delay to 0.01 seconds

    for event in pygame.event.get():        # search for events
        if event.type == pygame.QUIT:       # if user exits window
            run = False                     # break the loop

    win.fill((0, 0, 0))                     # update black background

    new_square = color_square((win_height / 2, win_width / 2), # define
                              (win_height/2,win_width/2),
                              (win_height/2,win_width/2),
                              (win_height/2,win_width/2),
                              5)

    squares_lst.append(new_square)


    for place, square in enumerate(squares_lst):   #
        if square.top[1]> 1200:
            squares_lst.pop(place)
        else:
            pygame.draw.polygon(win,
                                (random.randint(100,150),random.randint(100,150),random.randint(100,150)),
                                [new_square.top,new_square.right,new_square.bottom, new_square.left],
                                new_square.line)

        new_square.grow()


    # sound intensity visualization (as shrinking circles)
    data_ = stream.read(CHUNK)                               # get stream as bytes
    data_np = np.frombuffer(data_, dtype=np.int16)           # get stream as np array of ints

    to_draw = False # condition weather to draw or not to draw onset circles.

    if max(data_np) > threshold * 100 : # if onset is above 100 times the threshold
        size_ = 70                     # set circles size to large
        to_draw = True                  # set condition to draw circles to True

    elif max(data_np) > threshold * 20: # if onset is above 20 times the threshold
        size_ = 50                     # set circles size to medium-large
        to_draw = True                  # set condition to draw circles to True

    elif max(data_np) > threshold * 5:  # if onset is above 5 times the threshold
        size_ = 30                     # set circles size to medium-small
        to_draw = True                  # set condition to draw circles to True

    elif max(data_np) > threshold:      # if onset is above the threshold
        size_ = 20                      # set circles size to small
        to_draw = True                  # set condition to draw circles to True

    if to_draw:                         # if condition to drawing circles is True
        new_circ = rand_circ(          # create a circle object
            (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)),   # set circle color
            (random.randint(0, win_width), random.randint(0, win_height)),              # set circle start point
            (size_)                                                                     # set circle size
            )
        circ_lst.append(new_circ)                                                      # append circle to circles list

    for place, circle in enumerate(circ_lst):   # iterate on the circles list
        if circle.size < 1:                     # if a circle is smaller than 1 pixel
            circ_lst.pop(place)                 # remove it
        else:
            pygame.draw.circle(win, circle.color, (circle.start[0], circle.start[1]), circle.size) # else draw it
        circle.shrink()                                                                  # shrink it after drawing

    # sound equalizer plot visualization (as a polygon with the frequency data as points)

    s_point = (-10, win_height+10)                               # set bottom left point of the window as corner
    e_point = (win_width+10, win_height+10)                       # set bottom right  point of the window as corner

    # make lists of tuples with xy coordinates and add them bottom left and bottom right corners.
    # set equalizer threshold by splitting data_np according to the volume intensity
    # reduce from the coordinates a specific number to create each equalizer at a different location

    equalizer_line = list(enumerate(-1 * (data_np/5 - (win_height / 2))))    # make a list of tuples of xy coordinates
    equalizer_line.insert(0, (s_point))                                    # insert a coordinate for bottom left point
    equalizer_line.append(e_point)                                         # insert a coordinate for bottom right point

    pygame.draw.polygon(win, (240, 240, 240), equalizer_line, 3)           # draw line


    pygame.display.update()


pygame.quit()

