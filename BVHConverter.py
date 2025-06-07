import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont

from convert_video_to_bvh import process_video_to_bvh

class BVHConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2DPoseToBVH")
        self.setup_ui()

    def setup_ui(self):
        window_width, window_height = 800, 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x, y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        container = tk.Frame(self.root)
        container.pack(expand=True)

        file_frame1 = tk.LabelFrame(container, text=" 포즈 영상 파일 경로 ", bd=5, relief="ridge", font=("TkDefaultFont", 14, "bold"), pady=10, padx=10)
        file_frame1.pack(pady=10, padx=10, fill="x")
        self.entry1 = tk.Entry(file_frame1, font=("TkDefaultFont", 12), width=40)
        self.entry1.pack(side="left", padx=(0, 10))
        btn1 = tk.Button(file_frame1, text="파일 선택", command=self.browse_file)
        btn1.pack(side="left")

        btn = tk.Button(container, text="영상에서 포즈 추출하고 .bvh로 변환", command=self.convert_video_to_bvh)
        btn.pack(pady=20)

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.entry1.delete(0, tk.END)
            self.entry1.insert(0, path)

    def convert_video_to_bvh(self):
        try:
            video_path = self.entry1.get()
            output_path = process_video_to_bvh(video_path)
            messagebox.showinfo("완료", f".bvh 변환 완료! {output_path}")
        except Exception as e:
            messagebox.showerror("입력 오류", f"에러 발생: {e}")


def main():
    root = tk.Tk()
    app = BVHConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
