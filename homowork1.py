import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use("TkAgg")  # GUI 交互
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号 "-" 显示为方块的问题


class InteractiveGrid3D:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_title("3D 交互网格绘制\n按Enter循环选择点\n方向键移动点，空格升高/Alt降低")

        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)

        # 当前选中的点索引
        self.current_point_index = 0
        self.move_speed = 0.5  # 移动速度

        # 初始化 4x4 点阵
        self.grid_size = 4
        x_vals = np.linspace(-5, 5, self.grid_size)
        y_vals = np.linspace(-5, 5, self.grid_size)
        self.points = np.array([[x, y, 0] for x in x_vals for y in y_vals])

        # 初始化散点图
        self.scatter = self.ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2],
                                       c="red", s=50)

        # 初始化网格线
        self.lines = []
        for i in range(self.grid_size):
            # 横向连接每行点
            row_indices = range(i * self.grid_size, (i + 1) * self.grid_size)
            line, = self.ax.plot(self.points[row_indices, 0],
                                 self.points[row_indices, 1],
                                 self.points[row_indices, 2], c="blue")
            self.lines.append(line)

        for j in range(self.grid_size):
            # 纵向连接每列点
            col_indices = range(j, self.grid_size ** 2, self.grid_size)
            line, = self.ax.plot(self.points[col_indices, 0],
                                 self.points[col_indices, 1],
                                 self.points[col_indices, 2], c="blue")
            self.lines.append(line)

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
        self.coord_text.set_text(
            f'当前点 #{self.current_point_index}\nX: {point[0]:.2f}\nY: {point[1]:.2f}\nZ: {point[2]:.2f}')

    def on_key_press(self, event):
        """键盘事件处理"""
        if event.key == 'enter':
            # 循环选择下一个点
            self.current_point_index = (self.current_point_index + 1) % len(self.points)

        elif event.key == 'left':
            self.points[self.current_point_index][0] -= self.move_speed
        elif event.key == 'right':
            self.points[self.current_point_index][0] += self.move_speed
        elif event.key == 'up':
            self.points[self.current_point_index][1] += self.move_speed
        elif event.key == 'down':
            self.points[self.current_point_index][1] -= self.move_speed
        elif event.key == ' ':  # 空格键
            self.points[self.current_point_index][2] += self.move_speed
        elif event.key == 'alt':
            self.points[self.current_point_index][2] -= self.move_speed

        # 限制坐标范围
        self.points[self.current_point_index] = np.clip(self.points[self.current_point_index], -10, 10)

        # 更新图形
        self.update_plot()

    def update_plot(self):
        """更新图形，重新绘制散点和网格"""
        self.scatter._offsets3d = (self.points[:, 0], self.points[:, 1], self.points[:, 2])

        for i in range(self.grid_size):
            row_indices = range(i * self.grid_size, (i + 1) * self.grid_size)
            self.lines[i].set_data(self.points[row_indices, 0], self.points[row_indices, 1])
            self.lines[i].set_3d_properties(self.points[row_indices, 2])

        for j in range(self.grid_size):
            col_indices = range(j, self.grid_size ** 2, self.grid_size)
            self.lines[self.grid_size + j].set_data(self.points[col_indices, 0], self.points[col_indices, 1])
            self.lines[self.grid_size + j].set_3d_properties(self.points[col_indices, 2])

        current_point = self.points[self.current_point_index]
        self.highlight_scatter._offsets3d = ([current_point[0]], [current_point[1]], [current_point[2]])

        self.update_coord_text()

        self.fig.canvas.draw_idle()

    def run(self):
        self.update_plot()
        plt.show()


if __name__ == "__main__":
    app = InteractiveGrid3D()
    app.run()