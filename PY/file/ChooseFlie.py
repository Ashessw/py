#%%
import tkinter as tk
from tkinter import filedialog

#%%
def choose_file():
    # 创建窗口，打开文件对话框
    window = tk.Tk()
    window.title("选取文件")
    window.withdraw()
    window.wm_attributes("-topmost", True)


    # window.mainloop()
    filename = filedialog.askopenfilename()
    if filename != '':
        return (filename)
        root.destroy()  # 关闭窗口

