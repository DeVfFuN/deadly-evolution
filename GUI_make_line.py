import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseButton
import os


class LineDrawer:  #позволяет создать собственную линию параметров среды
    def __init__(self):
        self.x_data = []
        self.y_data = []
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'b-')  # Линия для отображения
        self.ax.set_xlim(0, 2000)  # Пример значений, можно настроить
        self.ax.set_ylim(0, 1000)
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.cid_move = self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def on_click(self, event):
        if event.button == MouseButton.LEFT and event.inaxes:
            self.x_data.append(event.xdata)
            self.y_data.append(event.ydata)
            self.update_line()

    def on_move(self, event):
        if event.button == MouseButton.LEFT and event.inaxes:
            self.x_data.append(event.xdata)
            self.y_data.append(event.ydata)
            self.update_line()

    def update_line(self):
        self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()

    def on_key_press(self, event):
        if event.key == 's':  # Клавиша для сохранения
            self.save_data()

    def save_data(self):
        if len(self.x_data) == 0:
            print("No data to save.")
            return

        x_min, x_max = int(np.floor(min(self.x_data))), int(np.ceil(max(self.x_data)))
        y_dict = {}
        for x in range(x_min, x_max + 1):
            if x in self.x_data:
                y_dict[x] = self.y_data[self.x_data.index(x)]
            else:
                idx = np.searchsorted(self.x_data, x)
                if 0 < idx < len(self.x_data):
                    x1, x2 = self.x_data[idx - 1], self.x_data[idx]
                    y1, y2 = self.y_data[idx - 1], self.y_data[idx]
                    y = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
                    y_dict[x] = y

        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'line_data_a.txt')

        with open(file_path, 'w') as f:
            for x in sorted(y_dict.keys()):
                f.write(f"{y_dict[x]}\n")

        print(f'Data saved to {file_path}')
        plt.close(self.fig)


if __name__ == "__main__":
    drawer = LineDrawer()
    plt.show()
