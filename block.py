import cadquery as cq
from Helpers import show

color = (   74, 35, 90 , 0.5 )

plane1 = cq.Workplane( "XY" )
plane2 = cq.Workplane( "YZ" )

(x,y) = p1 = ( 20 , 0 )
(x,y) = r1 = ( x+15 , y-15 )
(x,y) = r2 = (x-15 , y-15 )
(x,y) = p2 = (x-20 , y )

block = plane1.lineTo( *p1 ).threePointArc( r1 , r2 ).lineTo( *p2 )
(x,y) = p3 = (x , y-10 )
(x,y) = p4 = ( x-25 , y )
(x,y) = p5 = ( x , y+40 )

block = block.lineTo( *p3 ).lineTo( *p4 ).lineTo(*p5).close().moveTo( 20 ,-15 ).circle(5 ).extrude(-10).clean()
(x,y) = p6 = ( p3[0]-10 , p3[1] )
(x,y) = p7 = (x , y + 30 )
(x,y) = p8 = ( x-15 , y)

block = block .faces( ">Z" ).moveTo( 0 ,0  ).lineTo( *p3 ).lineTo(*p6).lineTo( *p7 ).lineTo(*p8).lineTo(*p5).\
    close().extrude( 50 )

obj2:cq.Workplane  = plane2.workplane( offset=-10 )
obj2 = obj2.moveTo( -10,0 ).lineTo( -40,0 ).lineTo( -10,50 ).close() .extrude( -15 , clean= True )
block = block.combineSolids( obj2 )

show ( block.combineSolids( block.mirror("YZ" , (-25,0,0)) ) , color )


























