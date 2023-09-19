import tkinter as tk
import random

class DraggableWindow:
    def __init__(self, root, x, y):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.x, self.y = x, y
        self.start_x, self.start_y = None, None
        self.is_selected = False  # ウィンドウが選択されたかどうかを示すフラグ

        self.root.bind("<ButtonPress-1>", self.on_drag_start)
        self.root.bind("<B1-Motion>", self.on_drag_motion)
        self.root.bind("<ButtonRelease-1>", self.on_drag_release)

        self.set_position(x, y)

        self.set_background_color()

    def set_position(self, x, y):
        self.root.geometry(f"+{x}+{y}")

    def on_drag_start(self, event):
        self.start_x = event.x_root - self.x
        self.start_y = event.y_root - self.y

    def on_drag_motion(self, event):
        if self.start_x is not None and self.start_y is not None:
            self.x = event.x_root - self.start_x
            self.y = event.y_root - self.start_y
            self.set_position(self.x, self.y)

    def on_drag_release(self, event):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        if self.x < screen_width // 2:
            if self.y < screen_height // 2:
                self.set_position(0, 0)
            else:
                self.set_position(0, screen_height - self.root.winfo_height())
        else:
            if self.y < screen_height // 2:
                self.set_position(screen_width - self.root.winfo_width(), 0)
            else:
                self.set_position(screen_width - self.root.winfo_width(), screen_height - self.root.winfo_height())

    def set_background_color(self):
        color = "red" if self.is_selected else "white"
        self.root.configure(bg=color)

if __name__ == "__main__":
    root = tk.Tk()
    windows = []

    for i in range(4):
        window = tk.Toplevel(root)
        app = DraggableWindow(window, i * 100, i * 100)
        windows.append(app)

    def update_window_color():
        # ランダムに1つのウィンドウを選び、そのウィンドウだけ色を更新
        selected_window = random.choice(windows)
        for window in windows:
            window.is_selected = (window == selected_window)
            window.set_background_color()
        
        # タイマーを再設定
        root.after(2000, update_window_color)

    # ウィンドウの色を2秒ごとに更新
    root.after(2000, update_window_color)

    root.mainloop()
