#!/usr/bin/env python

import os, sys, random
import pygame

class Vehicle(object):
    def __init__(self, data_source="random"):
        self.data_source = data_source
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.alt = 0
        self.airspeed = 0

    def get_orientation(self):
        self.update_orientation()
        return {'roll':     self.roll,
                'pitch':    self.pitch,
                'yaw':      self.yaw,
                'alt':      self.alt,
                'airspeed': self.airspeed}

    def set_orientation(self, roll=None, pitch=None, yaw=None, alt=None, airspeed=None):
        if roll != None:
            self.roll = roll

        if pitch != None:
            self.pitch = pitch

        if yaw != None:
            self.yaw = yaw

        if alt != None:
            self.alt = alt

        if airspeed != None:
            self.airspeed = airspeed

    def update_orientation(self):
        if self.data_source == "random":
            r = self.roll + random.normalvariate(0, 0.5)
            p = self.pitch + random.normalvariate(0, 0.5)
            self.set_orientation(roll=r, pitch=p)

        elif self.data_source == "manual":
            r = float(raw_input('Roll? '))
            p = float(raw_input('Pitch? '))
            self.set_orientation(roll=r, pitch=p)

        else:
            raise ValueError

def display_init():
    pygame.init()
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

def get_line_coords(pitch, screen_width, screen_height, ahrs_center):
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
    y = (px_per_deg_y * -pitch) + ahrs_center_y

    return [[start_x, y], [end_x, y]]

def main():
    screen, screen_size = display_init()
    width, height = screen_size
    pygame.mouse.set_visible(False)

    WHITE = (255, 255, 255)

    font = pygame.font.SysFont(None, int(height/20))

    v = Vehicle(data_source="random")

    ahrs_bg = pygame.Surface((width*2, height*2))
    ahrs_bg_width = ahrs_bg.get_width()
    ahrs_bg_height = ahrs_bg.get_height()
    ahrs_bg_center = (ahrs_bg_width/2, ahrs_bg_height/2)

    for l in range(-60, 60, 5):
        line_coords = get_line_coords(l, width, height, ahrs_bg_center)
        pygame.draw.lines(ahrs_bg, WHITE, False, line_coords, 2)

        if l != 0 and l%10 == 0:
            text = font.render(str(l), False, WHITE)
            text_width, text_height = text.get_size()
            left = int(line_coords[0][0]) - (text_width + int(width/100))
            top = int(line_coords[0][1]) - text_height / 2
            ahrs_bg.blit(text, (left, top))

    done = False
    clock = pygame.time.Clock()

    while not done:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        o = v.get_orientation()
        roll = o['roll']
        pitch = o['pitch']

        print "Roll:  {:.1f}".format(roll)
        print "Pitch: {:.1f}".format(pitch)
        print ""

        pitch_offset = height / 60 * pitch

        ahrs = ahrs_bg.copy()

        ahrs.scroll(dy=int(pitch_offset))

        ahrs = pygame.transform.rotate(ahrs, roll)

        top_left = (-(ahrs.get_width() - width)/2, -(ahrs.get_height() - height)/2)
        screen.blit(ahrs, top_left)

        pygame.draw.lines(screen, WHITE, False, [[0, height/2], [10, height/2]], 2)
        pygame.draw.lines(screen, WHITE, False, [[width-10, height/2], [width, height/2]], 2)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    sys.exit(main())

# vi: modeline tabstop=8 expandtab shiftwidth=4 softtabstop=4 syntax=python
