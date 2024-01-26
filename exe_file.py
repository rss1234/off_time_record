import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
import tkinter.font as tkfont
import os
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw


# 添加数据的函数
def add_data():
    popup = tk.Toplevel()
    popup.title('Add Data')
    tk.Label(popup, text="调休时长:").pack(side=tk.LEFT, padx=10, pady=10)
    length_entry = tk.Entry(popup)
    length_entry.pack(side=tk.LEFT, padx=10)
    popup.focus_set()
    length_entry.focus()

    def on_submit(event=None):
        data_length = length_entry.get()
        data_time = datetime.now().strftime("%Y/%m/%d")
        data_list.insert('', tk.END, values=(data_length, data_time))
        update_total()
        save_data()
        popup.destroy()

    length_entry.bind('<Return>', on_submit)
    submit_button = tk.Button(popup, text='Submit', command=on_submit)
    submit_button.pack(side=tk.RIGHT, padx=10, pady=10)


def update_total():
    total = 0
    for child in data_list.get_children():
        data = data_list.item(child)['values']
        length = data[0]
        if isinstance(length, int) or isinstance(length, float):
            total += length
        elif isinstance(length, str) and length.endswith('h'):
            total += float(length.replace('h', ''))
        else:
            print(f"无法处理的数据格式: {length}")
    total_label.config(text=f'调休时间剩余: {total}h')


def edit_time(event):
    selected_items = data_list.selection()
    if not selected_items:
        messagebox.showwarning("No Selection", "请先选择一个项然后再编辑时间。")
        return

    selected_item = selected_items[0]
    old_time = data_list.item(selected_item, 'values')[1]
    popup = tk.Toplevel()
    popup.title('Edit Time')
    tk.Label(popup, text="新时间 (YYYY/MM/DD):").pack(side=tk.LEFT, padx=10, pady=10)
    new_time_entry = tk.Entry(popup)
    new_time_entry.insert(0, old_time)
    new_time_entry.pack(side=tk.LEFT, padx=10)
    popup.focus_set()
    new_time_entry.focus()

    def on_submit(event=None):
        try:
            new_time = datetime.strptime(new_time_entry.get(), "%Y/%m/%d").strftime("%Y/%m/%d")
            data_list.item(selected_item, values=(data_list.item(selected_item, 'values')[0], new_time))
        except ValueError:
            messagebox.showerror("Invalid Date", "日期格式应为YYYY/MM/DD，请重新输入!")
            return
        save_data()
        popup.destroy()

    new_time_entry.bind('<Return>', on_submit)
    submit_button = tk.Button(popup, text='Submit', command=on_submit)
    submit_button.pack(side=tk.RIGHT, padx=10, pady=10)


def save_data():
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        for child in data_list.get_children():
            data = data_list.item(child)['values']
            file.write(f"{data[0]},{data[1]}\n")


def load_data():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                length, time = line.strip().split(',')
                data_list.insert('', tk.END, values=(length, time))
            update_total()
    else:
        print("数据文件未找到，将创建一个新文件。")


def delete_data(event):
    selected_item = data_list.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "请先选择一个项然后再尝试删除。")
        return
    if messagebox.askyesno("确认", "你确定要删除这条数据吗？"):
        data_list.delete(selected_item)
        save_data()
        update_total()


def minimize_app():
    data_list.pack_forget()
    add_button.pack_forget()
    total_label.pack(side=tk.LEFT, fill=tk.X)
    min_button.config(text="完整布局", command=restore_app)
    min_button.pack(side=tk.RIGHT)
    root.geometry(minimized_size)


def restore_app():
    data_list.pack(fill=tk.BOTH, expand=True)
    add_button.pack(side=tk.LEFT, padx=10, pady=10)
    min_button.config(text="简化布局", command=minimize_app)
    min_button.pack(side=tk.RIGHT, padx=10, pady=10)
    total_label.pack(side=tk.RIGHT, padx=10, pady=10)
    root.geometry(normal_size)


# 根据内容自动调整
def autosize_treeview_columns(treeview):
    for column in treeview['columns']:
        treeview.column(column, width=tkfont.Font().measure(column.title()))
        for row in treeview.get_children():
            # 调整列宽度以适应每行的内容
            cell_width = tkfont.Font().measure(treeview.item(row, 'values')[treeview['columns'].index(column)])
            if treeview.column(column)['width'] < cell_width:
                treeview.column(column, width=cell_width)


######################################################
# EXE package
######################################################
def create_image(width, height, color1, color2):
    # 创建一个空白图像，初始化为透明背景
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        [width // 2, 0, width, height // 2],
        fill=color2)
    dc.rectangle(
        [0, height // 2, width // 2, height],
        fill=color2)
    return image


def create_icon():
    icon_image = create_image(64, 64, 'black', 'blue')
    icon_menu = (item('还原', show_app), item('关闭', quit_app))
    icon = pystray.Icon("app_icon", icon_image, "我的应用", icon_menu)
    return icon


def on_minimize():
    root.withdraw()  # 隐藏主窗口
    global icon
    icon = create_icon()  # 创建新的图标实例
    icon.run()


def quit_app(icon, item):
    icon.stop()  # 停止图标
    root.destroy()  # 销毁主窗口
    os._exit(0)  # 强制Python清理并退出


def show_app(icon, item):
    root.after(0, root.deiconify)  # 显示窗口
    icon.stop()  # 停止当前的图标实例


username = os.getlogin()
app_name = "offTimeRecord_tk"
file_name = "data.txt"
file_path = f"C:\\Users\\{username}\\AppData\\Local\\{app_name}\\{file_name}"

minimized_size = "200x50"
normal_size = "300x300"

root = tk.Tk()
root.title("调休时长计算器")
root.geometry(normal_size)

root.attributes('-alpha', 0.9)

data_list = ttk.Treeview(root, columns=('Length', 'Time'), show='headings')
data_list.heading('Length', text='调休时长')
data_list.heading('Time', text='时间')
data_list.pack(fill=tk.BOTH, expand=True)

control_frame = tk.Frame(root)
control_frame.pack(fill=tk.X, side=tk.BOTTOM)

add_button = tk.Button(control_frame, text='添加记录', command=lambda: add_data())
add_button.pack(side=tk.LEFT, padx=10, pady=10)

total_label = tk.Label(control_frame, text='调休剩余时间: 0')
total_label.pack(side=tk.RIGHT, padx=10, pady=10)

min_button = tk.Button(control_frame, text="简化布局", command=minimize_app)
min_button.pack(side=tk.LEFT, padx=10, pady=10)

data_list.bind('<Button-3>', delete_data)
data_list.bind('<Double-1>', edit_time)

load_data()
autosize_treeview_columns(data_list)

# 程序是否进入后台
icon_running = False
# 设置主窗口关闭按钮的行为
root.protocol("WM_DELETE_WINDOW", root.destroy)  # 点击关闭按钮时正常关闭
root.bind("<Unmap>", lambda e: on_minimize() if root.state() == 'iconic' else None)  # 最小化时运行 on_minimize


# Main
root.mainloop()

