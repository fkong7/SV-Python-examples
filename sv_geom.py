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
def geom_local_constrain_smooth():
    out_dir = os.path.join(os.path.dirname(__file__), 'test')
    try:
        os.makedirs(out_dir)
    except Exception as e: print(e)
    objs = Repository.List()
    for name in objs:
        try:
            Repository.Delete(name)
        except Exception as e: print(e)
    
    # create geometry: two intersected cylinders
    Solid.SetKernel('PolyData')
    cyl_1 = Solid.pySolidModel()
    cyl_1.Cylinder('cyl',1.,10.,[0,0,0],[0,0,1])
    cyl_2 = Solid.pySolidModel()
    cyl_2.Cylinder('cyl2', 0.6, 10., [0,5,0], [0,1,0])

    union = Solid.pySolidModel()
    union.Union('u', 'cyl', 'cyl2', 'All')
    union.GetBoundaryFaces(90)
    union.GetPolyData('poly1', 2)
    
    # face remeshing
    MeshUtil.Remesh('poly1', 'poly2', 0.3, 0.4)
    MeshUtil.Remesh('poly2', 'poly3', 0.3, 0.4)
    output_1 = os.path.join(out_dir, 'cyl.vtk')
    
    # set sphere constrain args: name , dst_name, radius, center, array name, datatype(0=point, 1=cell)
    Geom.Set_array_for_local_op_sphere('poly3', 'smth', 3, [0,0,0],'LocalOpsArray', 0)
    Geom.Set_array_for_local_op_sphere('smth', 'smth2', 3, [0,0,0],'LocalOpsArray', 1)
    # check arrays on surfaces 
    Repository.WriteVtkPolyData('smth2', 'ascii', output_1)
    # local constrained smoothing: name, dst_name, iter, relax_factor, numcgsolves, pt array name, cell array name
    Geom.Local_constrain_smooth('smth2', 'smth3', 5, 0.8, 30, 'LocalOpsArray','LocalOpsArray')
    output = os.path.join(out_dir, 'geom_test_local_smooth.vtk')
    Repository.WriteVtkPolyData('smth3', 'ascii', output)


if __name__ == '__main__':
    geom_local_constrain_smooth()




