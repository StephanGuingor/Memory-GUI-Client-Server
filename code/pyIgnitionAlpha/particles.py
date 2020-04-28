### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Particle and ParticleSource objects


from code.pyIgnitionAlpha import keyframes, interpolate
import random, math, pygame

DRAWTYPE_POINT = 0
DRAWTYPE_CIRCLE = 1
DRAWTYPE_LINE = 2
DRAWTYPE_SCALELINE = 3
DRAWTYPE_BUBBLE = 4
DRAWTYPE_IMAGE = 5


class Particle:
    def __init__(self, initpos, velocity, life, drawtype=0, colour=(0, 0, 0), radius=0.0, length=0.0, image=None,
                 keyframes=[]):
        self.pos = initpos
        self.velocity = velocity
        self.life = life
        self.colour = colour
        self.radius = radius
        self.length = length
        self.image = image
        self.drawtype = drawtype

        self.keyframes = []
        self.keyframes.extend(keyframes[:])
        self.CreateKeyframe(0, self.colour, self.radius, self.length)
        self.curframe = 0
        self.curkey = 0
        self.nextkey = 1

        self.alive = True

    def Update(self):
        self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]

        if self.curframe >= self.life:
            self.alive = False

        if self.nextkey < len(self.keyframes):
            if self.curframe > self.keyframes[self.nextkey].frame:
                self.curkey += 1
                self.nextkey += 1

            if self.nextkey < len(self.keyframes):
                self.colour = (interpolate.LinearInterpolateKeyframes(self.curframe, self.keyframes[self.curkey].frame,
                                                                      self.keyframes[self.nextkey].frame,
                                                                      self.keyframes[self.curkey].colour[0],
                                                                      self.keyframes[self.nextkey].colour[0]),
                               interpolate.LinearInterpolateKeyframes(self.curframe, self.keyframes[self.curkey].frame,
                                                                      self.keyframes[self.nextkey].frame,
                                                                      self.keyframes[self.curkey].colour[1],
                                                                      self.keyframes[self.nextkey].colour[1]),
                               interpolate.LinearInterpolateKeyframes(self.curframe, self.keyframes[self.curkey].frame,
                                                                      self.keyframes[self.nextkey].frame,
                                                                      self.keyframes[self.curkey].colour[2],
                                                                      self.keyframes[self.nextkey].colour[2]))
                if self.drawtype == DRAWTYPE_CIRCLE or self.drawtype == DRAWTYPE_BUBBLE:  # Interpolate radius for circles and bubles
                    self.radius = interpolate.LinearInterpolateKeyframes(self.curframe,
                                                                         self.keyframes[self.curkey].frame,
                                                                         self.keyframes[self.nextkey].frame,
                                                                         self.keyframes[self.curkey].radius,
                                                                         self.keyframes[self.nextkey].radius)
                if self.drawtype == DRAWTYPE_LINE:  # Interpolate length for lines
                    self.length = interpolate.LinearInterpolateKeyframes(self.curframe,
                                                                         self.keyframes[self.curkey].frame,
                                                                         self.keyframes[self.nextkey].frame,
                                                                         self.keyframes[self.curkey].length,
                                                                         self.keyframes[self.nextkey].length)

        self.curframe = self.curframe + 1

    def Draw(self, display):
        if self.drawtype == DRAWTYPE_POINT:  # Point
            pygame.draw.circle(display, self.colour, (int(round(self.pos[0], 0)), int(round(self.pos[1], 0))),
                               0)  # CHANGED HERE

        elif self.drawtype == DRAWTYPE_CIRCLE:  # Circle
            pygame.draw.circle(display, self.colour, self.pos, self.radius)

        elif self.drawtype == DRAWTYPE_LINE:
            if self.length == 0.0:
                pygame.draw.circle(display, self.colour, self.pos, 0)

            else:
                velocitymagoverlength = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2) / self.length
                linevec = [(self.velocity[0] / velocitymagoverlength), (self.velocity[1] / velocitymagoverlength)]
                endpoint = [self.pos[0] + linevec[0], self.pos[1] + linevec[1]]
                pygame.draw.aaline(display, self.colour, self.pos, endpoint)

        elif self.drawtype == DRAWTYPE_SCALELINE:  # Scaling line (scales with velocity)
            endpoint = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]
            pygame.draw.aaline(display, self.colour, self.pos, endpoint)

        elif self.drawtype == DRAWTYPE_BUBBLE:  # Bubble
            if self.radius >= 1.0:
                pygame.draw.circle(display, self.colour, self.pos, self.radius, 1)
            else:  # Pygame won't draw circles with thickness < radius, so if radius is smaller than one don't bother trying to set thickness
                pygame.draw.circle(display, self.colour, self.pos, self.radius)

        elif self.drawtype == DRAWTYPE_IMAGE:  # Image
            size = self.image.get_size()
            display.blit(self.image, (self.pos[0] - size[1], self.pos[1] - size[1]))

    def CreateKeyframe(self, frame, colour=(0, 0, 0), radius=0.0, length=0.0):
        newframe = keyframes.ParticleKeyframe(frame, colour, radius, length)
        self.keyframes.append(newframe)
        self.keyframes = sorted(self.keyframes, key=lambda keyframe: keyframe.frame)


class ParticleSource:
    def __init__(self, parenteffect, pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange,
                 particlesperframe, particlelife, drawtype=0, colour=(0, 0, 0), radius=0.0, length=0.0, image=None):
        self.parenteffect = parenteffect
        self.pos = pos
        self.initspeed = initspeed
        self.initdirection = initdirection
        self.initspeedrandrange = initspeedrandrange
        self.initdirectionrandrange = initdirectionrandrange
        self.particlesperframe = particlesperframe
        self.particlelife = particlelife
        self.colour = colour
        self.drawtype = drawtype
        self.radius = radius
        self.length = length
        self.image = image

        self.keyframes = []
        self.CreateKeyframe(0, self.pos, self.initspeed, self.initdirection, self.initspeedrandrange,
                            self.initdirectionrandrange, self.particlesperframe)

        self.particlekeyframes = []
        self.curframe = 0
        self.curkey = 0
        self.nextkey = 1

    def Update(self):
        if self.nextkey < len(self.keyframes):
            if self.curframe > self.keyframes[self.nextkey].frame:
                self.curkey += 1
                self.nextkey += 1

            if self.nextkey < len(self.keyframes):
                self.pos = [interpolate.LinearInterpolateKeyframes(self.curframe, self.keyframes[self.curkey].frame,
                                                                   self.keyframes[self.nextkey].frame,
                                                                   self.keyframes[self.curkey].pos[0],
                                                                   self.keyframes[self.nextkey].pos[0]),
                            interpolate.LinearInterpolateKeyframes(self.curframe, self.keyframes[self.curkey].frame,
                                                                   self.keyframes[self.nextkey].frame,
                                                                   self.keyframes[self.curkey].pos[1],
                                                                   self.keyframes[self.nextkey].pos[1])]
                self.initspeed = interpolate.LinearInterpolateKeyframes(self.curframe,
                                                                        self.keyframes[self.curkey].frame,
                                                                        self.keyframes[self.nextkey].frame,
                                                                        self.keyframes[self.curkey].initspeed,
                                                                        self.keyframes[self.nextkey].initspeed)
                self.initdirection = interpolate.LinearInterpolateKeyframes(self.curframe,
                                                                            self.keyframes[self.curkey].frame,
                                                                            self.keyframes[self.nextkey].frame,
                                                                            self.keyframes[self.curkey].initdirection,
                                                                            self.keyframes[self.nextkey].initdirection)
                self.initspeedrandrange = interpolate.LinearInterpolateKeyframes(self.curframe,
                                                                                 self.keyframes[self.curkey].frame,
                                                                                 self.keyframes[self.nextkey].frame,
                                                                                 self.keyframes[
                                                                                     self.curkey].initspeedrandrange,
                                                                                 self.keyframes[
                                                                                     self.nextkey].initspeedrandrange)
                self.initdirectionrandrange = interpolate.LinearInterpolateKeyframes(self.curframe,
                                                                                     self.keyframes[self.curkey].frame,
                                                                                     self.keyframes[self.nextkey].frame,
                                                                                     self.keyframes[
                                                                                         self.curkey].initdirectionrandrange,
                                                                                     self.keyframes[
                                                                                         self.nextkey].initdirectionrandrange)
                self.particlesperframe = interpolate.LinearInterpolateKeyframes(self.curframe,
                                                                                self.keyframes[self.curkey].frame,
                                                                                self.keyframes[self.nextkey].frame,
                                                                                self.keyframes[
                                                                                    self.curkey].particlesperframe,
                                                                                self.keyframes[
                                                                                    self.nextkey].particlesperframe)

        particlesperframe = self.particlesperframe
        for i in range(0, particlesperframe):
            self.CreateParticle()

        self.curframe = self.curframe + 1

    def CreateParticle(self):
        if self.initspeedrandrange != 0.0:
            speed = self.initspeed + (float(
                random.randrange(int(-self.initspeedrandrange * 100.0), int(self.initspeedrandrange * 100.0))) / 100.0)
        else:
            speed = self.initspeed
        if self.initdirectionrandrange != 0.0:
            direction = self.initdirection + (float(random.randrange(int(-self.initdirectionrandrange * 100.0),
                                                                     int(self.initdirectionrandrange * 100.0))) / 100.0)
        else:
            direction = self.initdirection
        velocity = [speed * math.sin(direction), -speed * math.cos(direction)]
        newparticle = Particle(initpos=self.pos, velocity=velocity, life=self.particlelife, drawtype=self.drawtype,
                               colour=self.colour, radius=self.radius, length=self.length, image=self.image,
                               keyframes=self.particlekeyframes)
        self.parenteffect.AddParticle(newparticle)

    def CreateKeyframe(self, frame, pos=(0, 0), initspeed=0.0, initdirection=0.0, initspeedrandrange=0.0,
                       initdirectionrandrange=0.0, particlesperframe=0):
        newframe = keyframes.SourceKeyframe(frame, pos, initspeed, initdirection, initspeedrandrange,
                                            initdirectionrandrange, particlesperframe)
        self.keyframes.append(newframe)
        self.keyframes = sorted(self.keyframes, key=lambda keyframe: keyframe.frame)

    def CreateParticleKeyframe(self, frame, colour=(0, 0, 0), radius=0.0, length=0.0):
        newframe = keyframes.ParticleKeyframe(frame, colour, radius, length)
        self.particlekeyframes.append(newframe)
