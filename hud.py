#!/usr/bin/env python

import os, sys, random
import pygame

def display_init():
    disp_no = os.getenv('DISPLAY')
    if disp_no:
    #if False:
        #print "I'm running under X display = {0}".format(disp_no)
        size = 320, 240
        screen = pygame.display.set_mode(size)
    else:
        drivers = ['directfb', 'fbcon', 'svgalib']
        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)

            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue

            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        size = pygame.display.Info().current_w, pygame.display.Info().current_h
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    return screen, size

def get_line_coords (pitch, screen_width, screen_height, ahrs_center):
    if pitch == 0:
        length = screen_width*.6
    elif (pitch%10) == 0:
        length = screen_width*.4
    elif (pitch%5) == 0:
        length = screen_width*.2

    ahrs_center_x, ahrs_center_y = ahrs_center

    px_per_deg_y = screen_height / 60

    start_x = ahrs_center_x - (length / 2)
    end_x = ahrs_center_x + (length / 2)
    y = (px_per_deg_y * pitch) + ahrs_center_y

    return [[start_x, y], [end_x, y]]

def main():
    screen, screen_size = display_init()
    width, height = screen_size

    WHITE =   (255, 255, 255)

    roll = 0.0
    pitch = 0.0

    ahrs_bg = pygame.Surface((width*2, height*2))
    ahrs_bg_width = ahrs_bg.get_width()
    ahrs_bg_height = ahrs_bg.get_height()
    ahrs_bg_center = (ahrs_bg_width/2, ahrs_bg_height/2)

    for l in range(-60, 60, 5):
        pygame.draw.lines(ahrs_bg, WHITE, False, get_line_coords(l, width, height, ahrs_bg_center), 2)

    done = False
    clock = pygame.time.Clock()

    while not done:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        print "Roll:  {:.1f}".format(roll)
        print "Pitch: {:.1f}".format(pitch)
        print ""

        pitch_offset = height / 60 * pitch

        ahrs = ahrs_bg.copy()

        ahrs.scroll(dy=int(pitch_offset))

        ahrs = pygame.transform.rotate(ahrs, roll)

        top_left = (-(ahrs.get_width() - width)/2, -(ahrs.get_height() - height)/2)
        screen.blit(ahrs, top_left)

        pygame.display.flip()

        roll = roll + random.normalvariate(0, 0.5)
        pitch = pitch + random.normalvariate(0, 0.5)

    pygame.quit()

if __name__ == '__main__':
    sys.exit(main())

# vi: modeline tabstop=8 expandtab shiftwidth=4 softtabstop=4 syntax=python
