from sv import *

def mesh_spherical_refinement():
    MeshObject.SetKernel('TetGen')
    a=MeshObject.pyMeshObject()

    solidName='/Users/fanweikong/Documents/LV/extrudeOutput/EndoExtend26r.vtk'
    a.NewObject('LV')
    a.LoadModel(solidName)
    a.NewMesh()
    
    
    a.SetMeshOptions('SurfaceMeshFlag',[1])
    a.SetMeshOptions('GlobalEdgeSize',[1.5])
    a.SetMeshOptions('LocalEdgeSize',[1.5,1.3])
    a.SetMeshOptions('VolumeMeshFlag',[0])
    a.SetSizeFunctionBasedMesh(1.5,'MeshSizingFunction')
    a.SetSphereRefinement(0.1,15.0,[7.6,-19.34,-18.8])
    a.GenerateMesh()
    
    a.GetPolyData('LVSph3')
    
    outMeshu='/Users/fanweikong/Downloads/meshTestNewSph.vtk'
    Repository.WriteVtkPolyData('LVSph3','ascii',outMeshu)

