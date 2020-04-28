### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Gravity objects

from math import sqrt
from code.pyIgnitionAlpha import keyframes, interpolate
import random

UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL = 1000.0  # Well, Newton got one to make it less stupidly large.


def RandomiseStrength(base, range):
    return base + (float(random.randrange(int(-range * 100), int(range * 100))) / 100.0)


class DirectedGravity:
    def __init__(self, strength=0.0, strengthrandrange=0.0, direction=[0, 1]):
        self.initstrength = strength
        self.strength = strength
        self.strengthrandrange = strengthrandrange
        directionmag = sqrt(direction[0] ** 2 + direction[1] ** 2)
        self.direction = [direction[0] / directionmag, direction[1] / directionmag]

        self.keyframes = []
        self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.direction)
        self.curframe = 0
        self.curkey = 0
        self.nextkey = 1

    def Update(self):
        if self.nextkey >= len(self.keyframes):
            pass

        else:
            if self.curframe > self.keyframes[self.nextkey].frame:
                self.curkey += 1
                self.nextkey += 1

            if self.nextkey < len(self.keyframes):
                self.initstrength = interpolate.LinearInterpolateKeyframes(self.curframe,
                                                                           self.keyframes[self.curkey].frame,
                                                                           self.keyframes[self.nextkey].frame,
                                                                           self.keyframes[self.curkey].strength,
                                                                           self.keyframes[self.nextkey].strength)
                self.direction = [
                    interpolate.LinearInterpolateKeyframes(self.curframe, self.keyframes[self.curkey].frame,
                                                           self.keyframes[self.nextkey].frame,
                                                           self.keyframes[self.curkey].direction[0],
                                                           self.keyframes[self.nextkey].direction[0]),
                    interpolate.LinearInterpolateKeyframes(self.curframe, self.keyframes[self.curkey].frame,
                                                           self.keyframes[self.nextkey].frame,
                                                           self.keyframes[self.curkey].direction[1],
                                                           self.keyframes[self.nextkey].direction[1])]

        if self.strengthrandrange != 0.0:
            self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)

        self.curframe = self.curframe + 1

    def GetForce(self, pos):
        force = [self.strength * self.direction[0], self.strength * self.direction[1]]

        return force

    def CreateKeyframe(self, frame, strength=0.0, strengthrandrange=0.0, direction=[0, 1]):
        newframe = keyframes.DirectedGravityKeyframe(frame, strength, strengthrandrange, direction)
        self.keyframes.append(newframe)
        self.keyframes = sorted(self.keyframes, key=lambda keyframe: keyframe.frame)


class PointGravity:
    def __init__(self, strength=0.0, strengthrandrange=0.0, pos=(0, 0)):
        self.initstrength = strength
        self.strength = strength
        self.strengthrandrange = strengthrandrange
        self.pos = pos

        self.keyframes = []
        self.CreateKeyframe(0, self.strength, self.strengthrandrange, self.pos)
        self.curframe = 0
        self.curkey = 0
        self.nextkey = 1

    def Update(self):
        if self.nextkey >= len(self.keyframes):
            pass  # We've reached the end of this object's keyframes

        else:
            if self.curframe > self.keyframes[self.nextkey].frame:
                self.curkey += 1
                self.nextkey += 1

            if self.nextkey < len(self.keyframes):
                self.initstrength = interpolate.LinearInterpolateKeyframes(self.curframe,
                                                                           self.keyframes[self.curkey].frame,
                                                                           self.keyframes[self.nextkey].frame,
                                                                           self.keyframes[self.curkey].strength,
                                                                           self.keyframes[self.nextkey].strength)
                self.pos = [interpolate.LinearInterpolateKeyframes(self.curframe, self.keyframes[self.curkey].frame,
                                                                   self.keyframes[self.nextkey].frame,
                                                                   self.keyframes[self.curkey].pos[0],
                                                                   self.keyframes[self.nextkey].pos[0]),
                            interpolate.LinearInterpolateKeyframes(self.curframe, self.keyframes[self.curkey].frame,
                                                                   self.keyframes[self.nextkey].frame,
                                                                   self.keyframes[self.curkey].pos[1],
                                                                   self.keyframes[self.nextkey].pos[1])]

        if self.strengthrandrange != 0.0:
            self.strength = RandomiseStrength(self.initstrength, self.strengthrandrange)

        self.curframe = self.curframe + 1

    def GetForce(self, pos):
        distsquared = (pow(float(pos[0] - self.pos[0]), 2.0) + pow(float(pos[1] - self.pos[1]), 2.0))
        if distsquared == 0.0:
            return [0.0, 0.0]

        forcemag = (self.strength * UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL) / (distsquared)

        # Calculate normal vector from pos to the gravity point and multiply by force magnitude to find force vector
        dist = sqrt(distsquared)
        dx = float(self.pos[0] - pos[0]) / dist
        dy = float(self.pos[1] - pos[1]) / dist

        force = [forcemag * dx, forcemag * dy]

        return force

    def GetMaxForce(self):
        return self.strength * UNIVERSAL_CONSTANT_OF_MAKE_GRAVITY_LESS_STUPIDLY_SMALL

    def CreateKeyframe(self, frame, strength=0.0, strengthrandrange=0.0, pos=(0, 0)):
        newframe = keyframes.PointGravityKeyframe(frame, strength, strengthrandrange, pos)
        self.keyframes.append(newframe)
        self.keyframes = sorted(self.keyframes, key=lambda keyframe: keyframe.frame)
