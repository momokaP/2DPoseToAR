import os
from multiprocessing import Process

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont

from convert_video_to_bvh import process_video_to_bvh
from show_ar import Show_AR
from Camera_Calibration import run_camera_calibration

def run_ar_process(video_path, gltf_path, animation_name, setting_path):
    Show_AR(video_path, gltf_path, animation1=animation_name, config_path=setting_path)

class PoseToARApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2DPoseToAR")
        self.setup_ui()

    def setup_ui(self):
        # 창 크기 설정 및 중앙 배치
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 글꼴 설정
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        # Notebook (탭)
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')

        self.tab1 = ttk.Frame(notebook)
        self.tab2 = ttk.Frame(notebook)
        self.tab3 = ttk.Frame(notebook)
        notebook.add(self.tab1, text="2d to .bvh")
        notebook.add(self.tab2, text="Show AR")
        notebook.add(self.tab3, text="Calibration")

        self.create_tab1()
        self.create_tab2()
        self.create_tab3()

    def browse_file(self, entry):
        path = filedialog.askopenfilename()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def browse_relative_file(self, entry):
        path = filedialog.askopenfilename()
        if path:
            rel_path = os.path.relpath(path)
            rel_path = rel_path.replace("\\", "/")
            entry.delete(0, tk.END)
            entry.insert(0, rel_path)

    def browse_directory(self, entry):
        path = filedialog.askdirectory()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def toggle_input(self, entry, button, var):
        state = "normal" if var.get() else "disabled"
        entry.config(state=state)
        button.config(state=state)

    def create_tab1(self):
        container = tk.Frame(self.tab1)
        container.pack(expand=True)

        # 포즈 영상 경로
        file_frame1 = tk.LabelFrame(container, text=" 포즈 영상 파일 경로 ", bd=5, relief="ridge", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        file_frame1.pack(pady=10, padx=10, fill="x")
        self.entry1 = tk.Entry(file_frame1, font=("TkDefaultFont", 12), width=40)
        self.entry1.pack(side="left", padx=(0, 10))
        btn1 = tk.Button(file_frame1, text="파일 선택", command=lambda: self.browse_file(self.entry1))
        btn1.pack(side="left")

        # bvh 출력 경로
        # file_frame2 = tk.LabelFrame(container, text=" 출력될 .bvh 경로 ", bd=5, relief="ridge", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        # file_frame2.pack(pady=10, padx=10, fill="x")
        # self.entry2 = tk.Entry(file_frame2, font=("TkDefaultFont", 12), width=40)
        # self.entry2.pack(side="left", padx=(0, 10))
        # btn2 = tk.Button(file_frame2, text="폴더 선택", command=lambda: self.browse_directory(self.entry2))
        # btn2.pack(side="left")

        # 실행 버튼
        btn = tk.Button(container, text="영상에서 포즈 추출하고 .bvh로 변환", command=self.convert_video_to_bvh)
        btn.pack(pady=20)

    def create_tab2(self):
        container = tk.Frame(self.tab2)
        container.pack(expand=True)

        # gltf 경로
        file_frame3 = tk.LabelFrame(container, text=" .gltf 파일 경로 ", bd=5, relief="ridge", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        file_frame3.pack(pady=10, padx=10, fill="x")
        self.entry3 = tk.Entry(file_frame3, font=("TkDefaultFont", 12), width=40)
        self.entry3.pack(side="left", padx=(0, 10))
        btn3 = tk.Button(file_frame3, text="파일 선택", command=lambda: self.browse_relative_file(self.entry3))
        btn3.pack(side="left")

        # 영상 파일 (선택)
        file_frame4 = tk.LabelFrame(container, text=" 영상 파일 경로 (체크 안하면 웹캠) ", bd=5, relief="ridge", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        file_frame4.pack(pady=10, padx=10, fill="x")
        self.check_var1 = tk.IntVar()
        check1 = tk.Checkbutton(file_frame4, variable=self.check_var1, command=lambda: self.toggle_input(self.entry4, btn4, self.check_var1))
        check1.pack(side="left", padx=(0, 10))
        self.entry4 = tk.Entry(file_frame4, font=("TkDefaultFont", 12), width=40, state="disabled")
        self.entry4.pack(side="left", padx=(0, 10))
        btn4 = tk.Button(file_frame4, text="파일 선택", state="disabled", command=lambda: self.browse_file(self.entry4))
        btn4.pack(side="left")

        # 카메라, 체스보드 설정 파일 경로
        file_frame5 = tk.LabelFrame(container, text=" 카메라, 체스보드 설정 파일 경로", bd=5, relief="ridge", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        file_frame5.pack(pady=10, padx=10, fill="x")
        self.entry5 = tk.Entry(file_frame5, font=("TkDefaultFont", 12), width=40)
        self.entry5.pack(side="left", padx=(0, 10))
        btn5 = tk.Button(file_frame5, text="파일 선택", command=lambda: self.browse_file(self.entry5))
        btn5.pack(side="left")

        # 애니메이션 이름 입력
        size_frame = tk.LabelFrame(container, text=" 애니메이션 이름", bd=5, relief="ridge",
                                font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        size_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(size_frame, text="애니메이션 이름:").pack(side="left", padx=(0, 5))
        self.animation_entry = tk.Entry(size_frame, font=("TkDefaultFont", 12), width=10)
        self.animation_entry.pack(side="left")

        # 실행 버튼
        btn = tk.Button(container, text="AR로 보여주기", command=self.show_ar)
        btn.pack(pady=20)

    def create_tab3(self):
        container = tk.Frame(self.tab3)
        container.pack(expand=True)

        # 영상 파일 경로 입력
        file_frame = tk.LabelFrame(container, text=" 캘리브레이션 할 영상 파일 경로 ", bd=5, relief="ridge",
                                font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        file_frame.pack(pady=10, padx=10, fill="x")

        self.calib_entry = tk.Entry(file_frame, font=("TkDefaultFont", 12), width=40)
        self.calib_entry.pack(side="left", padx=(0, 10))

        calib_btn = tk.Button(file_frame, text="파일 선택", command=lambda: self.browse_file(self.calib_entry))
        calib_btn.pack(side="left")

        # 보드 패턴 입력 (가로, 세로)
        pattern_frame = tk.LabelFrame(container, text=" 체스보드 패턴 크기 (cols x rows) ", bd=5, relief="ridge",
                                    font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        pattern_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(pattern_frame, text="가로(col):").pack(side="left", padx=(0, 5))
        self.pattern_cols = tk.Entry(pattern_frame, font=("TkDefaultFont", 12), width=5)
        self.pattern_cols.insert(0, "10")
        self.pattern_cols.pack(side="left", padx=(0, 20))

        tk.Label(pattern_frame, text="세로(row):").pack(side="left", padx=(0, 5))
        self.pattern_rows = tk.Entry(pattern_frame, font=("TkDefaultFont", 12), width=5)
        self.pattern_rows.insert(0, "7")
        self.pattern_rows.pack(side="left")

        # 셀 크기 입력
        size_frame = tk.LabelFrame(container, text=" 보드 셀 크기 (미터 단위)", bd=5, relief="ridge",
                                font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        size_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(size_frame, text="셀 크기(m):").pack(side="left", padx=(0, 5))
        self.cell_size_entry = tk.Entry(size_frame, font=("TkDefaultFont", 12), width=10)
        self.cell_size_entry.insert(0, "0.023")
        self.cell_size_entry.pack(side="left")

        # 캘리브레이션 시작 버튼
        start_btn = tk.Button(container, text="캘리브레이션 시작", command=self.start_calibration)
        start_btn.pack(pady=20)

    def convert_video_to_bvh(self):
        try:
            video_path = self.entry1.get()
        except Exception as e:
            messagebox.showerror("입력 오류", "입력 오류")
            print(f"{e}")
            return
        
        output_path = process_video_to_bvh(video_path)

        messagebox.showinfo("완료", f".bvh 변환 완료! {output_path}")

    def show_ar(self):
        try:
            gltf_path = self.entry3.get()
            video_path = self.entry4.get() if self.check_var1.get() else None
            setting_path = self.entry5.get()
            animation_name = self.animation_entry.get()
        except Exception as e:
            messagebox.showerror("입력 오류", "입력 오류")
            print(f"{e}")
            return
        
        # Show_AR(video_path, gltf_path, animation1=animation_name, config_path=setting_path)
        p = Process(target=run_ar_process, 
                    args=(video_path, gltf_path, animation_name, setting_path))
        p.start()

        messagebox.showinfo("AR 실행", "AR 출력 시작!")

    def start_calibration(self):
        try:
            video_path = self.calib_entry.get()
            cols = int(self.pattern_cols.get())
            rows = int(self.pattern_rows.get())
            board_pattern = (cols, rows)

            cell_size = float(self.cell_size_entry.get())
            board_cellsize = cell_size
        except Exception as e:
            messagebox.showerror("입력 오류", "입력 오류")
            print(f"{e}")
            return
    
        output_file = run_camera_calibration(video_path, board_pattern, board_cellsize)

        messagebox.showinfo("캘리브레이션", f"캘리브레이션 값 경로: {output_file}")

# ---------------- 메인 함수 ----------------

def main():
    root = tk.Tk()
    app = PoseToARApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
