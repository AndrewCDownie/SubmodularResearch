from shapely.geometry import Point


def get_cover_func(f,domain):
    #Takes function and create a distritized intergral coverage function f(x) = int(F(x),U(s))
    print(f)
    
class submodular_functions:
    def __init__(self,*args,**kwargs):
        print(kwargs)
        self.r = 1
        if "r" in kwargs.keys():
            self.r = kwargs['r']
    
    def coverage(self,S):
        r = self.r
        polygons = []
        if len(S) == 0:
            return 0
        for p in S:
            polygons.append(Point(p[0],p[1]).buffer(r))
        total_area = 0
        union_poly = polygons[0]
        for poly in polygons:
            total_area += poly.area
            union_poly = union_poly.union(poly)
        return union_poly.area

        




def coverage(points,r):
    polygons = []
    if len(points) == 0:
        return 0
    for p in points:
        polygons.append(Point(p[0],p[1]).buffer(r))
    total_area = 0
    union_poly = polygons[0]
    for poly in polygons:
        total_area += poly.area
        union_poly = union_poly.union(poly)
    return union_poly.area



def  main():
    sfs = submodular_functions(r = 10)
    print(sfs.coverage([(0,0),(0,10)]))

if __name__ =="__main__":
    main()
