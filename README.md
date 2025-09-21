# Add-Watermark
给图片添加水印

作业在first_edition分支里，运行python文件即可对文件夹内的图片添加水印。

命令行运行该python文件的输入格式为 python add_watermark.py “文件路径” --font_size “字体大小（输入数字）” --color “RGB（例如：0,128,128）” --position “位置，有['left-top','right-top','center','left-bottom','right-bottom']可供选择” --xy （坐标，用户不满足于上面5个位置时，可自行选择水印要放置的坐标，用户提供坐标时自动覆盖position）
