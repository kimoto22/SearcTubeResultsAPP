import tkinter as tk

class DraggableWindow:
    def __init__(self, root, x, y):
        self.root = root
        self.root.overrideredirect(True)  # 標準のウィンドウ装飾を無効化
        self.root.attributes('-topmost', True)  # ウィンドウを最前面に表示
        self.root.bind("<ButtonPress-1>", self.on_drag_start)
        self.root.bind("<ButtonRelease-1>", self.on_drag_stop)
        self.root.bind("<B1-Motion>", self.on_drag_motion)
        self.x, self.y = 0, 0
        self.set_position(x, y)

    def on_drag_start(self, event):
        self.x, self.y = event.x, event.y

    def on_drag_stop(self, event):
        self.x, self.y = 0, 0

    def on_drag_motion(self, event):
        new_x = event.x_root - self.x
        new_y = event.y_root - self.y
        self.root.geometry(f"+{new_x}+{new_y}")

    def set_position(self, x, y):
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    windows = []

    # 4つのウィンドウを作成し、それぞれの位置を設定
    for i in range(4):
        window = tk.Toplevel(root)
        app = DraggableWindow(window, i * 100, i * 100)
        windows.append(app)

    root.mainloop()
