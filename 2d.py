import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.use("TkAgg")#GUI 交互
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号 "-" 显示为方块的问题


class InteractivePolyline2D:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("交互折线绘制 (左键添加/拖拽, 右键删除)")


        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        self.points = []  # 存储点的坐标列表
        self.epsilon = 0.25  # 选点范围
        self.dragging_index = None  # 当前拖拽的点索引

        # 初始化散点图和折线
        self.scatter = self.ax.scatter([], [], c="red", s=50)
        (self.line,) = self.ax.plot([], [], c="blue", linestyle="-", marker="o")

        # 连接鼠标事件
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_click(self, event):
        """鼠标点击事件：左键添加/拖拽点，右键删除点"""
        if event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata
        idx = self.get_nearest_point_index(x, y)

        if event.button == 1:  # 左键：新增点或拖拽点
            if idx is None:
                self.points.append([x, y])  # 直接添加新点
            else:
                self.dragging_index = idx  # 选中已有点，进入拖拽模式
            self.update_plot()  # 无论如何，都要刷新图像

        elif event.button == 3:  # 右键：删除已有点
            if idx is not None:
                self.points.pop(idx)
                self.update_plot()

    def on_release(self, event):
        """鼠标释放，停止拖拽"""
        if event.button == 1:
            self.dragging_index = None

    def on_motion(self, event):
        """鼠标移动事件：拖拽已选中的点"""
        if self.dragging_index is not None and event.inaxes == self.ax:
            self.points[self.dragging_index] = [event.xdata, event.ydata]
            self.update_plot()

    def get_nearest_point_index(self, x, y):
        """判断鼠标是否点击到已有点，返回索引，否则返回 None"""
        if not self.points:
            return None
        pts_arr = np.array(self.points)
        dist = np.sqrt((pts_arr[:, 0] - x) ** 2 + (pts_arr[:, 1] - y) ** 2)
        idx_min = np.argmin(dist)
        return idx_min if dist[idx_min] < self.epsilon else None

    def update_plot(self):
        """更新图形，重新绘制散点和折线"""
        if self.points:
            pts_arr = np.array(self.points)
            self.scatter.set_offsets(pts_arr)  # 更新散点
            self.line.set_data(pts_arr[:, 0], pts_arr[:, 1])  # 更新折线
        else:
            self.scatter.set_offsets([])
            self.line.set_data([], [])

        self.fig.canvas.draw_idle()  # 触发绘图刷新

    def run(self):
        plt.show()


if __name__ == "__main__":
    app = InteractivePolyline2D()
    app.run()
