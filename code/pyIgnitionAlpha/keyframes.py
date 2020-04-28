### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
#
# Keyframe objects


class Keyframe:
    def __init__(self, frame = 0):
        self.frame = frame


class ParticleKeyframe(Keyframe):
    def __init__(self, frame = 0, colour = (0, 0, 0), radius = 0.0, length = 0.0):
        Keyframe.__init__(self, frame)
        self.colour = colour
        self.radius = radius
        self.length = length


class SourceKeyframe(Keyframe):
    def __init__(self, frame = 0, pos = (0, 0), initspeed = 0.0, initdirection = 0.0, initspeedrandrange = 0.0, initdirectionrandrange = 0.0, particlesperframe = 0):
        Keyframe.__init__(self, frame)
        self.pos = pos
        self.initspeed = initspeed
        self.initdirection = initdirection
        self.initspeedrandrange = initspeedrandrange
        self.initdirectionrandrange = initdirectionrandrange
        self.particlesperframe = particlesperframe


class GravityKeyframe(Keyframe):
	def __init__(self, frame = 0, strength = 0.0, strengthrandrange = 0.0):
		Keyframe.__init__(self, frame)
		self.strength = strength
		self.strengthrandrange = strengthrandrange
		

class DirectedGravityKeyframe(GravityKeyframe):
    def __init__(self, frame = 0, strength = 0.0, strengthrandrange = 0.0, direction = [0.0, 0.0]):
        GravityKeyframe.__init__(self, frame, strength, strengthrandrange)
        self.direction = direction


class PointGravityKeyframe(GravityKeyframe):
    def __init__(self, frame = 0, strength = 0.0, strengthrandrange = 0.0, pos = [0, 0]):
        GravityKeyframe.__init__(self, frame, strength, strengthrandrange)
        self.pos = pos
