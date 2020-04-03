import os
from sv import *

"""
Example meshing functinos using SV Python API
Functions in this file were tested using SV demo data
"""

def clean_repos():
    objs = Repository.List()
    for name in objs:
        try:
            Repository.Delete(name)
        except Exception as e: print(e)

def new_object(name, meshName=None, solidName=None):
    msh=MeshObject.pyMeshObject()
    msh.NewObject(name)
    if not Repository.Exists(name):
        raise RuntimeError("Error creating mesh object")
    if meshName is not None:
        load = msh.LoadMesh(meshName)
        if not load:
            raise RuntimeError("Error loading mesh")
    if solidName is not None:
        load = msh.LoadModel(solidName)
        if not load:
            raise RuntimeError("Error loading model")
    return msh

def boundary_layer(name, fn, wall_list, global_edge_size, bl_ops, fns_out):
    clean_repos()
    msh = new_object(name, solidName = fn)
    msh.GetBoundaryFaces(80.)
    msh.SetWalls(wall_list)
    #Create new mesh
    msh.NewMesh()
    print(msh.GetModelFaceInfo())
    mesh_ops = {
            'SurfaceMeshFlag': True,
            'VolumeMeshFlag': True,
            'GlobalEdgeSize': global_edge_size,
            'MeshWallFirst': True,
            'NoMerge':True,
            'NoBisect': True,
            'Epsilon': 1e-8,
            'Optimization': 3,
            'QualityRatio': 1.4,
    }
    
    for key in mesh_ops:
        msh.SetMeshOptions(key,[mesh_ops[key]])
    msh.SetBoundaryLayer(bl_ops['type'], bl_ops['id'], bl_ops['side'],bl_ops['num_lyr'], bl_ops['H'])
    msh.GenerateMesh()
    msh.Print()

    poly_fn, ug_fn = fns_out
    if mesh_ops['SurfaceMeshFlag']:
        msh.GetPolyData(poly_fn)
        Repository.WriteVtkPolyData(poly_fn, 'ascii', poly_fn)
    if mesh_ops['VolumeMeshFlag']:
        msh.GetUnstructuredGrid(ug_fn)
        Repository.WriteVtkUnstructuredGrid(ug_fn, 'ascii', ug_fn)
    return msh

def size_function(name, fn, cap_source_list, cap_target_list, wall_list, mesh_ops, fns_out):
    """
    Attemping radius based meshing, not working yet
    """
    clean_repos()
    solid = Solid.pySolidModel()
    solid.ReadNative('surface', fn)
    solid.GetPolyData('surface_p')
    solid.GetBoundaryFaces(45)
    VMTKUtils.Centerlines('surface_p', cap_source_list, cap_target_list, 'lines', 'voronoi')
    VMTKUtils.Distancetocenterlines('surface_p', 'lines', 'distance')

    msh = new_object(name)
    msh.SetVtkPolyData('distance')
    msh.GetBoundaryFaces(50.)
    #msh.SetWalls(wall_list)
    msh.NewMesh()
    mesh_ops = {
            'SurfaceMeshFlag': True,
            'VolumeMeshFlag': True,
            'GlobalEdgeSize': 0.5,
            'LocalEdgeSize': [1, 0.1, 2, 0.3, 3, 0.3, 4, 0.3],
    }

    for key in mesh_ops:
        msh.SetMeshOptions(key, mesh_ops[key] if type(mesh_ops[key])==list else [mesh_ops[key]] )
    msh.SetSizeFunctionBasedMesh(0.5, 'DistanceToCenterlines')
    #msh.SetSizeFunctionBasedMesh(0.5, 'MeshSizingFunction')
    print("sizing function")
    msh.Print()
    
    poly_fn, ug_fn = fns_out
    if mesh_ops['SurfaceMeshFlag']:
        msh.GetPolyData(poly_fn)
        Repository.WriteVtkPolyData(poly_fn, 'ascii', poly_fn)
    if mesh_ops['VolumeMeshFlag']:
        msh.GetUnstructuredGrid(ug_fn)
        Repository.WriteVtkUnstructuredGrid(ug_fn, 'ascii', ug_fn)
    return msh

def local_size_function(name, fn, global_edge_size, local_edge_size_list, fns_out, bl_ops=None):
    clean_repos()
    print(local_edge_size_list)
    
    msh = new_object(name, solidName=fn)
    msh.GetBoundaryFaces(50.)
    print(msh.GetModelFaceInfo())
    msh.NewMesh()
    mesh_ops = {
            'SurfaceMeshFlag': True,
            'VolumeMeshFlag': True,
            'GlobalEdgeSize': global_edge_size,
            'LocalEdgeSize': local_edge_size_list,
    }
    

    for key in mesh_ops:
        msh.SetMeshOptions(key, mesh_ops[key] if type(mesh_ops[key])==list else [mesh_ops[key]] )
    msh.SetSizeFunctionBasedMesh(0.5, 'MeshSizingFunction')
    if bl_ops is not None:
        msh.SetWalls(bl_ops['wall'])
        msh.SetBoundaryLayer(bl_ops['type'], bl_ops['id'], bl_ops['side'],bl_ops['num_lyr'], bl_ops['H'])
    msh.GenerateMesh()
    msh.Print()
    
    poly_fn, ug_fn = fns_out
    if mesh_ops['SurfaceMeshFlag']:
        msh.GetPolyData(poly_fn)
        Repository.WriteVtkPolyData(poly_fn, 'ascii', poly_fn)
    if mesh_ops['VolumeMeshFlag']:
        msh.GetUnstructuredGrid(ug_fn)
        Repository.WriteVtkUnstructuredGrid(ug_fn, 'ascii', ug_fn)
    return msh



solid_fn = '/Users/fanweikong/Downloads/SVDemoProject/Models/demo.vtp'
mesh_fn = '/Users/fanweikong/Downloads/SVDemoProject/Meshes/demo_test.vtu'
out_dir = '/Users/fanweikong/Downloads/SVDemoProject/test'
MeshObject.SetKernel('TetGen')
Solid.SetKernel('PolyData')
try:
    os.makedirs(out_dir)
except Exception as e: print(e)

mesh_ops = {
        'SurfaceMeshFlag': True,
        'VolumeMeshFlag': True,
        'GlobalEdgeSize': 0.5,
        'MeshWallFirst': True,
        'NoMerge':True,
        'NoBisect': True,
        'Epsilon': 1e-8,
        'Optimization': 3,
        'QualityRatio': 1.4,
}
try:
    print("*********size based function meshing****")
    poly_fn = os.path.join(out_dir, 'sf_surface.vtk')
    ug_fn = os.path.join(out_dir, 'sf_vol.vtk')
    local_size_function('sf_test', solid_fn, 1., [1, 0.15, 2, 0.3, 3, 0.6, 4, 0.6], (poly_fn, ug_fn))
    #Combine with boundary layer meshing:
    #local_size_function('sf_test', solid_fn, 1., [1, 0.15, 2, 0.3, 3, 0.6, 4, 0.6], (poly_fn, ug_fn), 
    #        {'wall':[1], 'type':0, 'id':0, 'side':0, 'num_lyr': 3, 'H':[0.3,0.6, 0.8]})
except Exception as e: print(e)
#try:
#    print("*********boundary layer *****")
#    poly_fn = os.path.join(out_dir, 'bl_surface.vtk')
#    ug_fn = os.path.join(out_dir, 'bl_rfn_vol.vtk')
#    msh = boundary_layer('bl_test', solid_fn, [1], 0.5,  
#            {'type':0, 'id':0, 'side':0, 'num_lyr': 2, 'H':[0.1,0.3]}, (poly_fn, ug_fn))
#except Exception as e: print(e)


