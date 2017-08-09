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

def main():
    screen, screen_size = display_init()
    width, height = screen_size

    BLACK =   (  0,   0,   0)
    WHITE =   (255, 255, 255)
    BLUE =    (  0,   0, 255)
    GREEN =   (  0, 255,   0)
    RED =     (255,   0,   0)
    GROUND =  ( 84,  53,  10)
    SKY =     (  9,  79, 252)

    miniature_airplane = {'color': WHITE,
                          'coords': [[width/6*2,  height/2],
                                     [width/2-10, height/2],
                                     [width / 2,  height/2+20],
                                     [width/2+10, height/2],
                                     [width/6*4,  height/2]],
                          'width': 2}

    static_ahrs_bkgnd = pygame.transform.smoothscale(pygame.image.load("ahrsbkgnd.png").convert(),
                                                     (width*3, height*3))

    roll = 0.0
    pitch = 0.0

    done = False
    clock = pygame.time.Clock()

    while not done:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        print "Roll:  {:.1f}".format(roll)
        print "Pitch: {:.1f}".format(pitch)
        print ""

        pitch_offset = height / 90 * pitch

        ahrs = static_ahrs_bkgnd.copy()

        ahrs.scroll(dy=int(pitch_offset))

        ahrs = pygame.transform.rotate(ahrs, roll)

        top_left = (-(ahrs.get_width() - width)/2, -(ahrs.get_height() - height)/2)
        screen.blit(ahrs, top_left)

        for l in [miniature_airplane]:
            pygame.draw.lines(screen, l['color'], False, l['coords'], l['width'])

        pygame.display.flip()

        roll = roll + random.normalvariate(0, 0.5)
        pitch = pitch + random.normalvariate(0, 0.1)

    pygame.quit()

if __name__ == '__main__':
    sys.exit(main())

# vi: modeline tabstop=8 expandtab shiftwidth=4 softtabstop=4 syntax=python
