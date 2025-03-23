from geomdl import BSpline

# Create the curve instance
crv = BSpline.Curve()

# Set degree
crv.degree = 3

# Set control points
crv.ctrlpts = [[1, 0], [1, 1], [0, 1],[0,0],[1,-0.5],[0.5,0.5]]

# Set knot vector
crv.knotvector = [0, 0, 0,0.25,0.5,0.75,1,1,1,1]

crv.evaluate()

# Import Matplotlib visualization module
from geomdl.visualization import VisVTK as visModule


# Set the visualization component of the curve
crv.vis = visModule.VisCurve2D()

print(crv.vis.vconf.keypress_callback)

# Plot the curve
crv.render(animte=True)

# 不用看geomdl的document，直接看py代码。关于geomdl的计算细节、可视化的细节，可以直接查看geomdl的安装目录的py文件，例如：vis.py, VisVTK.py, abstract.py, BSpline.py,vtk_helpers.py。必要时，可以通过扩展VisVTK的兄弟模块来实现对vtk的绝对控制。(搜索keypress_callback于VisVTK, vtk_helpers.py中函数create_render_window的第二个参数callbacks参数的用法)