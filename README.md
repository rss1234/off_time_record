# off_time_record
Record off time, and show it on the desktop of windows. 

默认在目录`C:/Users/{username}/AppData/Local/offTimeRecord_tk`文件夹下创建`data.txt`文件用于保存历史数据。

在对应文件目录下，使用命令`pyinstaller --onefile --windowed --icon=app_logo.png exe_file.py`将.py文件编译为.exe可执行程序。

程序启动后会自动进入后台。

操作方式：
双击需要更改的日期，即可进行更改；
左键选中需要删除的行，单击右键进行删除。

如何设置程序开机自启：
win+R  -->  `shell:startup`  -->  右键新建快捷方式  -->  链接到file_name.exe文件中 [DONE]

