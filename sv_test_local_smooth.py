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




