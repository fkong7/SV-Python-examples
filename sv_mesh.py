# Copyright (c) Stanford University, The Regents of the University of
#               California, and others.
#
# All Rights Reserved.
#
# See Copyright-SimVascular.txt for additional details.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# SV Python API Testing Script
# Author: Fanwei Kong (fanwei_kong@berkeley.edu)

import os
from sv import *

def clean_repos():
    objs = Repository.List()
    for name in objs:
        try:
            Repository.Delete(name)
        except Exception as e: print(e)

def test_kernel(kernel_name):
    if kernel_name == 'TetGen':
        print(MeshTetgen.Available())
    return MeshObject.SetKernel(kernel_name)

def test_methods():
    MeshObject.ListMethods()

def new_object(name, meshName=None, solidName=None):
    msh=MeshObject.pyMeshObject()
    msh.NewObject(name,meshName,solidName)
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

def set_kernel(msh, kernel_name):
    if kernel_name == 'PolyData':
        print(SolidPolyData.Available())
    elif kernel_name =='OpenCASCADE':
        print(SolidOCCT.Available())
    msh.SetSolidKernel(kernel_name)

    if msh.GetKernel() != kernel_name:
        raise RuntimeError("Error getting mesh solid kernel, kernel is ", msh.GetKernel())

def test_get_solid(msh, out_fn):
    out = msh.GetSolid(out_fn)
    if not out:
        raise RunTimeError("Error getting solid")
    Repository.WriteVtkPolyData(out_fn, 'ascii', out_fn)
  

def test_get_vtk_objects(msh, poly_fn, face_fn, mesh_fn):
    msh.GetPolyData(poly_fn)
    msh.GetUnstructuredGrid(mesh_fn)
    msh.GetFacePolyData(face_fn, 1)
    print(msh.GetModelFaceInfo())
    Repository.WriteVtkPolyData(poly_fn, 'ascii', poly_fn)
    Repository.WriteVtkUnstructuredGrid(mesh_fn, 'ascii', mesh_fn)
    Repository.WriteVtkPolyData(face_fn, 'ascii', face_fn)

def mesh(name, fn, args, fns_out):
    clean_repos()
    msh=MeshObject.pyMeshObject()
    msh.NewObject(name)
    #Load Model
    msh.LoadModel(fn)
    msh.GetBoundaryFaces(80.)
    #Create new mesh
    msh.NewMesh()
    print(msh.GetModelFaceInfo())
    
    for key in args:
        msh.SetMeshOptions(key,[args[key]])
    try:
        msh.SetSizeFunctionBasedMesh(args['MeshSizingFunction'],'MeshSizingFunction')
    except Exception as e: print(e)

    msh.GenerateMesh()
    msh.Print()

    poly_fn, ug_fn = fns_out
    if args['SurfaceMeshFlag']:
        msh.GetPolyData(poly_fn)
        Repository.WriteVtkPolyData(poly_fn, 'ascii', poly_fn)
    if args['VolumeMeshFlag']:
        msh.GetUnstructuredGrid(ug_fn)
        Repository.WriteVtkUnstructuredGrid(ug_fn, 'ascii', ug_fn)
    return msh
def sphere_refine(name, fn, args, sph_rfn_ops, fns_out):
    clean_repos()
    msh=MeshObject.pyMeshObject()
    msh.NewObject(name)
    #Load Model
    msh.LoadModel(fn)
    msh.GetBoundaryFaces(80.)
    #Create new mesh
    msh.NewMesh()
    print(msh.GetModelFaceInfo())
    
    for key in args:
        msh.SetMeshOptions(key,[args[key]])
    try:
        msh.SetSizeFunctionBasedMesh(args['MeshSizingFunction'],'MeshSizingFunction')
    except Exception as e: print(e)
    msh.SetSphereRefinement(sph_rfn_ops['size'], 
            sph_rfn_ops['rad'],
            sph_rfn_ops['center'])
    msh.GenerateMesh()
    msh.Print()

    poly_fn, ug_fn = fns_out
    if args['SurfaceMeshFlag']:
        msh.GetPolyData(poly_fn)
        Repository.WriteVtkPolyData(poly_fn, 'ascii', poly_fn)
    if args['VolumeMeshFlag']:
        msh.GetUnstructuredGrid(ug_fn)
        Repository.WriteVtkUnstructuredGrid(ug_fn, 'ascii', ug_fn)
    return msh

def cylinder_refine(name, fn, args, cyl_rfn_ops, fns_out):
    clean_repos()
    msh=MeshObject.pyMeshObject()
    msh.NewObject(name)
    #Load Model
    msh.LoadModel(fn)
    msh.GetBoundaryFaces(80.)
    #Create new mesh
    msh.NewMesh()
    print(msh.GetModelFaceInfo())
    
    for key in args:
        msh.SetMeshOptions(key,[args[key]])
    try:
        msh.SetSizeFunctionBasedMesh(args['MeshSizingFunction'],'MeshSizingFunction')
    except Exception as e: print(e)
    msh.SetCylinderRefinement(cyl_rfn_ops['size'], 
            cyl_rfn_ops['rad'],
            cyl_rfn_ops['length'],
            cyl_rfn_ops['center'],
            cyl_rfn_ops['nrm'])
    msh.GenerateMesh()
    msh.Print()

    poly_fn, ug_fn = fns_out
    if args['SurfaceMeshFlag']:
        msh.GetPolyData(poly_fn)
        Repository.WriteVtkPolyData(poly_fn, 'ascii', poly_fn)
    if args['VolumeMeshFlag']:
        msh.GetUnstructuredGrid(ug_fn)
        Repository.WriteVtkUnstructuredGrid(ug_fn, 'ascii', ug_fn)
    return msh
    
def boundary_layer(name, fn, args, bl_ops, fns_out):
    clean_repos()
    msh=MeshObject.pyMeshObject()
    msh.NewObject(name)
    #Load Model
    msh.LoadModel(fn)
    msh.GetBoundaryFaces(80.)
    msh.SetWalls([2])
    #Create new mesh
    msh.NewMesh()
    print(msh.GetModelFaceInfo())
    
    for key in args:
        msh.SetMeshOptions(key,[args[key]])
    try:
        msh.SetSizeFunctionBasedMesh(args['MeshSizingFunction'],'MeshSizingFunction')
    except Exception as e: print(e)
    msh.SetBoundaryLayer(bl_ops['type'], bl_ops['id'], bl_ops['side'],bl_ops['num_lyr'], bl_ops['H'])
    msh.GenerateMesh()
    msh.Print()

    poly_fn, ug_fn = fns_out
    if args['SurfaceMeshFlag']:
        msh.GetPolyData(poly_fn)
        Repository.WriteVtkPolyData(poly_fn, 'ascii', poly_fn)
    if args['VolumeMeshFlag']:
        msh.GetUnstructuredGrid(ug_fn)
        Repository.WriteVtkUnstructuredGrid(ug_fn, 'ascii', ug_fn)
    return msh

if __name__ == '__main__':
    solid_fn = '/Users/fanweikong/SV-Python-examples/cylinder.vtp'
    mesh_fn = '/Users/fanweikong/SV-Python-examples/cylinder.vtu'
    out_dir = '/Users/fanweikong/Documents/test'
    
    print("*********mesh kernel*********")
    test_kernel('TetGen')
    print("*********mesh method*********")
    test_methods()
    try:
        print("********* new object*********")
        msh = new_object('cylinder', meshName=mesh_fn, solidName=solid_fn)
    except Exception as e: print(e)
    try:
        print("*********solid kernel********")
        set_kernel(msh, 'PolyData')
    except Exception as e: print(e)
    try:
        print("*********get solid **********")
        Solid.SetKernel('PolyData')
        out_fn = os.path.join(out_dir, 'cylinder.vtk')
        test_get_solid(msh, out_fn)
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
            'QualityRatio': 1.4
    }
    try:
        print("*********simple mesh**********")
        poly_fn = os.path.join(out_dir, 'mesh_surface.vtk')
        ug_fn = os.path.join(out_dir, 'mesh_vol.vtk')
        msh = mesh('cylinder', solid_fn, mesh_ops, (poly_fn, ug_fn))
    except Exception as e: print(e)


    try:
        print("**********spherical refine *****")
        poly_fn = os.path.join(out_dir, 'sph_rfn_surface.vtk')
        ug_fn = os.path.join(out_dir, 'sph_rfn_vol.vtk')
        msh = sphere_refine('sph_refine', solid_fn, mesh_ops, 
            {'size':0.2, 'rad':1, 'center':[0,0,0]}, (poly_fn, ug_fn))
    except Exception as e: print(e)
    
    try:
        print("**********cylinder refine *****")
        poly_fn = os.path.join(out_dir, 'cyl_rfn_surface.vtk')
        ug_fn = os.path.join(out_dir, 'cyl_rfn_vol.vtk')
        msh = cylinder_refine('cyl_refine', solid_fn, mesh_ops, 
                {'size':0.2, 'rad':1, 'length': 10, 'center':[0,0,0], 'nrm':[0,0,1]}, (poly_fn, ug_fn))
    except Exception as e: print(e)
    
    try:
        print("*********get vtk objects*****")
        poly_fn = os.path.join(out_dir, 'poly.vtk')
        face_fn = os.path.join(out_dir, 'face.vtk')
        mesh_fn = os.path.join(out_dir, 'vol.vtk')
        test_get_vtk_objects(msh, poly_fn, face_fn, mesh_fn)
    except Exception as e: print(e)
    
    try:
        print("*********boundary layer *****")
        poly_fn = os.path.join(out_dir, 'bl_surface.vtk')
        ug_fn = os.path.join(out_dir, 'bl_rfn_vol.vtk')
        msh = boundary_layer('sph_refine', solid_fn, mesh_ops, 
                {'type':0, 'id':0, 'side':0, 'num_lyr': 2, 'H':[0.1,0.3]}, (poly_fn, ug_fn))
    except Exception as e: print(e)
