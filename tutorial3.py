import cadquery as cq
from Helpers import show
from math import  pi, sin, cos, tan

color1 = (99, 75, 114,0.5)
color2 = ( 255,0,0,0.5)

r1 = (130/2)
r2 = (100/2)
arcX,arcY = r1* cos(pi/6), r1*sin(pi/6)

def cutRectOfPolarArray( part:cq.Workplane ,point , rotateAnglesList ) :
    for rotateAngle in rotateAnglesList :
        part = part.rotate( (0 , 0 , 0), (0 , 0 ,1), rotateAngle )
        part = part.moveTo( *point ).rect(10,15).cutThruAll(clean= True)
        part = part.rotate( (0 , 0 , 0), (0 , 0 ,1), -rotateAngle )
    return  part

part_sub1 = cq.Workplane ( "XY" )
part_sub1 = part_sub1.circle( radius=31 ).extrude( 53, both= False )
part_sub1 = part_sub1.faces(">Z").first().circle(31).workplane(offset=12).circle(25).loft()

part_sub2 = cq.Workplane ( "XY" ).lineTo( -arcX , -arcY ).threePointArc( (0 ,r1) , (arcX , -arcY) ).close()
part_sub2 = part_sub2.extrude( -20 , clean=True ,combine=True ).faces(">Z")
part_sub2 = cutRectOfPolarArray( part_sub2 , ( -r2*cos(pi/2) , ( r2*sin(pi/2) + 7.5) ) , [ 0 , 60 ,-60 ] )
part_sub2 = part_sub2.faces( ">Z" ).moveTo(  0 , 0 ).circle(12.5).cutThruAll()

part_sub1 = part_sub1.faces (">Z") .circle(20).cutBlind( -26 ).faces(">Z").circle(12.5).cutThruAll()

rot_part_sub1 = part_sub1.rotate( ( 0 , 0 , 0) , ( 1 , 0 , 0 ) , 90 ).moveTo( 0, -13 ).workplane( offset=-(65-31)).circle(3).\
            cutBlind(-18.5)
rot_part_sub1 = rot_part_sub1.rotate( (0,0,0) , ( 1,0,0) , -90 )

final_part = part_sub2.combineSolids ( rot_part_sub1 )
# show ( part_sub2 , color2 )
# show ( part_sub1, color1 )
# show ( rot_part_sub1 , color2 )
show ( final_part , color1 )
