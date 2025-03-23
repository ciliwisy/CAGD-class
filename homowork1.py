import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use("TkAgg")  # GUI 交互
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号 "-" 显示为方块的问题


class InteractivePolyline3D:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_title("3D 交互折线绘制\n按Enter循环选择点\n方向键移动点，空格升高/Alt降低")

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)

        # 当前选中的点索引
        self.current_point_index = 0
        self.move_speed = 0.5  # 移动速度

        # 初始化 4x4 点阵
        self.points = np.array([[x, y, 0] for x in np.linspace(-5, 5, 4) for y in np.linspace(-5, 5, 4)])

        # 初始化散点图和折线
        self.scatter = self.ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2], 
                                     c="red", s=50)
        self.line, = self.ax.plot(self.points[:, 0], self.points[:, 1], self.points[:, 2], 
                                 c="blue", linestyle="-", marker="o")
        
        # 高亮显示当前选中的点
        self.highlight_scatter = self.ax.scatter([], [], [], c="yellow", s=100)

        # 添加坐标文本显示
        self.coord_text = self.ax.text2D(0.02, 0.98, '', transform=self.ax.transAxes)

        # 添加网格线以便于观察
        self.ax.grid(True)

        # 连接键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def update_coord_text(self):
        """更新坐标显示文本"""
        point = self.points[self.current_point_index]
        self.coord_text.set_text(f'当前点 #{self.current_point_index}\nX: {point[0]:.2f}\nY: {point[1]:.2f}\nZ: {point[2]:.2f}')

    def on_key_press(self, event):
        """键盘事件处理"""
        if event.key == 'enter':
            # 循环选择下一个点
            self.current_point_index = (self.current_point_index + 1) % len(self.points)
        
        elif event.key == 'left':
            # 向左移动
            self.points[self.current_point_index][0] -= self.move_speed
        elif event.key == 'right':
            # 向右移动
            self.points[self.current_point_index][0] += self.move_speed
        elif event.key == 'up':
            # 向前移动
            self.points[self.current_point_index][1] += self.move_speed
        elif event.key == 'down':
            # 向后移动
            self.points[self.current_point_index][1] -= self.move_speed
        elif event.key == ' ':  # 空格键
            # 增加高度
            self.points[self.current_point_index][2] += self.move_speed
        elif event.key == 'alt':
            # 降低高度
            self.points[self.current_point_index][2] -= self.move_speed

        # 限制坐标范围
        self.points[self.current_point_index] = np.clip(self.points[self.current_point_index], -10, 10)
        
        # 更新图形
        self.update_plot()

    def update_plot(self):
        """更新图形，重新绘制散点和折线"""
        # 更新所有点
        self.scatter._offsets3d = (self.points[:, 0], self.points[:, 1], self.points[:, 2])
        self.line.set_data(self.points[:, 0], self.points[:, 1])
        self.line.set_3d_properties(self.points[:, 2])
        
        # 更新高亮点
        current_point = self.points[self.current_point_index]
        self.highlight_scatter._offsets3d = ([current_point[0]], [current_point[1]], [current_point[2]])
        
        # 更新坐标显示
        self.update_coord_text()
        
        self.fig.canvas.draw_idle()

    def run(self):
        # 初始化高亮显示第一个点和坐标
        self.update_plot()
        plt.show()


if __name__ == "__main__":
    app = InteractivePolyline3D()
    app.run()
