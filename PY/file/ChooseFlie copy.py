import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
 
def button_click():
    window1 = tk.Tk()
    window1.title("选取文件")
    window1.withdraw()
    window1.wm_attributes("-topmost", True)

    filename = filedialog.askopenfilename()
    if filename != '':
        print(filename)
    window1.destroy()  # 关闭窗口

# def radio_button_click():
#     selected = radio.get()
#     window1 = tk.Tk()
#     window1.title("选取文件")
#     window1.withdraw()
#     window1.wm_attributes("-topmost", True)

#     filename = filedialog.askopenfilename()
#     if filename != '':
#         print(filename)
#     window1.destroy()  # 关闭窗口
 
# 创建主窗口对象
window = tk.Tk()
# 设置窗口标题
window.title("选择数据文件")

window.geometry("500x300")
 
# 创建按钮对象
button1 = tk.Button(window, text="选择案件原始数据", command=button_click)
button2 = tk.Button(window, text="选择字段采集表", command=button_click)

# 单选按钮
radio1 = ttk.Radiobutton(window,text="信用卡")
radio2 = ttk.Radiobutton(window,text="非信用卡")

# 按钮布局
button1.grid(row=0,column=0)
button2.grid(row=1,column=0)
radio1.grid(row=2,column=1)
radio2.grid(row=2,column=2)
 

 
# 进入消息循环
window.mainloop()