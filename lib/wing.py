#!python

__author__ = "Curtis L. Olson < curtolson {at} flightgear {dot} org >"
__url__ = "http://gallinazo.flightgear.org"
__version__ = "1.0"
__license__ = "GPL v2"


import copy
import math
import svgwrite

import airfoil
import layout


class Rib:
    def __init__(self):
        self.thickness = 0.0625
        self.material = "balsa"
        self.contour = None
        self.pos = (0.0, 0.0, 0.0)
        self.sweep = 0.0
        self.placed = False


class Wing:

    def __init__(self):
        self.root = None
        self.tip = None
        self.root_chord = 10.0
        self.tip_chord = 0.0
        self.root_yscale = 1.0
        self.tip_yscale = 1.0
        self.span = 30.0
        self.steps = 10
        self.twist = 0.0
        self.sweep = 0.0 # angle @ 25% chord line, in degrees 
        self.units = "in"
        self.right_ribs = []
        self.left_ribs = []

    def load_airfoils(self, root, tip = None):
        self.root = airfoil.Airfoil(root, 1000, True)
        if tip:
            self.tip = airfoil.Airfoil(tip, 1000, True)

    def make_rib(self, airfoil, chord, lat_dist, twist, label ):
        result = Rib()
        result.contour = copy.deepcopy(airfoil)
        # scale and position
        result.contour.scale(chord, chord)
        result.contour.fit(500, 0.002)
        result.contour.move(-0.25*chord, 0.0)
        # add label (before rotate)
        posx = 0.0
        ty = result.contour.simple_interp(result.contour.top, posx)
        by = result.contour.simple_interp(result.contour.bottom, posx)
        posy = by + (ty - by) / 2.0
        result.contour.add_label( posx, posy, 14, 0, label )
        # do rotate
        result.contour.rotate(twist)
        # compute plan position
        sweep_offset = lat_dist * math.tan(math.radians(self.sweep))
        #print self.sweep
        #print sweep_offset
        result.contour.move(sweep_offset, 0.0)
        result.pos = (lat_dist, sweep_offset, 0.0)
        result.sweep = self.sweep

        return result

    def build(self):
        if self.steps <= 0:
            return
        dp = 1.0 / self.steps
        for p in range(0, self.steps+1):
            print p

            percent = p * dp

            # generate airfoil
            if not self.tip:
                af = self.root
            else:
                af = airfoil.blend(self.root, self.tip, percent)

            # compute rib chord
            if self.tip_chord < 0.01:
                chord = self.root_chord
            else:
                chord = self.root_chord*(1.0-percent) + self.tip_chord*percent

            # compute placement parameters
            lat_dist = self.span * percent
            twist = self.twist * percent

            # make the ribs
            label = 'WR' + str(p+1) 
            rib = self.make_rib(af, chord, lat_dist, twist, label)
            self.right_ribs.append(rib)

            label = 'WL' + str(p+1)
            rib = self.make_rib(af, chord, -lat_dist, twist, label)
            self.left_ribs.append(rib)

    def layout_parts(self, basename, width_in, height_in, margin_in):
        l = layout.Layout( basename + '-wing-parts', width_in, height_in, margin_in )
        for rib in self.right_ribs:
            rib.placed = l.draw_part_demo(rib.contour)
        for rib in self.left_ribs:
            rib.placed = l.draw_part_demo(rib.contour)
        l.save()

    def layout_plans(self, basename, width_in, height_in):
        sheet = layout.Sheet( basename + '-wing', width_in, height_in )
        yoffset = (height_in - self.span) * 0.5
        #print yoffset

        # determine "x" extent of ribs
        minx = 0
        maxx = 0
        for rib in self.right_ribs:
            bounds = rib.contour.get_bounds()
            if bounds[0][0] < minx:
                minx = bounds[0][0]
            if bounds[1][0] > maxx:
                maxx = bounds[1][0]
        #print (minx, maxx)
        dx = maxx - minx
        xmargin = (width_in - 2*dx) / 3.0
        #print "xmargin = " + str(xmargin)

        # right wing
        planoffset = (xmargin - minx, height_in - yoffset, -1)
        #print planoffset
        for rib in self.right_ribs:
            rib.placed = sheet.draw_part_top(planoffset, rib.contour, rib.pos, "1px", "red")

        # left wing
        planoffset = ((width_in - xmargin) - dx - minx, yoffset, 1)
        #print planoffset
        for rib in self.left_ribs:
            rib.placed = sheet.draw_part_top(planoffset, rib.contour, rib.pos, "1px", "red")
        sheet.save()
