import cadquery as cq
import sys, os, math
import numpy as np
from cadquery import exporters

cq_show_object = show_object

show_object = lambda part : cq_show_object(part,
                options = {"alpha":0.5})

def cyl_mtg_plate_create(
        outer_radius, inner_radius, bh,
        bw, mirror_center, hole_radius
    ):

    plane = cq.Workplane("XY")

    bwh = bw / 2
    hypotenuse = hp = math.sqrt((bh ** 2) + (bwh ** 2))

    base_plate_length = bl =  int(1.3*(bw))
    base_plate_breadth = bb =int(1.3*(2*(mirror_center)))
    base_plate_thickness = bt = int(0.25*bh)

    outer_circle = plane.circle(radius=outer_radius)\
        .extrude(20)

    part1 = outer_circle.faces("<Z").workplane()\
        .circle(radius=inner_radius).cutThruAll().clean()

    # show_object(part1)
    # θ

    tan_points_at_zero = (lambda r, x0: ((r**2)/x0,\
            (r/x0)*(math.sqrt(x0**2-(r**2)))))\
            (outer_radius, hypotenuse)


    tan_points = (np.array([
                [bh/hp, -bwh/hp], #cosθ, -sinθ
                [bwh/hp, bh/hp]   #sinθ , cosθ
            ])@np.array(tan_points_at_zero)).tolist()


    tan_point_x, tan_point_y = tan_points

    part2 = cq.Workplane("XY").workplane(offset=5)\
        .lineTo(bh, bwh, forConstruction=True).lineTo(tan_point_x, tan_point_y)\
        .threePointArc((outer_radius, 0), (tan_point_x, -tan_point_y))\
        .lineTo(bh, -bwh).close().extrude(10)

    # show_object(part2)


    part = part1.combineSolids(part2)
    part_mirror = part.mirror("XY",(0, 0, mirror_center))
    show_object([part, part_mirror])


    work_plane2 = cq.Workplane("YZ").workplane(offset=bh)

    def get_push_points(z_offset, length, breadth, circle_rad):
        x_points = [((length*i)/2) + (-i*1.3*circle_rad) for i in [1,-1]]
        y_points = [((breadth * i) / 2) + (-i * 1.3 * circle_rad) for i in [1, -1]]
        return [( x, y+z_offset)  for x in x_points for y in y_points]

    base_plate = work_plane2.moveTo(0, mirror_center).rect( bl, bb)\
        .pushPoints(get_push_points(mirror_center, bl, bb, hole_radius))\
        .circle(hole_radius).extrude(bt)

    final_part = part.combineSolids(part_mirror).combineSolids(base_plate)\
        .clean()

    show_object(final_part)

outer_radius = 60 / 2
inner_radius = 35 / 2

bracket_height = bh = 100
bracket_width = bw = 150
mirror_center = 30
hole_radius = 8

cyl_mtg_plate_create(outer_radius, inner_radius, bracket_height,\
        bracket_width, mirror_center, hole_radius)