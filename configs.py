from numpy import deg2rad

l1,l2,l3 = 0.2,1.5,1.6
p1,p2,p3 = 0.5,1.2,0
a0,(a1,a2,a3) = deg2rad(90), deg2rad( (30,0,0) )

webot_mantis = (
    ( (l1,l2,l3),(l1,l2,l3),(l1,l2,l3),(l1,l2,l3) ),
    ( (p1,p2,p3),(-p1,p2,p3),(-p1,-p2,p3),(p1,-p2,p3) ),
    ( (a1,a2,a3),(2*a0-a1,a2,a3),(a1+a0*2,a2,a3),(a0*4-a1,a2,a3) )
)

l1,l2,l3 = 3,4,8
p1,p2,p3 = 2.5,4.5,2
a1,a2,a3 = deg2rad( (30,0,0) )

my_quad = (
    ( (l1,l2,l3),(l1,l2,l3),(l1,l2,l3),(l1,l2,l3) ),
    ( (p1,p2,p3),(-p1,p2,p3),(-p1,-p2,p3),(p1,-p2,p3) ),
    ( (a1,a2,a3),(2*a0-a1,a2,a3),(a1+a0*2,a2,a3),(a0*4-a1,a2,a3) )
)

default = webot_mantis
