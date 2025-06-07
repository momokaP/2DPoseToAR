import os
from multiprocessing import Process
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont

from show_ar import Show_AR
from Camera_Calibration import run_camera_calibration


def run_ar_process(video_path, gltf_path, animation_name, setting_path):
    Show_AR(video_path, gltf_path, animation1=animation_name, config_path=setting_path)


class ARCalibApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AR + Calibration")
        self.setup_ui()

    def setup_ui(self):
        window_width, window_height = 800, 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x, y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')

        self.tab_ar = ttk.Frame(notebook)
        self.tab_calib = ttk.Frame(notebook)
        notebook.add(self.tab_ar, text="Show AR")
        notebook.add(self.tab_calib, text="Calibration")

        self.create_tab_ar()
        self.create_tab_calibration()

    def browse_file(self, entry):
        path = filedialog.askopenfilename()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def browse_relative_file(self, entry):
        path = filedialog.askopenfilename()
        if path:
            rel_path = os.path.relpath(path).replace("\\", "/")
            entry.delete(0, tk.END)
            entry.insert(0, rel_path)

    def toggle_input(self, entry, button, var):
        state = "normal" if var.get() else "disabled"
        entry.config(state=state)
        button.config(state=state)

    def create_tab_ar(self):
        container = tk.Frame(self.tab_ar)
        container.pack(expand=True)

        frame = tk.LabelFrame(container, text=".gltf 파일 경로", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        frame.pack(pady=10, fill="x")
        self.entry_gltf = tk.Entry(frame, font=("TkDefaultFont", 12), width=40)
        self.entry_gltf.pack(side="left", padx=(0, 10))
        tk.Button(frame, text="파일 선택", command=lambda: self.browse_relative_file(self.entry_gltf)).pack(side="left")

        frame = tk.LabelFrame(container, text="영상 파일 경로 (체크 안하면 웹캠)", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        frame.pack(pady=10, fill="x")
        self.check_var = tk.IntVar()
        tk.Checkbutton(frame, variable=self.check_var, command=lambda: self.toggle_input(self.entry_video, self.btn_video, self.check_var)).pack(side="left", padx=(0, 10))
        self.entry_video = tk.Entry(frame, font=("TkDefaultFont", 12), width=40, state="disabled")
        self.entry_video.pack(side="left", padx=(0, 10))
        self.btn_video = tk.Button(frame, text="파일 선택", state="disabled", command=lambda: self.browse_file(self.entry_video))
        self.btn_video.pack(side="left")

        frame = tk.LabelFrame(container, text="카메라/체스보드 설정 파일 경로", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        frame.pack(pady=10, fill="x")
        self.entry_config = tk.Entry(frame, font=("TkDefaultFont", 12), width=40)
        self.entry_config.pack(side="left", padx=(0, 10))
        tk.Button(frame, text="파일 선택", command=lambda: self.browse_file(self.entry_config)).pack(side="left")

        frame = tk.LabelFrame(container, text="애니메이션 이름", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        frame.pack(pady=10, fill="x")
        tk.Label(frame, text="이름:").pack(side="left", padx=(0, 5))
        self.animation_entry = tk.Entry(frame, font=("TkDefaultFont", 12), width=20)
        self.animation_entry.pack(side="left")

        tk.Button(container, text="AR로 보여주기", command=self.run_show_ar).pack(pady=20)

    def create_tab_calibration(self):
        container = tk.Frame(self.tab_calib)
        container.pack(expand=True)

        frame = tk.LabelFrame(container, text="캘리브레이션 영상", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        frame.pack(pady=10, fill="x")
        self.calib_entry = tk.Entry(frame, font=("TkDefaultFont", 12), width=40)
        self.calib_entry.pack(side="left", padx=(0, 10))
        tk.Button(frame, text="파일 선택", command=lambda: self.browse_file(self.calib_entry)).pack(side="left")

        pattern_frame = tk.LabelFrame(container, text="체스보드 패턴 크기 (cols x rows)", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        pattern_frame.pack(pady=10, fill="x")
        tk.Label(pattern_frame, text="가로:").pack(side="left", padx=(0, 5))
        self.pattern_cols = tk.Entry(pattern_frame, font=("TkDefaultFont", 12), width=5)
        self.pattern_cols.insert(0, "10")
        self.pattern_cols.pack(side="left", padx=(0, 20))
        tk.Label(pattern_frame, text="세로:").pack(side="left", padx=(0, 5))
        self.pattern_rows = tk.Entry(pattern_frame, font=("TkDefaultFont", 12), width=5)
        self.pattern_rows.insert(0, "7")
        self.pattern_rows.pack(side="left")

        size_frame = tk.LabelFrame(container, text="셀 크기 (m)", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        size_frame.pack(pady=10, fill="x")
        tk.Label(size_frame, text="크기:").pack(side="left", padx=(0, 5))
        self.cell_size_entry = tk.Entry(size_frame, font=("TkDefaultFont", 12), width=10)
        self.cell_size_entry.insert(0, "0.023")
        self.cell_size_entry.pack(side="left")

        tk.Button(container, text="캘리브레이션 시작", command=self.run_calibration).pack(pady=20)

    def run_show_ar(self):
        try:
            gltf = self.entry_gltf.get()
            video = self.entry_video.get() if self.check_var.get() else None
            config = self.entry_config.get()
            anim = self.animation_entry.get()
            p = Process(target=run_ar_process, args=(video, gltf, anim, config))
            p.start()
            messagebox.showinfo("AR 실행", "AR 출력 시작!")
        except Exception as e:
            messagebox.showerror("에러", str(e))

    def run_calibration(self):
        try:
            path = self.calib_entry.get()
            cols = int(self.pattern_cols.get())
            rows = int(self.pattern_rows.get())
            cell_size = float(self.cell_size_entry.get())
            output = run_camera_calibration(path, (cols, rows), cell_size)
            messagebox.showinfo("완료", f"캘리브레이션 저장: {output}")
        except Exception as e:
            messagebox.showerror("에러", str(e))


def main():
    root = tk.Tk()
    app = ARCalibApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
