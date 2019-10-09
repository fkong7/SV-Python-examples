from sv import *
def geom_local_constrain_smooth():
    Solid.SetKernel('PolyData')
    cyl_1 = Solid.pySolidModel()
    cyl_1.Cylinder('cyl',1.,10.,[0,0,0],[0,0,1])
    cyl_2 = Solid.pySolidModel()
    cyl_2.Cylinder('cyl2', 0.6, 10., [0,5,0], [0,1,0])

    union = Solid.pySolidModel()
    union.Union('u', 'cyl', 'cyl2', 'All')
    union.GetBoundaryFaces(90)
    union.GetPolyData('poly1', 2)
    
    MeshUtil.Remesh('poly1', 'poly2', 0.3, 0.4)
    MeshUtil.Remesh('poly2', 'poly3', 0.3, 0.4)
    output_1 = '/Users/fanweikong/Downloads/cyl.vtk'
    Repository.WriteVtkPolyData('poly3', 'ascii', output_1)
    

    Geom.Set_array_for_local_op_sphere('poly3', 'smth', 3, [0,0,0])
    print("ok")
    Geom.Local_constrain_smooth('smth', 'smth2', 5, 0.8)
    print("ok")
    output = '/Users/fanweikong/Downloads/geomTestLocalSmooth.vtk'
    Repository.WriteVtkPolyData('smth2', 'ascii', output)


if __name__ == '__main__':
    geom_local_constrain_smooth()




