import cadquery as cq
from Helpers import show

plane = cq.Workplane ( "XY" )
box = plane.box( 50 ,50 , 4 )

mounting_plate = box.faces(">Z").rect( 40 ,40 ).vertices() .\
    cboreHole( diameter=3 , cboreDiameter= 5 , cboreDepth=2 )

plate1 = cq.Workplane ( "YZ" ).workplane( offset=20 ).move( xDist = -15,
                                    yDist=2 )
plate1 = plate1.lineTo( 15 ,2 ).lineTo( 15,40 ).threePointArc( (0,50), (-15 ,40)
                                                ).close().\
      extrude(-5).faces(">X").workplane().move(xDist=0 , yDist=10).hole(10 , depth =5)


plate2 = cq.Workplane ( "YZ" ).workplane( offset=-20 ).move( xDist = -15,
                                    yDist=2 )
plate2 =  plate2.lineTo( 15 ,2 ).lineTo( 15,40 ).threePointArc( (0,50), (-15 ,40)
                                                ).close().\
extrude(5).faces(">X").workplane().move(xDist=0 , yDist=10).hole(10 , depth =5)

cylinder_mounting_plate = mounting_plate.combineSolids( plate1 ).combineSolids( plate2 )
show ( cylinder_mounting_plate )

# mounting_plate.combineSolids(  )