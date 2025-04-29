import tkinter as tk
from tkinter import colorchooser, messagebox, ttk, Menu
from datetime import datetime, timedelta
import tkinter.font as tkFont

class InputWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("下班倒计时")
        self.master.configure(bg='#2c3e50')
        
        # 创建滚动容器系统
        self.setup_scroll_system()
        
        # 初始化变量
        self.end_prompt = tk.StringVar(value="到点儿啦！")
        self.font_color = tk.StringVar(value="#00FF00")
        self.font_size = tk.IntVar(value=48)
        self.font_family = tk.StringVar(value=self.get_system_fonts()[0] if self.get_system_fonts() else "Arial")

        # 创建内容框架
        self.create_widgets()
        
        # 初始化界面样式
        self.update_preview_style()

    def get_system_fonts(self):
        fonts = []
        for family in tkFont.families():
            if family.strip():
                fonts.append(family)
        fonts.sort()
        return fonts

    def setup_scroll_system(self):
        """创建滚动容器系统"""
        self.canvas = tk.Canvas(self.master, bg='#2c3e50')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.scrollbar = ttk.Scrollbar(
            self.master, 
            orient=tk.VERTICAL, 
            command=self.canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.main_frame = tk.Frame(self.canvas, bg='#2c3e50')
        self.canvas_window = self.canvas.create_window(
            (0, 0), 
            window=self.main_frame, 
            anchor=tk.NW
        )
        
        self.bind_scroll_events()

    def bind_scroll_events(self):
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_widgets(self):
        """创建所有界面组件"""
        self.create_time_section(self.main_frame)
        self.create_font_section(self.main_frame)
        self.create_preview_section(self.main_frame)
        self.create_prompt_section(self.main_frame)
        self.create_control_buttons(self.main_frame)

    def create_time_section(self, parent):
        time_frame = tk.LabelFrame(parent, text="⏰ 时间设置", bg='#2c3e50', fg='white')
        time_frame.pack(pady=20, fill=tk.X)
        
        time_container = tk.Frame(time_frame, bg='#34495e')
        time_container.pack(pady=15, fill=tk.X, padx=15)
        
        tk.Label(time_container, text="输入下班时间 (HH:MM):", 
                bg='#34495e', fg='white', 
                font=('Segoe UI', 10, 'italic')).pack(anchor='w', pady=5)
        
        time_entry_frame = tk.Frame(time_container, bg='#34495e')
        time_entry_frame.pack(fill=tk.X, pady=10)
        
        self.time_entry = tk.Entry(
            time_entry_frame, 
            width=10, 
            font=('Segoe UI', 14, 'bold'),
            justify='center',
            bg='#404040',
            fg='white',
            insertbackground='white'
        )
        self.time_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.time_entry.insert(0, "18:00")
        
        tk.Label(
            time_container, 
            text="格式: 24小时制 HH:MM",
            bg='#34495e', 
            fg='#bdc3c7',
            font=('Segoe UI', 8)
        ).pack(side=tk.RIGHT, padx=10)

    def create_font_section(self, parent):
        font_frame = tk.LabelFrame(parent, text="🔤 字体设置", bg='#2c3e50', fg='white')
        font_frame.pack(pady=20, fill=tk.X)
        
        family_frame = tk.Frame(font_frame, bg='#34495e')
        family_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(family_frame, text="字体:", bg='#34495e', fg='white', 
                font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=10)
        
        self.font_combo = ttk.Combobox(
            family_frame, 
            textvariable=self.font_family,
            values=self.get_system_fonts(),
            state="readonly",
            width=25
        )
        self.font_combo.pack(side=tk.LEFT, padx=10)
        self.font_combo.current(0)
        self.font_combo.bind("<<ComboboxSelected>>", self.update_preview_style)

        size_frame = tk.Frame(font_frame, bg='#34495e')
        size_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(size_frame, text="字号:", bg='#34495e', fg='white', 
                font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=10)
        self.size_spinbox = ttk.Spinbox(
            size_frame, from_=12, to=100, textvariable=self.font_size,
            command=self.update_preview_style, width=5
        )
        self.size_spinbox.pack(side=tk.LEFT, padx=10)

        color_frame = tk.Frame(font_frame, bg='#34495e')
        color_frame.pack(pady=10, fill=tk.X)
        
        self.color_btn = tk.Button(
            color_frame, 
            text="🎨 选择颜色",
            command=self.choose_color,
            bg='#3498db', 
            fg='white',
            activebackground='#2980b9',
            padx=15,
            font=('Segoe UI', 10)
        )
        self.color_btn.pack(side=tk.LEFT, padx=10)

    def create_preview_section(self, parent):
        preview_frame = tk.LabelFrame(parent, text="📊 效果预览", bg='#2c3e50', fg='white')
        preview_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        preview_container = tk.Frame(preview_frame, bg='#34495e')
        preview_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.preview_label = tk.Label(
            preview_container, 
            text="18:00:00",
            font=("Arial", 48, 'bold'),
            fg=self.font_color.get(),
            bg='#34495e',
            bd=0,
            highlightthickness=0
        )
        self.preview_label.pack(pady=30, fill=tk.BOTH, expand=True)

    def create_prompt_section(self, parent):
        prompt_frame = tk.LabelFrame(parent, text="📝 结束提示", bg='#2c3e50', fg='white')
        prompt_frame.pack(pady=20, fill=tk.X)
        
        prompt_container = tk.Frame(prompt_frame, bg='#34495e')
        prompt_container.pack(pady=15, fill=tk.X, padx=15)
        
        tk.Label(prompt_container, text="倒计时结束提示词:", 
                bg='#34495e', fg='white', 
                font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        
        self.prompt_entry = tk.Entry(
            prompt_container, 
            width=30, 
            font=('Segoe UI', 10),
            textvariable=self.end_prompt
        )
        self.prompt_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.prompt_entry.insert(0, "")

    def create_control_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg='#2c3e50')
        btn_frame.pack(pady=20, fill=tk.X)
        
        self.start_btn = tk.Button(
            btn_frame, 
            text="▶ 开始倒计时",
            command=self.start_countdown,
            font=('Segoe UI', 12, 'bold'),
            bg='#27ae60', 
            fg='white',
            activebackground='#2ecc71',
            padx=25, 
            pady=12,
            relief=tk.RAISED
        )
        self.start_btn.pack(pady=15, fill=tk.X)

    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.font_color.get())
        if color and color[1]:
            self.font_color.set(color[1])
            self.update_preview_style()

    def update_preview_style(self, *args):
        font_tuple = (self.font_family.get(), self.font_size.get(), 'bold')
        self.preview_label.config(font=font_tuple, fg=self.font_color.get())

    def start_countdown(self):
        try:
            input_time = datetime.strptime(self.time_entry.get(), "%H:%M").time()
            now = datetime.now()
            target_datetime = datetime.combine(now.date(), input_time)
            
            if target_datetime < now:
                target_datetime += timedelta(days=1)
            
            delta = target_datetime - now
            total_seconds = int(delta.total_seconds())
            
            self.master.withdraw()
            self.countdown_window = CountdownWindow(
                total_seconds,
                self.font_color.get(),
                self.font_size.get(),
                self.font_family.get(),
                self.end_prompt.get(),
                self.master
            )
            
        except Exception as e:
            messagebox.showerror("错误", f"计算失败: {str(e)}")

class CountdownWindow:
    def __init__(self, total_seconds, font_color, font_size, font_family, end_prompt, master):
        self.master = master
        self.root = tk.Tk()
        self.root.title("倒计时")
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#000000')
        self.root.geometry("300x150+500+300")
        
        self.root.attributes('-transparentcolor', '#000000')
        self.root.overrideredirect(True)
        
        self.remaining = total_seconds
        self.end_prompt = end_prompt
        
        self.display = tk.Label(
            self.root, 
            text=self.format_time(self.remaining),
            font=(font_family, font_size), 
            fg=font_color,
            bg='#000000',
            bd=0,
            highlightthickness=0
        )
        self.display.pack(expand=True, pady=20)
        
        self.drag_data = {"x": 0, "y": 0, "dragging": False}
        
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag_window)
        self.root.bind("<ButtonRelease-1>", self.stop_drag)
        self.root.bind("<Button-3>", self.show_context_menu)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_display()

    def format_time(self, seconds):
        h, remainder = divmod(seconds, 3600)
        m, s = divmod(remainder, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def update_display(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.display.config(text=self.format_time(self.remaining))
            self.root.after(1000, self.update_display)
        else:
            self.display.config(text=self.end_prompt)

    def show_context_menu(self, event):
        menu = Menu(self.root, tearoff=0)
        menu.add_command(label="关闭", command=self.on_close)
        menu.add_command(label="重新设置", command=self.reopen_settings)
        menu.post(event.x_root, event.y_root)

    def reopen_settings(self):
        self.root.destroy()
        self.master.deiconify()

    def start_drag(self, event):
        self.drag_data["x"] = event.x_root
        self.drag_data["y"] = event.y_root
        self.drag_data["dragging"] = True

    def drag_window(self, event):
        if self.drag_data["dragging"]:
            dx = event.x_root - self.drag_data["x"]
            dy = event.y_root - self.drag_data["y"]
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")
            self.drag_data["x"] = event.x_root
            self.drag_data["y"] = event.y_root

    def stop_drag(self, event):
        self.drag_data["dragging"] = False

    def on_close(self):
        """完全退出程序"""
        self.master.destroy()  # 销毁主窗口
        self.root.destroy()    # 销毁倒计时窗口

if __name__ == "__main__":
    root = tk.Tk()
    app = InputWindow(root)
    root.mainloop()