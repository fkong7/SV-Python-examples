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
    if kernel_name == 'PolyData':
        print(SolidPolyData.Available())
    elif kernel_name =='OpenCASCADE':
        print(SolidOCCT.Available())
    return Solid.SetKernel(kernel_name)

def test_methods():
    solid = Solid.pySolidModel()
    solid.Methods()

def cylinder(ctr=[1., 1., 1.], axisL=[0.,0.,1.], radius=1., length=1., fn=None):
    cyl=Solid.pySolidModel()
    cyl.Cylinder('cyl',radius,length,ctr,axisL)
    poly=cyl.GetPolyData('cyl_poly',1.)
    if fn is not None:
        Repository.WriteVtkPolyData('cyl_poly','ascii',fn)
    return cyl

def sphere(ctr=[0.,0.,0.], radius=1., fn=None):
    sph = Solid.pySolidModel()
    sph.Sphere('sph', radius, ctr)
    sph.GetPolyData('sph_poly', 1.)
    if fn is not None:
        Repository.WriteVtkPolyData('sph_poly', 'ascii', fn)
    return sph

def ellipsoid(ctr=[1.,1.,1.], axis=[2.,1.,1.], fn=None):
    ellpsd=Solid.pySolidModel()
    ellpsd.Ellipsoid('ellpsd',axis,ctr)
    ellpsd.GetPolyData('ellpsd_poly',1.)
    if fn is not None:
        Repository.WriteVtkPolyData('ellpsd_poly','ascii',fn)
    return ellpsd

def box(ctr=[1.,1.,1.], axis=[2.,1.,1.], fn=None):
    box=Solid.pySolidModel()
    box.Box3d('box',axis,ctr)
    box.GetPolyData('box_poly',1.)
    if fn is not None:
        Repository.WriteVtkPolyData('box_poly','ascii',fn)
    return box
def io_ops(fn):
    #reading a solid from file and write it out
    solid = Solid.pySolidModel()
    solid.ReadNative('read_model', fn)
    if not solid.WriteNative(fn):
        raise RuntimeError("Failed in reading and writing files")

def copy(fn, fn_copy):
    clean_repos()
    solid = cylinder()
    solid.GetBoundaryFaces(80)
    copy = Solid.pySolidModel()
    copy.Copy('cyl', 'cyl_copy')
    copy.GetPolyData('cyl_copy_poly')
    if copy.GetFaceIds() != solid.GetFaceIds():
        raise RuntimeError("Face ids are different, failed in copying")
    solid.WriteNative(fn)
    copy.WriteNative(fn_copy)

def remesh(fn):
    clean_repos()
    assert Solid.GetKernel() == "PolyData", "Only works for PolyData"
    solid = cylinder()
    solid.GetBoundaryFaces(80)
    solid.RemeshFace([1], 0.2)
    solid.WriteNative(fn)

def face_ops_polydata():
    clean_repos()
    assert Solid.GetKernel() == "PolyData", "Only works for PolyData"
    solid = cylinder()
    solid.GetBoundaryFaces(80)
    face_list = solid.GetFaceIds()
    print("Solid face id numbers: ", face_list)
    solid.CombineFaces(1,2)
    face_list_combine = solid.GetFaceIds()
    if face_list_combine != ['1','3']:
        print("Face Ids after combining faces: ", solid.GetFaceIds())
        raise RuntimeError("Failed in combining faces")

    face_list = [3]
    solid.DeleteFaces(face_list)
    if solid.GetFaceIds() != ['1']:
        print("Face ids after removing faces: ", solid.GetFaceIds())
        raise RuntimeError("Failed in deleting faces")
    
    #solid.GetFacePolyData('cyl_face1',1,0.5)
    #Repository.WriteVtkPolyData('cyl_face1','ascii','/Users/fanweikong/Documents/test/cylinderFace1.vtk')
    
def face_ops_occt():
    assert Solid.GetKernel() == "OpenCASCADE", "Only works for OpenCASCADE"
    clean_repos()
    solid = cylinder()
    print("Face Ids of a cylinder: ", solid.GetFaceIds())
    faceList=[2,3]
    solid.DeleteFaces(faceList)
    if solid.GetFaceIds() != ['1']:
        print("Face ids after removing faces: ", solid.GetFaceIds())
        raise RuntimeError("Failed in deleting faces")
    solid.GetPolyData('cyl_after_del_face',0.5)
    print("Face ids after removing caps: ", solid.GetFaceIds())
    #Repository.WriteVtkPolyData('cyl_after_del_face','ascii','/Users/fanweikong/Documents/test/cylinderDelFace.vtk')

def face_blend(fn) :
    assert Solid.GetKernel() == "OpenCASCADE", "Only works for OpenCASCADE"
    clean_repos()
    solid = cylinder()
    solid.CreateEdgeBlend(1, 2, 0.2)
    solid.GetPolyData("blend_poly", 0.)
    solid.WriteNative(fn)

def face_attr():
    assert Solid.GetKernel() == "OpenCASCADE", "Only works for OpenCASCADE"
    clean_repos()
    solid=cylinder()
    print(solid.GetFaceAttr('id',1))
    solid.SetFaceAttr('gdscname','test',1)
    if solid.GetFaceAttr('gdscname',1) != 'test':
        raise RuntimeError("Failed in setting or getting face attributes")

def boolean_ops(mode, fn):
    #Boolean operations between a sphere and a cylinder
    clean_repos()
    cyl = cylinder()
    sph = sphere()
    if mode=='union':
        u=Solid.pySolidModel()
        u.Union('union','sph','cyl','All')
        u.WriteNative(fn)
    elif mode=='subtract':
        s=Solid.pySolidModel()
        s.Subtract('subtract','sph','cyl','All')
        s.WriteNative(fn)
    elif mode=='intersect':
        i=Solid.pySolidModel()
        i.Intersect('intersect','sph','cyl','None')
        i.WriteNative(fn)

if __name__ == '__main__':
    
    fn_dir = '/Users/fanweikong/Documents/test'
    
    #Kernels

    print("******kernel test********")
    try:
        test_kernel('OpenCASCADE')
    except Exception as e: print(e)
    try:
        test_kernel('PolyData')
    except Exception as e: print(e)
    try:
        test_kernel('wrong_name')
    except Exception as e: print(e)
    
    print("******print method test********")

    test_methods()

    # Simple Geomtries
    print("******simple geometry test********")
   
    try:
        print("Creating cylinder")
        poly_fn = os.path.join(fn_dir, "cylinder.vtk")
        cyl = cylinder(fn=poly_fn)
    except Exception as e: print(e)

    try:
        print("Creating sphere")
        poly_fn = os.path.join(fn_dir, "sphere.vtk")
        sph = sphere(fn=poly_fn)
    except Exception as e: print(e)
    

    try:
        print("Creating box")
        poly_fn = os.path.join(fn_dir, "box.vtk")
        box = box(fn=poly_fn)
    except Exception as e: print(e)

    print("******io test********")
    # IO
    try:
        io_ops(poly_fn)
    except Exception as e: print(e)
    
    print("******boolean test********")
    # Boolean
    for mode in ['union', 'subtract', 'intersect']:
        fn = os.path.join(fn_dir, mode+'.vtk')
        try:
            boolean_ops(mode, fn)
        except Exception as e: print(e)

    print("******face operation test - PolyData********")
    try:
        face_ops_polydata()
    except Exception as e: print(e)
    
    print("******copy test********")
    try:
        poly_fn = os.path.join(fn_dir, "cylinder.vtk")
        poly_copy = os.path.join(fn_dir, "cylinder_copy.vtk")
        copy(poly_fn, poly_copy)
    except Exception as e: print(e)
    
    print("******remesh test********")

    try:
        poly_fn = os.path.join(fn_dir, "remesh_cyl.vtk")
        remesh(poly_fn)
    except Exception as e: print(e)

    print("******OCCT face operation test********")
    try:
        #only availabl in OCCT
        Solid.SetKernel('OpenCASCADE')
        face_attr()
    except Exception as e: print(e)
    try:
        face_ops_occt()
    except Exception as e: print(e)
    try:
        poly_fn = os.path.join(fn_dir, "blend.stl")
        face_blend(poly_fn)
    except Exception as e: print(e)

# Never worked, output planar geometry
#    try:
#        poly_fn = os.path.join(fn_dir, "ellipsoid.vtk")
#        ellpsd = ellipsoid(fn=poly_fn)
#    except Exception as e: print(e)

