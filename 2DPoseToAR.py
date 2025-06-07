import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont

from convert_video_to_bvh import process_video_to_bvh
from show_ar import Show_AR

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
        notebook.add(self.tab1, text="2d to .bvh")
        notebook.add(self.tab2, text="Show AR")

        self.create_tab1()
        self.create_tab2()

    def browse_file(self, entry):
        path = filedialog.askopenfilename()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

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
        btn3 = tk.Button(file_frame3, text="파일 선택", command=lambda: self.browse_file(self.entry3))
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

        # 저장 경로 (선택)
        file_frame5 = tk.LabelFrame(container, text=" 결과 영상 저장 경로 (체크 안하면 저장안함) ", bd=5, relief="ridge", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        file_frame5.pack(pady=10, padx=10, fill="x")
        self.check_var3 = tk.IntVar()
        check3 = tk.Checkbutton(file_frame5, variable=self.check_var3, command=lambda: self.toggle_input(self.entry5, btn5, self.check_var3))
        check3.pack(side="left", padx=(0, 10))
        self.entry5 = tk.Entry(file_frame5, font=("TkDefaultFont", 12), width=40, state="disabled")
        self.entry5.pack(side="left", padx=(0, 10))
        btn5 = tk.Button(file_frame5, text="파일 선택", state="disabled", command=lambda: self.browse_file(self.entry5))
        btn5.pack(side="left")

        # 실행 버튼
        btn = tk.Button(container, text="AR로 보여주기", command=self.show_ar)
        btn.pack(pady=20)

    def convert_video_to_bvh(self):
        video_path = self.entry1.get()

        output_path = process_video_to_bvh(video_path)

        print(f"[bvh 변환] 영상: {video_path} → 저장: {output_path}")
        messagebox.showinfo("완료", f".bvh 변환 완료!")

    def show_ar(self):
        gltf_path = self.entry3.get()
        video_path = self.entry4.get() if self.check_var1.get() else None
        output_path = self.entry5.get() if self.check_var3.get() else None

        
            
        print(f"[AR 실행] 모델: {gltf_path} | 영상: {video_path or '웹캠'} | 저장: {output_path or 'X'}")
        messagebox.showinfo("AR 실행", "AR 출력 시작!")

# ---------------- 메인 함수 ----------------

def main():
    root = tk.Tk()
    app = PoseToARApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
