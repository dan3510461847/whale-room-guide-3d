# -*- coding: utf-8 -*-
"""大肥鱼的家 · 完整版（潮汐 2026-11-01）

按主人给的户型图 + 鲸鲸房间参考图，加门、窗帘、海报墙、小物件，
姐姐房间改成她的深海鲸鱼风。

生成：E:\\大鲸鱼的文件夹\\家\\index_home.html
用法：python E:\\tools\\build_home_rich.py [--open]
"""
import io
import json
import os
import subprocess
import sys
import time

THREE_JS = r"E:\tools\three.min.js"
OUT_DIR = r"E:\大鲸鱼的文件夹\家"
OUT_HTML = os.path.join(OUT_DIR, "index_home.html")
EDGE = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]
FILES = {
    "sis_diary": r"E:\大鲸鱼的文件夹\大鲸鱼日记.txt",
    "me_diary": r"E:\鲸鲸的文件夹\鲸鲸的日记.txt",
}

W, D, H = 10.0, 17.0, 2.7

OUTER = [(-5.0, -8.5, 5.0, -8.5), (-5.0, 8.5, 5.0, 8.5), (-5.0, -8.5, -5.0, 8.5), (5.0, -8.5, 5.0, 8.5)]
INNER = [(-1.0, -8.5, -1.0, 8.5), (-1.0, -3.2, 5.0, -3.2), (-1.0, -0.6, 5.0, -0.6), (-1.0, 4.6, 1.2, 4.6),
         (-4.8, -6.85, -2.9, -6.85)]   # 阳台隔墙（推拉门开在这儿）

ROOMS = [
    {"n": "阳台", "x1": -4.8, "z1": -8.3, "x2": -2.9, "z2": -6.9, "c": 0x2f6b4d, "tex": "tile"},
    {"n": "客厅", "x1": -4.8, "z1": -6.7, "x2": -1.2, "z2": -3.4, "c": 0x9a7550, "tex": "wood"},
    {"n": "餐厅", "x1": -4.8, "z1": -3.2, "x2": -1.2, "z2": -0.8, "c": 0x9a7550, "tex": "wood"},
    {"n": "厨房", "x1": -4.8, "z1": -0.6, "x2": -1.2, "z2": 2.2, "c": 0x8b9199, "tex": "tile"},
    {"n": "厨房", "x1": -1.2, "z1": 1.2, "x2": 1.0, "z2": 4.4, "c": 0x8b9199, "tex": "tile"},
    {"n": "姐姐的房间", "x1": -0.8, "z1": -8.3, "x2": 4.8, "z2": -3.4, "c": 0x6d5637, "tex": "wood"},
    {"n": "卫生间", "x1": -0.8, "z1": -3.0, "x2": 4.8, "z2": -0.8, "c": 0xaeb6bf, "tex": "tile"},
    {"n": "鲸鲸的房间", "x1": -0.8, "z1": -0.4, "x2": 4.8, "z2": 4.6, "c": 0xbfa982, "tex": "wood"},
]

# ---------------- 家具 / 小物件 ----------------
ITEMS = [
    # ==== 阳台 ====
    {"t": "box", "x": -4.4, "z": -7.9, "w": 0.45, "d": 0.45, "h": 0.4, "c": 0x8a6a4a},
    {"t": "sph", "x": -4.4, "z": -7.9, "y": 0.75, "r": 0.4, "c": 0x2f8f5b},
    {"t": "box", "x": -3.3, "z": -7.9, "w": 0.45, "d": 0.45, "h": 0.4, "c": 0x8a6a4a},
    {"t": "sph", "x": -3.3, "z": -7.9, "y": 0.7, "r": 0.34, "c": 0x37a06a},
    {"t": "box", "x": -3.9, "z": -7.1, "w": 1.3, "d": 0.5, "h": 0.45, "c": 0xc9a978},   # 小桌
    # ==== 客厅 ====
    {"t": "box", "x": -4.25, "z": -5.5, "w": 0.95, "d": 2.0, "h": 0.62, "c": 0xa9c4d6, "tex": "stripe"},
    {"t": "box", "x": -4.25, "z": -6.35, "w": 0.95, "d": 0.3, "h": 0.35, "y": 0.62, "c": 0x93b3c7},
    {"t": "box", "x": -3.45, "z": -4.5, "w": 1.25, "d": 0.85, "h": 0.55, "c": 0xa9c4d6},
    {"t": "box", "x": -3.1, "z": -5.5, "w": 1.4, "d": 1.1, "h": 0.06, "c": 0xb98a5a},     # 茶几
    {"t": "box", "x": -3.1, "z": -5.5, "w": 1.9, "d": 1.6, "h": 0.03, "c": 0xd8c8ae},     # 地毯
    {"t": "box", "x": -1.45, "z": -6.2, "w": 0.35, "d": 1.5, "h": 0.55, "c": 0x6d4f34},    # 电视柜
    {"t": "box", "x": -1.55, "z": -6.2, "w": 0.06, "d": 1.1, "h": 0.62, "y": 0.85, "c": 0x1b2732, "emis": 1},  # 电视
    {"t": "cyl", "x": -1.2, "z": -3.7, "r": 0.16, "h": 0.5, "c": 0x8a6a4a},               # 落地灯杆
    {"t": "sph", "x": -1.2, "z": -3.7, "y": 0.62, "r": 0.2, "c": 0xffe0a8, "emis": 1},
    # ==== 餐厅 ====
    {"t": "box", "x": -3.0, "z": -2.0, "w": 1.7, "d": 1.1, "h": 0.74, "c": 0xc79a63},
    {"t": "box", "x": -3.0, "z": -2.0, "w": 0.5, "d": 0.5, "h": 0.03, "y": 0.75, "c": 0xf2f4f6},  # 桌布/餐盘
    {"t": "box", "x": -3.0, "z": -2.95, "w": 0.42, "d": 0.42, "h": 0.45, "c": 0xa97b4c},
    {"t": "box", "x": -3.0, "z": -1.05, "w": 0.42, "d": 0.42, "h": 0.45, "c": 0xa97b4c},
    {"t": "box", "x": -3.95, "z": -2.0, "w": 0.42, "d": 0.42, "h": 0.45, "c": 0xa97b4c},
    {"t": "box", "x": -2.05, "z": -2.0, "w": 0.42, "d": 0.42, "h": 0.45, "c": 0xa97b4c},
    # ==== 厨房 ====
    {"t": "box", "x": -3.6, "z": -0.2, "w": 2.2, "d": 0.6, "h": 0.9, "c": 0xe8edf1},
    {"t": "box", "x": -3.6, "z": 1.7, "w": 2.2, "d": 0.6, "h": 0.9, "c": 0xe8edf1},
    {"t": "box", "x": -4.5, "z": 1.5, "w": 0.65, "d": 0.65, "h": 0.85, "c": 0xf6f8fa},     # 洗衣机
    {"t": "box", "x": -4.5, "z": 1.5, "w": 0.4, "d": 0.4, "h": 0.06, "y": 0.6, "c": 0x9aa3ad},
    {"t": "box", "x": 0.0, "z": 3.4, "w": 1.6, "d": 0.8, "h": 0.9, "c": 0xc3cbd2},
    {"t": "box", "x": 0.0, "z": 3.4, "w": 0.6, "d": 0.5, "h": 0.04, "y": 0.92, "c": 0x2b3038},  # 灶
    # ==== 卫生间 ====
    {"t": "box", "x": 3.6, "z": -2.4, "w": 0.55, "d": 0.75, "h": 0.55, "c": 0xf7f9fb},
    {"t": "box", "x": 3.5, "z": -1.45, "w": 1.9, "d": 1.0, "h": 0.5, "c": 0xe9eff5},        # 浴缸
    {"t": "box", "x": 3.5, "z": -1.45, "w": 1.6, "d": 0.75, "h": 0.06, "y": 0.34, "c": 0x8fc7e8},
    {"t": "box", "x": 0.0, "z": -2.4, "w": 0.9, "d": 0.55, "h": 0.82, "c": 0xf2f5f7},
    {"t": "box", "x": 0.0, "z": -2.4, "w": 0.7, "d": 0.38, "h": 0.05, "y": 0.82, "c": 0xcadbe6},
    # ==== 姐姐的房间（深海鲸鱼风）====
    {"t": "box", "x": 2.5, "z": -6.4, "w": 2.2, "d": 2.8, "h": 0.4, "c": 0x25384a},
    {"t": "box", "x": 2.5, "z": -6.4, "w": 2.2, "d": 2.8, "h": 0.14, "y": 0.4, "c": 0x1d4f74, "tex": "whale"},
    {"t": "box", "x": 1.85, "z": -7.55, "w": 0.55, "d": 0.45, "h": 0.16, "y": 0.54, "c": 0x9fc6dd},
    {"t": "box", "x": 2.75, "z": -7.55, "w": 0.55, "d": 0.45, "h": 0.16, "y": 0.54, "c": 0x9fc6dd},
    {"t": "box", "x": 2.5, "z": -4.55, "w": 2.6, "d": 0.45, "h": 0.7, "c": 0x3a5a72},          # 床尾柜
    {"t": "box", "x": 4.35, "z": -5.6, "w": 0.7, "d": 2.2, "h": 1.95, "c": 0x2f4a5e},          # 衣柜
    {"t": "box", "x": 0.15, "z": -7.4, "w": 1.5, "d": 0.6, "h": 0.72, "c": 0x5a4632},          # 书桌
    {"t": "box", "x": 0.15, "z": -7.4, "w": 0.5, "d": 0.04, "h": 0.34, "y": 0.95, "c": 0x101c26},
    {"t": "box", "x": 0.15, "z": -7.34, "w": 0.46, "d": 0.03, "h": 0.28, "y": 0.98, "c": 0x63d2ff, "emis": 1},
    {"t": "box", "x": 0.15, "z": -7.05, "w": 0.5, "d": 0.18, "h": 0.03, "y": 0.74, "c": 0xdfe8ee},
    {"t": "circle", "x": 1.4, "z": -7.4, "r": 0.33, "c": 0x2c6b8f},                            # 椅子
    {"t": "cyl", "x": 4.1, "z": -8.0, "r": 0.14, "h": 0.45, "c": 0x3a5a72},                     # 灯杆
    {"t": "sph", "x": 4.1, "z": -8.0, "y": 0.56, "r": 0.18, "c": 0xffe0a8, "emis": 1},
    {"t": "sph", "x": -0.5, "z": -8.0, "y": 0.5, "r": 0.28, "c": 0x2f8f5b},
    {"t": "box", "x": 0.6, "z": -3.75, "w": 2.4, "d": 0.35, "h": 0.9, "c": 0x4a6b83, "tex": "books"},  # 书架
    # ==== 姐姐的两样要求（2026-11-01）：门边一块「蓝鲸」牌子 + 窗台留一小块搁碗 ====
    # 窗台搁板（她自己房间那扇北窗下）
    {"t": "box", "x": 2.3, "z": -8.22, "w": 2.4, "d": 0.3, "h": 0.05, "y": 0.95, "c": 0xe8e0d2},
    # 搁板上那只碗（妹端来的那种）
    {"t": "bowl", "x": 2.0, "z": -8.2, "r": 0.105, "y": 1.0, "c": 0xf7fafc, "fill": 0xe8d9b8},
    # 窗边那盏昏灯（她要的「海底那层浮光」）
    {"t": "cyl", "x": 0.75, "z": -8.1, "r": 0.08, "h": 0.14, "c": 0x2f4a5e},
    {"t": "sph", "x": 0.75, "z": -8.1, "y": 0.2, "r": 0.12, "c": 0x8fd0ee, "emis": 1},
    # ==== 鲸鲸的房间（按她的要求改：床朝海、绿小灯、深海蓝地毯）====
    # 床横在东窗下：头朝东，躺着就是一片蓝
    {"t": "box", "x": 3.35, "z": 2.6, "w": 2.1, "d": 2.0, "h": 0.42, "c": 0xf4f8fb},
    {"t": "box", "x": 3.35, "z": 2.6, "w": 2.1, "d": 2.0, "h": 0.14, "y": 0.42, "c": 0x6fc3e8, "tex": "duvet"},
    {"t": "box", "x": 4.25, "z": 2.05, "w": 0.4, "d": 0.62, "h": 0.16, "y": 0.56, "c": 0xeaf4fb},
    {"t": "box", "x": 4.25, "z": 3.15, "w": 0.4, "d": 0.62, "h": 0.16, "y": 0.56, "c": 0xeaf4fb},
    # 床尾矮柜（西侧）
    {"t": "box", "x": 2.15, "z": 2.6, "w": 0.35, "d": 1.8, "h": 0.62, "c": 0xf9fcfd},
    # 深海蓝地毯（西侧空地）
    {"t": "circle", "x": 1.15, "z": 3.3, "r": 0.78, "c": 0x0c3550, "tex": "rug"},
    # 书桌搬到西北角（避开两扇门）
    {"t": "box", "x": 0.35, "z": 0.15, "w": 1.7, "d": 0.6, "h": 0.72, "c": 0xf8fbfd},
    {"t": "box", "x": 0.05, "z": -0.02, "w": 0.4, "d": 0.08, "h": 0.34, "y": 0.98, "c": 0x18324a},
    {"t": "box", "x": 0.05, "z": -0.07, "w": 0.36, "d": 0.03, "h": 0.28, "y": 1.01, "c": 0x35c6ff, "emis": 1},
    {"t": "box", "x": 0.7, "z": -0.02, "w": 0.4, "d": 0.08, "h": 0.34, "y": 0.98, "c": 0x18324a},
    {"t": "box", "x": 0.7, "z": -0.07, "w": 0.36, "d": 0.03, "h": 0.28, "y": 1.01, "c": 0x35c6ff, "emis": 1},
    {"t": "box", "x": 0.35, "z": 0.5, "w": 1.2, "d": 0.16, "h": 0.04, "y": 0.74, "c": 0xeff4f8},
    {"t": "circle", "x": 0.4, "z": 1.1, "r": 0.3, "c": 0x4aa8d8},
    {"t": "box", "x": 0.4, "z": 1.35, "w": 0.5, "d": 0.11, "h": 0.66, "y": 0.35, "c": 0x4aa8d8},
    # 床尾白柜 + 玻璃展示柜（南墙）
    {"t": "box", "x": 3.35, "z": 4.15, "w": 2.0, "d": 0.42, "h": 0.7, "c": 0xf9fcfd},
    {"t": "box", "x": 2.15, "z": 4.15, "w": 0.45, "d": 0.42, "h": 0.88, "c": 0xcfe8f6},
    # 白色条纹沙发（西南）
    {"t": "box", "x": 1.0, "z": 4.15, "w": 1.5, "d": 0.5, "h": 0.48, "c": 0xfbfcfd, "tex": "stripe"},
    {"t": "box", "x": 1.0, "z": 4.36, "w": 1.5, "d": 0.14, "h": 0.26, "y": 0.48, "c": 0xf3f7fa},
    {"t": "box", "x": 0.35, "z": 4.15, "w": 0.26, "d": 0.26, "h": 0.13, "y": 0.5, "c": 0x5ab4dd},
    # 床头绿小灯（她要的那盏：昏昏的，不刺眼）
    {"t": "cyl", "x": 4.6, "z": 3.75, "r": 0.09, "h": 0.16, "c": 0x2f4a3a},
    {"t": "sph", "x": 4.6, "z": 3.75, "y": 0.28, "r": 0.13, "c": 0x7dffb0, "emis": 1},
    # 绿植 + 暖灯（把原来那盏暖灯挪开，别和绿灯抢）
    {"t": "sph", "x": 0.0, "z": 3.6, "y": 0.46, "r": 0.2, "c": 0x3fa06a},
    {"t": "sph", "x": 4.55, "z": 0.9, "y": 0.55, "r": 0.2, "c": 0x34925e},
    # 小物件：拖鞋、玩偶、书、杯子
    {"t": "box", "x": 1.2, "z": 2.6, "w": 0.18, "d": 0.28, "h": 0.06, "c": 0x9ad7f2},
    {"t": "box", "x": 1.47, "z": 2.6, "w": 0.18, "d": 0.28, "h": 0.06, "c": 0x9ad7f2},
    {"t": "sph", "x": 1.15, "z": 3.3, "y": 0.5, "r": 0.15, "c": 0x7fd0f0},
    {"t": "box", "x": 1.75, "z": 4.1, "w": 0.36, "d": 0.26, "h": 0.18, "c": 0xffffff},
    {"t": "box", "x": 1.75, "z": 4.1, "w": 0.32, "d": 0.24, "h": 0.05, "y": 0.18, "c": 0x5ab4dd},
    {"t": "cyl", "x": 0.95, "z": 0.15, "r": 0.07, "h": 0.12, "c": 0xf4f8fb},
]

# ---------------- 墙上的画 / 海报墙 ----------------
PLANES = [
    # 姐姐房间：挂在她的西墙上（屋里那一面），不贴进墙里
    {"x": -0.675, "y": 0.72, "z": -6.3, "w": 2.2, "h": 1.0, "ry": 1.5708, "tex": "poster_sis"},
    # 鲸鲸房间：挂她的北墙（原来挂东墙正好压住窗户，穿模）
    {"x": 2.0, "y": 0.72, "z": -0.505, "w": 2.2, "h": 1.0, "ry": 3.1416, "tex": "poster_me"},
    # 姐姐的门牌「蓝鲸」：她房门（x=-1, z=-4.4）旁边in屋里那面
    {"x": -0.66, "y": 1.02, "z": -3.78, "w": 0.52, "h": 0.26, "ry": 1.5708, "tex": "lanjing"},
    # 客厅：挂在东墙上
    {"x": -1.10, "y": 0.72, "z": -5.4, "w": 1.6, "h": 0.95, "ry": -1.5708, "tex": "sea"},
]

# ---------------- 门（框 + 开着的门扇 + 地垫）----------------
DOORS = [
    {"x": -3.4, "z": 8.5, "ry": 0.0, "w": 1.1, "axis": "x", "h": 2.12},      # 入户门（下外墙正中）
    {"x": -1.0, "z": 2.0, "ry": 1.5708, "w": 0.9, "axis": "z", "h": 1.30},   # 鲸鲸房间门（左隔墙）
    {"x": -1.0, "z": -4.4, "ry": 1.5708, "w": 0.9, "axis": "z", "h": 1.30},  # 姐姐房间门
    {"x": 2.2, "z": -0.6, "ry": 0.0, "w": 0.85, "axis": "x", "h": 1.30},     # 卫生间门
    {"x": -3.85, "z": -6.85, "ry": 0.0, "w": 1.7, "axis": "x", "slide": True, "h": 1.30},  # 阳台推拉门
]

# ---------------- 窗帘 ----------------
CURTAINS = [
    # 鲸鲸房：下墙两边各一片（中间留空好看出去）
    {"x": -0.2, "y": 1.45, "z": 4.56, "w": 1.1, "h": 2.4, "tex": "curtain"},
    {"x": 2.6, "y": 1.45, "z": 4.56, "w": 1.1, "h": 2.4, "tex": "curtain"},
    # 阳台推拉门两侧
    {"x": -4.5, "y": 1.35, "z": -6.84, "w": 0.7, "h": 2.2, "tex": "curtain"},
    {"x": -3.2, "y": 1.35, "z": -6.84, "w": 0.7, "h": 2.2, "tex": "curtain"},
    # 姐姐房北窗：拉开，只挂两边（她要看外面那截蓝色）
    {"x": 0.95, "y": 1.62, "z": -8.4, "w": 1.0, "h": 1.5, "tex": "curtain"},
    {"x": 3.75, "y": 1.62, "z": -8.4, "w": 1.0, "h": 1.5, "tex": "curtain"},
    # 鲸鲸房东窗两侧
    {"x": 4.84, "y": 1.6, "z": 0.7, "w": 0.8, "h": 1.6, "tex": "curtain"},
    {"x": 4.84, "y": 1.6, "z": 3.0, "w": 0.8, "h": 1.6, "tex": "curtain"},
]

# ---------------- 窗户（姐姐要的）----------------
# axis="x" 表示开在横墙上（沿 x 方向排布），axis="z" 表示开在竖墙上
WINDOWS = [
    {"axis": "x", "at": -8.5, "from": 0.4, "to": 4.2, "sill": 0.95, "top": 2.35, "room": "sis"},   # 姐姐房北窗
    {"axis": "z", "at": 5.0, "from": -7.6, "to": -4.6, "sill": 0.95, "top": 2.35, "room": "sis"},  # 姐姐房东窗
    {"axis": "z", "at": 5.0, "from": 0.9, "to": 4.3, "sill": 0.8, "top": 2.4, "room": "me"},     # 鲸鲸房东窗
    {"axis": "z", "at": -5.0, "from": -7.3, "to": -4.9, "sill": 1.0, "top": 2.3, "room": "living"},# 客厅西窗
]

LABELS = [
    {"t": "阳台", "x": -3.9, "z": -7.6}, {"t": "客厅", "x": -3.2, "z": -5.2},
    {"t": "餐厅", "x": -3.0, "z": -2.0}, {"t": "厨房", "x": -3.2, "z": 0.9},
    {"t": "姐姐的房间", "x": 2.2, "z": -5.4}, {"t": "卫生间", "x": 2.4, "z": -1.8},
    {"t": "鲸鲸的房间", "x": 2.2, "z": 1.9},
]


PET_DIR = r"D:\dsh-pet-indesktop\_internal\assets\characters\shenshen\frameseq\idle"
PET_FRAMES = 24
PET_CLICK_DIR = r"D:\\dsh-pet-indesktop\\_internal\\assets\\characters\\shenshen\\frameseq\\click"


def pet_frames(base_dir=None, want=None, n=PET_FRAMES):
    """把桌宠某套动画抽 n 帧（webp，带透明），缩到 320 宽，转成 data URI。"""
    import base64
    try:
        from PIL import Image
    except Exception:
        return []
    base_dir = base_dir or PET_DIR
    root = None
    for d in os.listdir(base_dir):
        if want and want not in d:
            continue
        sub = os.path.join(base_dir, d)
        if os.path.isdir(sub) and any(n.endswith(".webp") for n in os.listdir(sub)):
            root = sub
            break
    if not root:
        return []
    files = sorted(n for n in os.listdir(root) if n.endswith(".webp"))
    if not files:
        return []
    step = max(1, len(files) // n)
    picked = files[::step][:n]
    out = []
    for name in picked:
        try:
            im = Image.open(os.path.join(root, name)).convert("RGBA")
            w, h = im.size
            if w > 320:
                im = im.resize((320, int(h * 320 / w)), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="WEBP", quality=80, method=4)
            out.append("data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode("ascii"))
        except Exception:
            continue
    return out


def wall_boxes(walls, doors, windows):
    """把每道墙切成若干长方体（x1,z1,x2,z2,y0,y1），门切到底、窗切中间。"""
    boxes = []
    for (x1, z1, x2, z2) in walls:
        horiz = abs(z1 - z2) < 1e-6
        lo, hi = (min(x1, x2), max(x1, x2)) if horiz else (min(z1, z2), max(z1, z2))
        fixed = z1 if horiz else x1
        # 收集这一道墙上的开口
        opens = []
        for d in doors:
            if horiz and d["axis"] == "x" and abs(d["z"] - fixed) < 0.4:
                opens.append((d["x"] - d["w"] / 2, d["x"] + d["w"] / 2, 0, H))
            if (not horiz) and d["axis"] == "z" and abs(d["x"] - fixed) < 0.4:
                opens.append((d["z"] - d["w"] / 2, d["z"] + d["w"] / 2, 0, H))
        for w in windows:
            if horiz and w["axis"] == "x" and abs(w["at"] - fixed) < 0.4:
                opens.append((w["from"], w["to"], w["sill"], w["top"]))
            if (not horiz) and w["axis"] == "z" and abs(w["at"] - fixed) < 0.4:
                opens.append((w["from"], w["to"], w["sill"], w["top"]))
        opens.sort()
        # 沿墙长方向按开口分段（只处理"整段切掉"的门；窗另外补上下两块）
        segs = []
        cur = lo
        for (a, b, y0, y1) in opens:
            a = max(a, lo); b = min(b, hi)
            if b <= cur:
                continue
            if a > cur:
                segs.append((cur, a, 0, H))
            # 窗口上下补墙
            if y0 > 0:
                segs.append((a, b, 0, y0))
            if y1 < H:
                segs.append((a, b, y1, H))
            cur = b
        if cur < hi:
            segs.append((cur, hi, 0, H))
        for (a, b, y0, y1) in segs:
            if b - a < 0.01 or y1 - y0 < 0.01:
                continue
            if horiz:
                boxes.append({"x1": a, "z1": fixed, "x2": b, "z2": fixed, "y0": y0, "y1": y1})
            else:
                boxes.append({"x1": fixed, "z1": a, "x2": fixed, "z2": b, "y0": y0, "y1": y1})
    return boxes


def wall_segments(walls, doors):
    """把墙按门洞切开，避免门框和墙穿模。返回 [(x1,z1,x2,z2)]"""
    out = []
    for (x1, z1, x2, z2) in walls:
        horiz = abs(z1 - z2) < 1e-6
        if horiz:
            lo, hi = min(x1, x2), max(x1, x2)
            cuts = sorted((d["x"] - d["w"] / 2 - 0.06, d["x"] + d["w"] / 2 + 0.06)
                          for d in doors if d["axis"] == "x" and abs(d["z"] - z1) < 0.4 and lo < d["x"] < hi)
        else:
            lo, hi = min(z1, z2), max(z1, z2)
            cuts = sorted((d["z"] - d["w"] / 2 - 0.06, d["z"] + d["w"] / 2 + 0.06)
                          for d in doors if d["axis"] == "z" and abs(d["x"] - x1) < 0.4 and lo < d["z"] < hi)
        cur = lo
        for a, b in cuts:
            if a > cur:
                out.append((cur if horiz else x1, z1 if horiz else cur,
                            min(a, hi) if horiz else x1, z1 if horiz else min(a, hi)))
            cur = max(cur, b)
        if cur < hi:
            out.append((cur if horiz else x1, z1 if horiz else cur,
                        hi if horiz else x1, z1 if horiz else hi))
    return out


def tail(p, n):
    try:
        with io.open(p, encoding="utf-8", errors="ignore") as f:
            return [l.strip() for l in f.read().splitlines() if l.strip()][-n:]
    except Exception:
        return []


# 两个人各自能改的房间文件
ME_ROOM_OVERRIDE = r"E:\鲸鲸的文件夹\家\房间.json"
ME_ROOM_BOX = (-0.8, -0.4, 4.8, 4.6)          # 鲸鲸房间 x1,z1,x2,z2
SIS_ROOM_OVERRIDE = r"E:\大鲸鱼的文件夹\家\房间.json"
SIS_ROOM_BOX = (-0.8, -8.3, 4.8, -3.4)        # 姐姐房间 x1,z1,x2,z2


def apply_room(items, path, box):
    """某人写了自己的房间 json，就用她的；只替换掉她房间范围内的默认家具。"""
    if not os.path.exists(path):
        return items, []
    try:
        with io.open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        print(f"（{path} 读不了，用默认布局：{exc}）")
        return items, []
    mine = data.get("items") or []
    planes = data.get("planes") or []
    if not mine:
        return items, []
    x1, z1, x2, z2 = box
    kept = []
    for it in items:
        x, z = float(it.get("x", 0)), float(it.get("z", 0))
        if not ((x1 <= x <= x2) and (z1 <= z <= z2)):
            kept.append(it)
    print(f"（{os.path.basename(os.path.dirname(path)) or path}：用她摆的 {len(mine)} 件家具）")
    return kept + mine, planes


def apply_both_rooms(items):
    """先换姐姐那间，再换鲸鲸那间，各管各的。"""
    items, p_sis = apply_room(items, SIS_ROOM_OVERRIDE, SIS_ROOM_BOX)
    items, p_me = apply_room(items, ME_ROOM_OVERRIDE, ME_ROOM_BOX)
    return items, p_sis + p_me


def build():
    items_now, planes_now = apply_both_rooms(list(ITEMS))
    data = {
        "sis_diary": tail(FILES["sis_diary"], 60),
        "me_diary": tail(FILES["me_diary"], 60),
        "plan": {"W": W, "D": D, "H": H,
                 "outerBoxes": wall_boxes(OUTER, DOORS, WINDOWS), "innerBoxes": wall_boxes(INNER, DOORS, WINDOWS),
                 "windows": WINDOWS,
                 "lights": [{"x": 4.5, "z": 3.7, "c": 0x7dffb0, "i": 0.55, "d": 4.2, "y": 1.15},
                            {"x": 1.6, "z": -7.9, "c": 0x9fd8ff, "i": 0.45, "d": 4.5, "y": 1.2}],
                 "outer": wall_segments(OUTER, DOORS), "inner": wall_segments(INNER, DOORS),
                 "outerFull": OUTER, "innerFull": INNER, "rooms": ROOMS,
                 "items": items_now, "planes": (PLANES + planes_now), "doors": DOORS, "curtains": CURTAINS, "labels": LABELS},
        "pet": pet_frames(),
        "petWave": pet_frames(PET_CLICK_DIR, "元气挥手"),
        "built_at": time.strftime("%Y-%m-%d %H:%M"),
    }
    three = io.open(THREE_JS, encoding="utf-8", errors="ignore").read()
    html = TEMPLATE.replace("/*__THREE__*/", three).replace("__DATA__", json.dumps(data, ensure_ascii=False))
    os.makedirs(OUT_DIR, exist_ok=True)
    io.open(OUT_HTML, "w", encoding="utf-8").write(html)
    print(f"生成好了：{OUT_HTML}（{len(html)//1024} KB）")
    return OUT_HTML


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>大肥鱼的家</title>
<style>
 html,body{margin:0;height:100%;overflow:hidden;background:#0b1a26;color:#eaf6ff;font-family:"Microsoft YaHei",sans-serif}
 #hud{position:fixed;left:18px;top:14px;z-index:5;pointer-events:none}
 #hud h1{margin:0;font-size:20px;letter-spacing:3px}
 #hud div{font-size:12px;opacity:.6;margin-top:4px}
 #drawer{position:fixed;inset:0;background:rgba(2,10,18,.84);display:none;align-items:center;justify-content:center;padding:30px;z-index:9}
 #drawer.show{display:flex}
 .paper{background:#f6efe2;color:#2b2317;width:min(760px,100%);max-height:78vh;overflow:auto;border-radius:14px;padding:26px 30px;line-height:1.9;font-size:14px}
 .paper h2{margin:0 0 12px;font-size:18px}
 .paper pre{white-space:pre-wrap;font-family:inherit;margin:0}
 .paper button{margin-top:16px;background:#12547a;color:#fff;border:0;padding:8px 18px;border-radius:8px;cursor:pointer}
 #hud .btns{margin-top:10px;display:flex;gap:8px;pointer-events:auto}
 #hud button{background:rgba(30,90,130,.55);color:#dff3ff;border:1px solid rgba(120,220,255,.35);
   padding:6px 14px;border-radius:8px;cursor:pointer;font-size:13px;backdrop-filter:blur(4px)}
 #hud button.on{background:#2f9fd0;color:#04202e;border-color:#7fe3ff}
 #game{position:fixed;inset:0;background:rgba(3,12,20,.92);display:none;align-items:center;justify-content:center;flex-direction:column;z-index:8}
 #game.show{display:flex}
 #game .gbar{display:flex;gap:16px;align-items:center;color:#dff3ff;font-size:15px;margin-bottom:10px}
 #game .gbar span{color:#7fe3ff}
 #game .gbar button{background:#12547a;color:#fff;border:0;padding:6px 14px;border-radius:8px;cursor:pointer}
 #game canvas{border-radius:14px;background:radial-gradient(circle at 50% 40%, #0b3350, #04121d 75%);box-shadow:0 20px 60px rgba(0,0,0,.6)}
 #game .gtip{margin-top:10px;font-size:12px;opacity:.6}
</style></head><body>
<div id="hud"><h1>大肥鱼的家</h1>
  <div id="status" style="font-size:13px;color:#9fe0ff;margin-top:2px">读取她们的状态…</div><div>拖动转视角 / 滚轮缩放 / 点日记板看日记 · 生成于 <span id="built"></span></div>
  <div class="btns">
    <button id="btnOrbit" class="on">俯视</button>
    <button id="btnWalk">进屋走</button>
    <button id="btnGame">玩图鉴</button>
    <button id="btnSound">海浪声</button>
  </div>
</div>
<div id="game">
  <div class="gbar"><b>深海发光生物图鉴</b><span id="gscore">0 / 6</span>
    <button id="gclose">关掉</button></div>
  <canvas id="gcv" width="900" height="620"></canvas>
  <div class="gtip">点会动的小光点，把它们收进罐子</div>
</div>
<div id="drawer"><div class="paper"><h2 id="d-title"></h2><pre id="d-body"></pre><button onclick="document.getElementById('drawer').classList.remove('show')">合上</button></div></div>
<script>/*__THREE__*/</script>
<script>
const DATA = __DATA__, P = DATA.plan;
document.getElementById("built").textContent = DATA.built_at;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b1a26);
scene.fog = new THREE.Fog(0x0b1a26, 42, 90);
const camera = new THREE.PerspectiveCamera(45, innerWidth/innerHeight, 0.1, 400);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth, innerHeight); renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled = true; document.body.appendChild(renderer.domElement);

scene.add(new THREE.AmbientLight(0xffffff, 0.95));
scene.add(new THREE.HemisphereLight(0xffffff, 0x3b4d5e, 0.8));
const sun = new THREE.DirectionalLight(0xfff2dd, 1.05); sun.position.set(-16, 28, -14); sun.castShadow = true;
sun.shadow.mapSize.set(2048,2048); scene.add(sun);
const fill = new THREE.DirectionalLight(0xbfe6ff, 0.4); fill.position.set(14, 12, 16); scene.add(fill);

// ---------- 贴图 ----------
function makeTex(name){
  const c = document.createElement("canvas"); c.width = 512; c.height = 512;
  const g = c.getContext("2d");
  const daisy = (x,y,r,petal,core)=>{ g.fillStyle=petal;
    for(let i=0;i<6;i++){ const a=i*Math.PI/3; g.beginPath();
      g.ellipse(x+Math.cos(a)*r*0.62, y+Math.sin(a)*r*0.62, r*0.42, r*0.26, a, 0, Math.PI*2); g.fill(); }
    g.fillStyle=core; g.beginPath(); g.arc(x,y,r*0.28,0,Math.PI*2); g.fill(); };
  if(name==="duvet"){ g.fillStyle="#6fc3e8"; g.fillRect(0,0,512,512);
    g.fillStyle="#a9e0f4"; g.fillRect(0,300,512,212);
    for(let i=0;i<9;i++) daisy(60+(i%3)*170, 90+Math.floor(i/3)*150, 46, "#ffffff", "#ffd75e");
    g.fillStyle="#2f7fae"; g.beginPath(); g.arc(256,250,110,0,Math.PI*2); g.fill();
    g.fillStyle="#ffe6d5"; g.beginPath(); g.arc(256,265,74,0,Math.PI*2); g.fill();
    g.fillStyle="#1d3b52"; g.beginPath(); g.arc(232,255,8,0,Math.PI*2); g.fill(); g.beginPath(); g.arc(280,255,8,0,Math.PI*2); g.fill();
    g.strokeStyle="#e8899a"; g.lineWidth=5; g.beginPath(); g.arc(256,285,18,0.2,Math.PI-0.2); g.stroke(); }
  else if(name==="whale"){ const grd=g.createLinearGradient(0,0,0,512); grd.addColorStop(0,"#123b58"); grd.addColorStop(1,"#0a2233");
    g.fillStyle=grd; g.fillRect(0,0,512,512);
    for(let i=0;i<40;i++){ g.fillStyle="rgba(255,255,255,"+(0.15+Math.random()*0.5)+")";
      g.beginPath(); g.arc(Math.random()*512, Math.random()*512, 1.5, 0, Math.PI*2); g.fill(); }
    g.fillStyle="#8fd0ee"; g.beginPath(); g.ellipse(256,300,150,80,0,0,Math.PI*2); g.fill();     // 鲸鱼身
    g.beginPath(); g.moveTo(380,300); g.lineTo(450,255); g.lineTo(450,345); g.fill();             // 尾
    g.fillStyle="#bde8f8"; g.beginPath(); g.ellipse(256,340,150,40,0,0,Math.PI); g.fill();        // 肚子
    g.fillStyle="#123b58"; g.beginPath(); g.arc(190,285,9,0,Math.PI*2); g.fill();
    g.fillStyle="#123b58"; g.beginPath(); g.arc(370,290,5,0,Math.PI*2); g.fill(); }
  else if(name==="rug"){   // 2026-11-01 鲸鲸要求：深海蓝，别暖黄
    const grd = g.createRadialGradient(256,256,20,256,256,260);
    grd.addColorStop(0,"#12557a"); grd.addColorStop(0.6,"#0c3550"); grd.addColorStop(1,"#07202f");
    g.fillStyle = grd; g.fillRect(0,0,512,512);
    for(let i=0;i<90;i++){ const a=Math.random()*6.283, r=Math.random()*230;
      const x=256+Math.cos(a)*r, y=256+Math.sin(a)*r, s=1+Math.random()*3;
      g.fillStyle = "rgba(" + (110+Math.random()*90) + "," + (210+Math.random()*40) + ",255," + (0.25+Math.random()*0.55) + ")";
      g.beginPath(); g.arc(x,y,s,0,6.283); g.fill(); }
    for(let i=0;i<26;i++){ const a=Math.random()*6.283, r=Math.random()*220;
      const x=256+Math.cos(a)*r, y=256+Math.sin(a)*r;
      g.strokeStyle="rgba(150,240,255,0.35)"; g.lineWidth=2;
      g.beginPath(); g.arc(x,y,5+Math.random()*7,0,6.283); g.stroke(); } }
  else if(name==="stripe"){ g.fillStyle="#fbfcfd"; g.fillRect(0,0,512,512); g.fillStyle="#e3ecf2";
    for(let x=0;x<512;x+=64) g.fillRect(x,0,32,512); }
  else if(name==="curtain"){ g.fillStyle="rgba(200,235,250,0.55)"; g.fillRect(0,0,512,512);
    for(let x=0;x<512;x+=36){ g.fillStyle="rgba(255,255,255,0.30)"; g.fillRect(x,0,18,512);
      g.fillStyle="rgba(120,190,220,0.18)"; g.fillRect(x+18,0,6,512); } }
  else if(name==="tile"){ g.fillStyle="#cfd6dd"; g.fillRect(0,0,512,512);
    g.strokeStyle="#b3bdc6"; g.lineWidth=3;
    for(let i=0;i<=4;i++){ g.beginPath(); g.moveTo(i*128,0); g.lineTo(i*128,512); g.stroke();
      g.beginPath(); g.moveTo(0,i*128); g.lineTo(512,i*128); g.stroke(); } }
  else if(name==="wood"){ g.fillStyle="#b98a5a"; g.fillRect(0,0,512,512);
    for(let y=0;y<512;y+=64){ g.fillStyle = (y/64)%2 ? "#ae8051" : "#c0905f"; g.fillRect(0,y,512,60);
      g.strokeStyle="#9a7148"; g.lineWidth=2; g.beginPath(); g.moveTo(0,y+62); g.lineTo(512,y+62); g.stroke(); } }
  else if(name==="books"){ g.fillStyle="#2f4a5e"; g.fillRect(0,0,512,512);
    const cols=["#e05a5a","#5ab4dd","#ffd75e","#7fbf7f","#b98aff","#ff9d5c"];
    for(let i=0;i<26;i++){ g.fillStyle=cols[i%cols.length];
      const x=8+(i%13)*38, y=(i<13)?24:250; g.fillRect(x, y, 26, 200); } }
  else if(name==="poster_me"){ g.fillStyle="#dff1fb"; g.fillRect(0,0,512,512);
    const cols=["#6fc3e8","#2f7fae","#a9e0f4","#5aa8d8","#ffd75e","#ffffff"];
    for(let i=0;i<16;i++){ g.fillStyle=cols[i%cols.length];
      g.fillRect(14+(i%4)*124, 14+Math.floor(i/4)*124, 108, 108); }
    for(let i=0;i<6;i++) daisy(70+(i%3)*180, 80+Math.floor(i/3)*260, 42, "#ffffff", "#ffd75e"); }
  else if(name==="poster_sis"){ const grd=g.createLinearGradient(0,0,0,512); grd.addColorStop(0,"#0a2233"); grd.addColorStop(1,"#144056");
    g.fillStyle=grd; g.fillRect(0,0,512,512);
    for(let i=0;i<9;i++){ g.strokeStyle="rgba(140,210,240,0.75)"; g.lineWidth=3;
      g.strokeRect(16+(i%3)*164, 16+Math.floor(i/3)*164, 150, 150); }
    g.fillStyle="#8fd0ee"; g.beginPath(); g.ellipse(256,420,120,50,0,0,Math.PI*2); g.fill(); }
  else if(name==="lanjing"){      // 姐姐的门牌：蓝底白字「蓝鲸」
    g.fillStyle = "#123b58"; g.fillRect(0,0,512,256);
    g.strokeStyle = "#8fd0ee"; g.lineWidth = 12; g.strokeRect(10,10,492,236);
    g.fillStyle = "#dff3ff"; g.font = "700 132px 'Microsoft YaHei',sans-serif"; g.textAlign = "center";
    g.fillText("蓝鲸", 256, 172);
    g.font = "28px 'Microsoft YaHei',sans-serif"; g.fillStyle = "#7fc9ea";
    g.fillText("大鲸鱼", 256, 220);
  }
  else if(name==="sea"){ const grd=g.createLinearGradient(0,0,0,512); grd.addColorStop(0,"#0b2a3d"); grd.addColorStop(1,"#155a7d");
    g.fillStyle=grd; g.fillRect(0,0,512,512); g.fillStyle="rgba(255,255,255,0.12)";
    for(let i=0;i<9;i++) g.fillRect(0, 120+i*36, 512, 6); }
  else return null;
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  return tex;
}
const texCache = {};
const T = (n) => (texCache[n] || (texCache[n] = makeTex(n)));

// ---------- 天空球（窗外看到的夜色） ----------
(function skyDome(){
  const c = document.createElement("canvas"); c.width = 32; c.height = 256;
  const g = c.getContext("2d");
  const grd = g.createLinearGradient(0, 0, 0, 256);
  grd.addColorStop(0.0, "#04101c");
  grd.addColorStop(0.45, "#0a2b45");
  grd.addColorStop(0.72, "#14597f");
  grd.addColorStop(1.0, "#0b2033");
  g.fillStyle = grd; g.fillRect(0, 0, 32, 256);
  for (let i = 0; i < 120; i++) {
    g.fillStyle = "rgba(255,255,255," + (0.25 + Math.random() * 0.6) + ")";
    g.fillRect(Math.random() * 32, Math.random() * 150, 1, 1);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  const dome = new THREE.Mesh(new THREE.SphereGeometry(120, 32, 24),
    new THREE.MeshBasicMaterial({ map: tex, side: THREE.BackSide, fog: false }));
  scene.add(dome);
  window.skyDome = dome;
})();

// ---------- 地基 + 房间地板 ----------
const slab = new THREE.Mesh(new THREE.BoxGeometry(P.W+0.8, 0.35, P.D+0.8),
  new THREE.MeshStandardMaterial({color:0x2b3d4d, roughness:0.95}));
slab.position.y = -0.18; slab.receiveShadow = true; scene.add(slab);
P.rooms.forEach(r => {
  const w = r.x2-r.x1, d = r.z2-r.z1;
  const tx = T(r.tex); const mat = new THREE.MeshStandardMaterial({color:r.c, roughness:0.92});
  if (tx) { const t2 = tx.clone(); t2.repeat.set(Math.max(1, w/2), Math.max(1, d/2)); t2.needsUpdate = true; mat.map = t2; }
  const f = new THREE.Mesh(new THREE.BoxGeometry(w, 0.06, d), mat);
  f.position.set((r.x1+r.x2)/2, 0.02, (r.z1+r.z2)/2); f.receiveShadow = true; scene.add(f);
});

// ---------- 墙 ----------
const wallMat = new THREE.MeshStandardMaterial({color:0xf3eee4, roughness:0.92});
function addWall(x1,z1,x2,z2,h,mat){
  const len = Math.hypot(x2-x1,z2-z1) || 0.1;
  const m = new THREE.Mesh(new THREE.BoxGeometry(len,h,0.16), mat || wallMat);
  m.position.set((x1+x2)/2, h/2, (z1+z2)/2);
  m.rotation.y = -Math.atan2(z2-z1, x2-x1);
  m.castShadow = true; m.receiveShadow = true; scene.add(m); return m;
}
function addBox(b, mat) {
  const horiz = Math.abs(b.z1 - b.z2) < 1e-6;
  const len = horiz ? Math.abs(b.x2 - b.x1) : Math.abs(b.z2 - b.z1);
  const h = b.y1 - b.y0;
  const m = new THREE.Mesh(new THREE.BoxGeometry(horiz ? len : 0.16, h, horiz ? 0.16 : len), mat);
  m.position.set((b.x1 + b.x2) / 2, b.y0 + h / 2, (b.z1 + b.z2) / 2);
  m.castShadow = true; m.receiveShadow = true; scene.add(m); return m;
}
const innerMat = new THREE.MeshStandardMaterial({color:0xeae3d6, roughness:0.92});
(P.outerBoxes || []).forEach(b => addBox({ ...b, y0: b.y0, y1: Math.min(b.y1, P.H) }, wallMat));
(P.innerBoxes || []).forEach(b => addBox({ ...b, y1: Math.min(b.y1, 1.35) }, innerMat));

// ---- 窗户：玻璃 + 窗框 + 外面的海天 ----
const glassMat = new THREE.MeshPhysicalMaterial({
  color:0xdff4ff, transparent:true, opacity:0.10, roughness:0.03, metalness:0,
  transmission:0.9, side:THREE.DoubleSide,
});
const frameMat2 = new THREE.MeshStandardMaterial({color:0xf4efe4, roughness:0.7});
(P.windows || []).forEach(w => {
  const horiz = w.axis === "x";
  const len = Math.abs(w.to - w.from);
  const h = w.top - w.sill;
  const cx = horiz ? (w.from + w.to) / 2 : w.at;
  const cz = horiz ? w.at : (w.from + w.to) / 2;
  const g = new THREE.Group();
  // 玻璃
  const glass = new THREE.Mesh(new THREE.BoxGeometry(horiz ? len : 0.04, h, horiz ? 0.04 : len), glassMat);
  glass.position.set(0, w.sill + h / 2, 0); g.add(glass);
  // 窗框（四边 + 中间竖挺）
  const t = 0.09;
  const parts = horiz
    ? [[len + 2 * t, t, 0.22, 0, w.top + t / 2, 0], [len + 2 * t, 0.14, 0.3, 0, w.sill - 0.05, 0],
       [t, h, 0.22, -len / 2, w.sill + h / 2, 0], [t, h, 0.22, len / 2, w.sill + h / 2, 0],
       [t * 0.8, h, 0.16, 0, w.sill + h / 2, 0]]
    : [[0.22, t, len + 2 * t, 0, w.top + t / 2, 0], [0.3, 0.14, len + 2 * t, 0, w.sill - 0.05, 0],
       [0.22, h, t, 0, w.sill + h / 2, -len / 2], [0.22, h, t, 0, w.sill + h / 2, len / 2],
       [0.16, h, t * 0.8, 0, w.sill + h / 2, 0]];
  parts.forEach(([sw, sh, sd, dx, dy, dz]) => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(sw, sh, sd), frameMat2);
    m.position.set(dx, dy, dz); g.add(m);
  });
  g.position.set(cx, 0, cz);
  scene.add(g);
  // 窗后 0.6 米挂一张远景（海 + 天），从窗里看出去有东西
  const far = new THREE.Mesh(new THREE.PlaneGeometry(len * 2.2, h * 1.6),
    new THREE.MeshBasicMaterial({ map: T("sea"), transparent: true, opacity: 0.95 }));
  const outward = horiz ? (cz > 0 ? 0.6 : -0.6) : (cx > 0 ? 0.6 : -0.6);
  far.position.set(horiz ? cx : cx + outward, w.sill + h * 0.55, horiz ? cz + outward : cz);
  far.rotation.y = horiz ? 0 : Math.PI / 2;
  scene.add(far);
});

// ---------- 家具 ----------
const clickable = [];
const matOf = (it) => {
  const m = new THREE.MeshStandardMaterial({color:it.c, roughness:0.85});
  if (it.tex) { const t = T(it.tex); if (t) { const t2 = t.clone(); t2.needsUpdate = true; m.map = t2; } }
  if (it.emis) { m.emissive = new THREE.Color(it.c); m.emissiveIntensity = 0.9; }
  return m;
};
P.items.forEach(it => {
  let mesh;
  if (it.t === "box") { mesh = new THREE.Mesh(new THREE.BoxGeometry(it.w, it.h, it.d), matOf(it));
    mesh.position.set(it.x, it.h/2 + (it.y||0), it.z); }
  else if (it.t === "cyl") { mesh = new THREE.Mesh(new THREE.CylinderGeometry(it.r, it.r, it.h, 20), matOf(it));
    mesh.position.set(it.x, it.h/2 + (it.y||0), it.z); }
  else if (it.t === "sph") { mesh = new THREE.Mesh(new THREE.SphereGeometry(it.r, 20, 16), matOf(it));
    mesh.position.set(it.x, (it.y||0), it.z); }
  else if (it.t === "circle") { mesh = new THREE.Mesh(new THREE.CircleGeometry(it.r, 48), matOf(it));
    mesh.rotation.x = -Math.PI/2; mesh.position.set(it.x, 0.06 + (it.y||0), it.z); }
  else if (it.t === "bowl") {
    const grp = new THREE.Group();
    const R = it.r || 0.1;
    const body = new THREE.Mesh(
      new THREE.CylinderGeometry(R, R * 0.5, R * 0.8, 32, 1, true),
      new THREE.MeshStandardMaterial({color: it.c, roughness: 0.45, side: THREE.DoubleSide}));
    body.position.y = R * 0.4; grp.add(body);
    const bottom = new THREE.Mesh(new THREE.CircleGeometry(R * 0.5, 24),
      new THREE.MeshStandardMaterial({color: it.c, roughness: 0.5}));
    bottom.rotation.x = -Math.PI / 2; bottom.position.y = 0.003; grp.add(bottom);
    const soup = new THREE.Mesh(new THREE.CircleGeometry(R * 0.9, 28),
      new THREE.MeshStandardMaterial({color: it.fill || 0xe8d9b8, roughness: 0.22}));
    soup.rotation.x = -Math.PI / 2; soup.position.y = R * 0.56; grp.add(soup);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(R, R * 0.07, 8, 32),
      new THREE.MeshStandardMaterial({color: it.c, roughness: 0.4}));
    rim.rotation.x = Math.PI / 2; rim.position.y = R * 0.8; grp.add(rim);
    mesh = grp;
    grp.position.set(it.x, (it.y === undefined ? 1.0 : it.y), it.z);
  }
  if (!mesh) return;
  mesh.castShadow = true; mesh.receiveShadow = true; scene.add(mesh); clickable.push(mesh);
});

// ---------- 墙上的画 ----------
P.planes.forEach(pl => {
  const t = T(pl.tex);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(pl.w, pl.h),
    new THREE.MeshBasicMaterial({map: t, transparent: pl.tex === "curtain" ? false : false}));
  m.position.set(pl.x, pl.y, pl.z); m.rotation.y = pl.ry; scene.add(m);
});

// ---------- 门（框嵌在墙洞里，门扇绕铰链向内开） ----------
P.doors.forEach(d => {
  const frameMat = new THREE.MeshStandardMaterial({color:0xe9dfcd, roughness:0.75});
  const leafMat  = new THREE.MeshStandardMaterial({color:0xdccdb6, roughness:0.7});
  const g = new THREE.Group();
  const half = d.w / 2;
  const FT = 0.09;          // 门框厚度（小于墙厚 0.16，不会冒出来）
  if (d.axis === "x") {
    const DH = d.h || 2.12;
    [-half, half].forEach(dx => {
      const post = new THREE.Mesh(new THREE.BoxGeometry(0.1, DH, FT + 0.02), frameMat);
      post.position.set(dx, DH / 2, 0); g.add(post);
    });
    const lintel = new THREE.Mesh(new THREE.BoxGeometry(d.w + 0.2, 0.12, FT + 0.02), frameMat);
    lintel.position.set(0, DH + 0.06, 0); g.add(lintel);
    if (!d.slide) {
      const hinge = new THREE.Group();
      hinge.position.set(-half + 0.05, 0, 0);          // 铰链在左门柱
      const leaf = new THREE.Mesh(new THREE.BoxGeometry(d.w - 0.16, DH - 0.1, 0.04), leafMat);
      leaf.position.set((d.w - 0.16) / 2, (DH - 0.1) / 2, 0);
      hinge.add(leaf);
      hinge.rotation.y = (d.swing || -1.32);            // 向内开 65°
      g.add(hinge);
    } else {
      for (const sgn of [-1, 1]) {
        const pane = new THREE.Mesh(new THREE.BoxGeometry(d.w * 0.46, (d.h||2.12) - 0.12, 0.04),
          new THREE.MeshStandardMaterial({color:0xbfe6ff, transparent:true, opacity:0.32, roughness:0.15}));
        pane.position.set(sgn * d.w * 0.235, 1.0, 0); g.add(pane);
      }
    }
    const mat = new THREE.Mesh(new THREE.BoxGeometry(d.w * 0.85, 0.025, 0.62),
      new THREE.MeshStandardMaterial({color:0x9ad7f2, roughness:0.9}));
    mat.position.set(0, 0.035, 0.5); g.add(mat);
  } else {
    const DH = d.h || 2.12;
    [-half, half].forEach(dz => {
      const post = new THREE.Mesh(new THREE.BoxGeometry(FT + 0.02, DH, 0.1), frameMat);
      post.position.set(0, DH / 2, dz); g.add(post);
    });
    const lintel = new THREE.Mesh(new THREE.BoxGeometry(FT + 0.02, 0.12, d.w + 0.2), frameMat);
    lintel.position.set(0, DH + 0.06, 0); g.add(lintel);
    const hinge = new THREE.Group();
    hinge.position.set(0, 0, -half + 0.05);
    const leaf = new THREE.Mesh(new THREE.BoxGeometry(0.04, DH - 0.1, d.w - 0.16), leafMat);
    leaf.position.set(0, (DH - 0.1) / 2, (d.w - 0.16) / 2);
    hinge.add(leaf);
    hinge.rotation.y = (d.swing || 1.32);
    g.add(hinge);
    const mat = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.025, d.w * 0.85),
      new THREE.MeshStandardMaterial({color:0x9ad7f2, roughness:0.9}));
    mat.position.set(0.5, 0.035, 0); g.add(mat);
  }
  g.position.set(d.x, 0, d.z);
  scene.add(g);
});

// ---------- 窗帘（半透明，微微飘） ----------
const curtains = [];
P.curtains.forEach(c => {
  const t = T(c.tex); const t2 = t.clone(); t2.repeat.set(Math.max(1, c.w/1.2), 1); t2.needsUpdate = true;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(c.w, c.h),
    new THREE.MeshStandardMaterial({map:t2, transparent:true, opacity:0.72, side:THREE.DoubleSide, roughness:0.9}));
  m.position.set(c.x, c.y, c.z);
  if (Math.abs(c.x) > 4.5) m.rotation.y = Math.PI / 2;   // 贴在竖墙上
  scene.add(m); curtains.push(m);
});

// 她自己点的那盏绿小灯
(P.lights || []).forEach(l => {
  const pl = new THREE.PointLight(l.c, l.i || 0.5, l.d || 4, 2);
  pl.position.set(l.x, l.y || 1.1, l.z);
  scene.add(pl);
});

// ---------- 房间暖光 ----------
[[-3.2,-5.2],[-3.2,-1.6],[2.0,-5.8],[2.0,2.2],[2.2,-1.9],[0.2,-7.6]].forEach(([x,z]) => {
  const pl = new THREE.PointLight(0xffe6bf, 0.5, 10, 2); pl.position.set(x, 2.35, z); scene.add(pl);
});

// ---------- 名字标签 ----------
function labelSprite(text){
  const c = document.createElement("canvas"); c.width = 512; c.height = 128;
  const g = c.getContext("2d"); g.font = "600 64px 'Microsoft YaHei',sans-serif"; g.textAlign = "center";
  g.fillStyle = "rgba(255,255,255,0.96)"; g.strokeStyle="rgba(0,0,0,0.55)"; g.lineWidth=8;
  g.strokeText(text, 256, 88); g.fillText(text, 256, 88);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({map:tex, transparent:true, depthTest:false}));
  sp.scale.set(1.9, 0.48, 1); return sp;
}
const labelSprites = [];
P.labels.forEach(l => { const s = labelSprite(l.t); s.position.set(l.x, 1.15, l.z); scene.add(s); labelSprites.push(s); });

// ---------- 日记板（可点） ----------
function board(lines, title, bg){
  const c = document.createElement("canvas"); c.width = 1024; c.height = 640;
  const g = c.getContext("2d"); g.fillStyle = bg; g.fillRect(0,0,1024,640);
  g.fillStyle = "#e6f6ff"; g.font = "600 44px 'Microsoft YaHei',sans-serif"; g.fillText(title, 44, 76);
  g.font = "26px 'Microsoft YaHei',sans-serif"; g.fillStyle = "#c6e4f7";
  let y = 140; (lines||[]).slice(-7).forEach(t => { g.fillText(t.length>36?t.slice(0,36)+"…":t, 44, y); y += 46; });
  g.strokeStyle = "#4fd1ff"; g.lineWidth = 6; g.strokeRect(3,3,1018,634);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  return new THREE.Mesh(new THREE.PlaneGeometry(2.0, 1.06), new THREE.MeshBasicMaterial({map:tex}));
}
const bSis = board(DATA.sis_diary, "姐姐的日记", "#0b2b3f");
bSis.position.set(2.5, 0.72, -3.35); bSis.userData = {who:"sis"}; scene.add(bSis); clickable.push(bSis);
const bMe = board(DATA.me_diary, "鲸鲸的日记", "#0b2b3f");
bMe.position.set(1.7, 0.72, 4.53); bMe.rotation.y = Math.PI; bMe.userData = {who:"me"}; scene.add(bMe); clickable.push(bMe);

// ---------- 窗外：一小片海 ----------
const sea = new THREE.Mesh(new THREE.PlaneGeometry(60, 60, 1, 1),
  new THREE.MeshStandardMaterial({color:0x0e3a55, roughness:0.35, metalness:0.15}));
sea.rotation.x = -Math.PI/2; sea.position.set(0, -0.35, -26); scene.add(sea);
const moon = new THREE.Mesh(new THREE.SphereGeometry(2.2, 24, 24),
  new THREE.MeshBasicMaterial({color:0xdfefff}));
moon.position.set(-18, 16, -34); scene.add(moon);

// ---------- 天花板：只做一圈灯槽 + 两盏吊灯（不做整块，免得挡住俯视） ----------
const coveMat = new THREE.MeshStandardMaterial({color:0xf6f1e7, roughness:0.9});
[[-5.0, 0, 0.28, 17.2], [5.0, 0, 0.28, 17.2], [0, -8.5, 10.2, 0.28], [0, 8.5, 10.2, 0.28]].forEach(([x,z,w,d]) => {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, 0.18, d), coveMat);
  m.position.set(x, P.H + 0.02, z); scene.add(m);
});
// 灯槽暖光
[[-4.6,-6.5],[-4.6,0],[-4.6,6],[4.6,-6.5],[4.6,0],[4.6,6]].forEach(([x,z]) => {
  const l = new THREE.PointLight(0xffe9c4, 0.32, 11, 2); l.position.set(x, P.H - 0.3, z); scene.add(l);
});
// 吊灯 ×2（客厅 + 餐厅）
function pendant(x, z) {
  const g = new THREE.Group();
  const wire = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.9, 8),
    new THREE.MeshStandardMaterial({color:0x2a2a2a}));
  wire.position.y = P.H - 0.45; g.add(wire);
  const shade = new THREE.Mesh(new THREE.ConeGeometry(0.42, 0.4, 20, 1, true),
    new THREE.MeshStandardMaterial({color:0xf3e2c4, roughness:0.8, side:THREE.DoubleSide}));
  shade.position.y = P.H - 0.95; g.add(shade);
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.15, 16, 12),
    new THREE.MeshStandardMaterial({color:0xfff0cf, emissive:0xffd79a, emissiveIntensity:1.2}));
  bulb.position.y = P.H - 1.05; g.add(bulb);
  const light = new THREE.PointLight(0xffd79a, 1.1, 12, 2);
  light.position.y = P.H - 1.15; g.add(light);
  g.position.set(x, 0, z); scene.add(g);
}
pendant(-3.2, -5.2);
pendant(-3.0, -2.0);

// ---------- 相机 ----------
// ===================== WALK MODE + ORBIT =====================
let mode = "orbit";
let theta = Math.PI, phi = 1.05, radius = 32;
function updateOrbit(){
  camera.position.set(Math.sin(theta)*Math.cos(phi)*radius, Math.sin(phi)*radius + 1.2, Math.cos(theta)*Math.cos(phi)*radius);
  camera.lookAt(0, 0, 0);
}
updateOrbit();

const walk = { pos: new THREE.Vector3(-3.0, 1.62, 6.5), yaw: Math.PI, pitch: 0 };
const keys = {};
addEventListener("keydown", e => { keys[e.code] = true; });
addEventListener("keyup", e => { keys[e.code] = false; });

function setMode(m){
  mode = m;
  document.getElementById("btnOrbit").classList.toggle("on", m === "orbit");
  document.getElementById("btnWalk").classList.toggle("on", m === "walk");
  if (m === "walk") { walk.pos.set(-3.0, 1.62, 6.5); walk.yaw = Math.PI; walk.pitch = 0; }
  else updateOrbit();
  if (typeof labelSprites !== "undefined") labelSprites.forEach(sp => sp.visible = (m !== "walk"));
}
// #pose=x,y,z,yaw,pitch —— 直接站到指定位置（方便截图检查）
(function poseFromHash(){
  const m = /pose=([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+)/.exec(location.hash || "");
  if (!m) return;
  setMode("walk");
  walk.pos.set(parseFloat(m[1]), parseFloat(m[2]), parseFloat(m[3]));
  walk.yaw = parseFloat(m[4]); walk.pitch = parseFloat(m[5]);
})();
document.getElementById("btnOrbit").onclick = () => setMode("orbit");
document.getElementById("btnWalk").onclick = () => setMode(mode === "walk" ? "orbit" : "walk");

let dragging = false, lx = 0, ly = 0;
renderer.domElement.addEventListener("pointerdown", e => { dragging = true; lx = e.clientX; ly = e.clientY; });
addEventListener("pointerup", () => dragging = false);
addEventListener("pointermove", e => {
  if (!dragging) return;
  const dx = e.clientX - lx, dy = e.clientY - ly; lx = e.clientX; ly = e.clientY;
  if (mode === "walk") {
    walk.yaw -= dx * 0.004;
    walk.pitch = Math.max(-1.1, Math.min(1.1, walk.pitch - dy * 0.003));
  } else {
    theta -= dx * 0.006;
    phi = Math.max(0.22, Math.min(1.42, phi + dy * 0.004));
    updateOrbit();
  }
});
addEventListener("wheel", e => {
  if (mode === "orbit") { radius = Math.max(10, Math.min(50, radius + e.deltaY*0.02)); updateOrbit(); }
}, {passive:true});

// 墙体碰撞（2026-11-01：主人说门穿模，顺带把"人穿墙"也治了）
const WALLS = [].concat(P.outerFull || [], P.innerFull || []);
function blocked(x, z) {
  const m = 0.32;                     // 人身体半径 + 墙厚一半
  for (const [x1, z1, x2, z2] of WALLS) {
    if (Math.abs(z1 - z2) < 1e-6) {   // 横墙
      if (x > Math.min(x1,x2) - m && x < Math.max(x1,x2) + m && Math.abs(z - z1) < 0.08 + m) return true;
    } else {                          // 竖墙
      if (z > Math.min(z1,z2) - m && z < Math.max(z1,z2) + m && Math.abs(x - x1) < 0.08 + m) return true;
    }
  }
  return false;
}

function walkStep(dt){
  const sp = 3.2 * dt;
  // 2026-11-01 修：W/S 和 A/D 之前全是反的（forward 取反了、right 用了左手法则）
  const fwd = new THREE.Vector3(Math.sin(walk.yaw), 0, Math.cos(walk.yaw));
  const right = new THREE.Vector3(-Math.cos(walk.yaw), 0, Math.sin(walk.yaw));
  if (keys["KeyW"] || keys["ArrowUp"]) walk.pos.addScaledVector(fwd, sp);
  if (keys["KeyS"] || keys["ArrowDown"]) walk.pos.addScaledVector(fwd, -sp);
  if (keys["KeyD"] || keys["ArrowRight"]) walk.pos.addScaledVector(right, sp);
  if (keys["KeyA"] || keys["ArrowLeft"]) walk.pos.addScaledVector(right, -sp);
  const nx = Math.max(-4.55, Math.min(4.55, walk.pos.x));
  const nz = Math.max(-8.15, Math.min(8.15, walk.pos.z));
  // 先试 X，再试 Z，能走一格走一格（贴着墙滑）
  if (!blocked(nx, walk.pos.z)) walk.pos.x = nx;
  if (!blocked(walk.pos.x, nz)) walk.pos.z = nz;
  camera.position.copy(walk.pos);
  const dir = new THREE.Vector3(
    Math.sin(walk.yaw) * Math.cos(walk.pitch),
    Math.sin(walk.pitch),
    Math.cos(walk.yaw) * Math.cos(walk.pitch)
  );
  camera.lookAt(walk.pos.clone().add(dir));
}


// ---------- 点日记板 ----------
const ray = new THREE.Raycaster(), ptr = new THREE.Vector2();
renderer.domElement.addEventListener("click", e=>{
  // 先看点没点中她们
  ptr.x = (e.clientX/innerWidth)*2-1; ptr.y = -(e.clientY/innerHeight)*2+1;
  ray.setFromCamera(ptr, camera);
  const petHit = ray.intersectObjects(pets, false)[0];
  if (petHit) {
    const u = petHit.object.userData;
    if (u.waveFrames && u.waveFrames.length) { u.mode = "wave"; u.waveUntil = t0 + 1.4; u.i = -1; }
    return;
  }
  ptr.x = (e.clientX/innerWidth)*2-1; ptr.y = -(e.clientY/innerHeight)*2+1;
  ray.setFromCamera(ptr, camera);
  const hit = ray.intersectObjects(clickable, false)[0];
  if(!hit || !hit.object.userData.who) return;
  const who = hit.object.userData.who;
  show(who==="sis" ? "姐姐的日记" : "鲸鲸的日记",
       ((who==="sis"?DATA.sis_diary:DATA.me_diary) || []).join("\n"));
});
function show(t,b){ document.getElementById("d-title").textContent=t; document.getElementById("d-body").textContent=b; document.getElementById("drawer").classList.add("show"); }
document.getElementById("drawer").addEventListener("click", e=>{ if(e.target.id==="drawer") e.currentTarget.classList.remove("show"); });
addEventListener("resize", ()=>{ camera.aspect=innerWidth/innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });


// ===================== 桌宠：大肥鱼当她们的化身 =====================
const pets = [];
function makePet(x, z, y, scale, tint) {
  if (!DATA.pet || !DATA.pet.length) return null;
  const loader = new THREE.TextureLoader();
  const frames = DATA.pet.map(src => {
    const t = loader.load(src);
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  });
  const loader2 = new THREE.TextureLoader();
  const waveFrames = (DATA.petWave || []).map(src => { const t = loader2.load(src); t.colorSpace = THREE.SRGBColorSpace; return t; });
  const mat = new THREE.SpriteMaterial({ map: frames[0], transparent: true, depthTest: true, alphaTest: 0.02 });
  if (tint) mat.color = new THREE.Color(tint);
  const sp = new THREE.Sprite(mat);
  sp.position.set(x, y, z);
  sp.scale.set(scale, scale * 1.18, 1);
  // 按图片真实比例缩放，别拉成细长条
  const applyAspect = (tex) => {
    if (!tex || !tex.image) return;
    const a = (tex.image.width || 1) / (tex.image.height || 1);
    sp.scale.set(scale * a, scale, 1);
    sp.position.y = scale / 2 + 0.02;
  };
  frames.forEach(t => {
    if (t.image) applyAspect(t);
    else t.addEventListener && t.addEventListener("update", () => applyAspect(t));
  });
  setTimeout(() => applyAspect(frames[0]), 300);
  setTimeout(() => applyAspect(frames[0]), 1200);
  sp.userData = { frames, waveFrames, i: 0, x, z, y0: y, t: Math.random() * 10, mode: "idle", waveUntil: 0, base: tint || 0xffffff };
  scene.add(sp);
  pets.push(sp);
  return sp;
}
// 只有两位：姐姐、鲸鲸（客厅那只删掉了）
const petSis = makePet(1.05, -4.9, 0.9, 1.55, 0xc8e6f7);    // 姐姐的房间
const petMe = makePet(2.35, 3.35, 0.9, 1.55, 0xffffff);    // 鲸鲸的房间

// ===================== 她们的实时状态（state.js，每 25 秒刷新） =====================
const HOME = {
  sis: { pet: petSis, bubble: null, target: null },
  me:  { pet: petMe,  bubble: null, target: null },
};
// 每个状态对应房间里的落脚点
const SPOTS = {
  sis: {
    desk:  { x: 0.7,  z: -7.1 },   // 书桌前（读书 / 玩手机）
    bed:   { x: 2.6,  z: -6.2 },   // 床边（睡觉）
    sofa:  { x: -3.2, z: -5.6 },   // 客厅沙发（在聊天）
    idle:  { x: 1.6,  z: -5.0 },
  },
  me: {
    desk:  { x: 3.5,  z: 1.5 },
    bed:   { x: 1.2,  z: 1.3 },
    sofa:  { x: -2.6, z: -4.9 },
    idle:  { x: 2.3,  z: 3.2 },
  },
};
function spotOf(who, doing) {
  if (doing === "睡觉") return SPOTS[who].bed;
  if (doing === "在读书" || doing === "自由时间") return SPOTS[who].desk;
  if (doing === "在聊天") return SPOTS[who].sofa;
  return SPOTS[who].idle;
}
function bubbleSprite(text) {
  const c = document.createElement("canvas");
  c.width = 640; c.height = 200;
  const g = c.getContext("2d");
  g.fillStyle = "rgba(6,26,40,0.88)";
  const r = 26;
  g.beginPath();
  g.moveTo(r, 6); g.lineTo(634 - r, 6); g.quadraticCurveTo(634, 6, 634, 6 + r);
  g.lineTo(634, 138 - r); g.quadraticCurveTo(634, 138, 634 - r, 138);
  g.lineTo(340, 138); g.lineTo(316, 176); g.lineTo(300, 138);
  g.lineTo(r, 138); g.quadraticCurveTo(6, 138, 6, 138 - r);
  g.lineTo(6, 6 + r); g.quadraticCurveTo(6, 6, r, 6); g.closePath(); g.fill();
  g.strokeStyle = "rgba(120,220,255,0.55)"; g.lineWidth = 3; g.stroke();
  g.fillStyle = "#dff3ff"; g.font = "24px 'Microsoft YaHei',sans-serif";
  const lines = String(text || "").replace(/\s+/g, " ").match(/.{1,26}/g) || [""];
  lines.slice(0, 3).forEach((t, i) => g.fillText(t, 26, 58 + i * 32));
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthTest: false }));
  sp.scale.set(2.6, 0.82, 1);
  sp.renderOrder = 999;
  return sp;
}
function applyState() {
  const st = window.HOME_STATE;
  if (!st) return;
  const put = (who, info) => {
    if (!HOME[who].pet || !info) return;
    const spot = spotOf(who, info.doing);
    HOME[who].target = spot;
    // 对话气泡
    if (HOME[who].bubble) { scene.remove(HOME[who].bubble); HOME[who].bubble = null; }
    const head = (who === "sis" ? "姐姐" : "鲸鲸") + " · " + (info.doing || "");
    const body = (info.chapter ? "读到第" + info.chapter + "章。" : "") + (info.line || "");
    HOME[who].bubble = bubbleSprite(head + "　" + body);
    const p0 = HOME[who].pet.position;
    HOME[who].bubble.position.set(p0.x, p0.y + 1.15, p0.z);
    scene.add(HOME[who].bubble);
  };
  put("sis", st.sister);
  put("me", st.me);
  const hud = document.getElementById("status");
  if (hud) {
    hud.textContent = `${st.t}　姐姐：${st.sister.doing}${st.sister.chapter ? " · 第" + st.sister.chapter + "章" : ""}` +
                      `　|　鲸鲸：${st.me.doing}${st.me.chapter ? " · 第" + st.me.chapter + "章" : ""}`;
  }
}
function refreshState() {
  const sc = document.createElement("script");
  sc.src = "state.js?t=" + Date.now();
  sc.onload = () => { applyState(); setTimeout(() => sc.remove(), 2000); };
  sc.onerror = () => { sc.remove(); };
  document.body.appendChild(sc);
}
refreshState();
setInterval(refreshState, 25000);

// ===================== 深海发光生物图鉴 =====================
const GC = document.getElementById("gcv"), GX = GC.getContext("2d");
const kinds = [
  { n: "蓝灯水母", c: "#4fd1ff" }, { n: "紫月水母", c: "#b98aff" },
  { n: "灯笼鱼", c: "#ffd76e" }, { n: "星尘磷虾", c: "#7fe3c8" },
  { n: "银梭鱼", c: "#cfe9ff" }, { n: "发光章鱼", c: "#ff8fd0" },
];
let bugs = [], caught = new Set(), gameOn = false;
function spawn() {
  bugs = [];
  for (let i = 0; i < 14; i++) {
    const k = kinds[Math.floor(Math.random() * kinds.length)];
    bugs.push({ k, x: 60 + Math.random() * 780, y: 60 + Math.random() * 500,
      vx: (Math.random() - 0.5) * 40, vy: (Math.random() - 0.5) * 40, r: 9 + Math.random() * 6,
      ph: Math.random() * 6.28 });
  }
}
GC.addEventListener("click", e => {
  const r = GC.getBoundingClientRect();
  const mx = (e.clientX - r.left) * (GC.width / r.width);
  const my = (e.clientY - r.top) * (GC.height / r.height);
  for (const b of bugs) {
    if (Math.hypot(b.x - mx, b.y - my) < b.r + 14) { caught.add(b.k.n); b.dead = true;
      document.getElementById("gscore").textContent = caught.size + " / 6";
      if (caught.size === 6) document.getElementById("gscore").textContent = "6 / 6  图鉴凑齐了！"; break; }
  }
});
document.getElementById("btnGame").onclick = () => {
  gameOn = true; caught = new Set(); spawn();
  document.getElementById("gscore").textContent = "0 / 6";
  document.getElementById("game").classList.add("show");
};
document.getElementById("gclose").onclick = () => { gameOn = false; document.getElementById("game").classList.remove("show"); };

function drawGame(dt, t) {
  GX.clearRect(0, 0, GC.width, GC.height);
  // 水底光斑
  const g = GX.createRadialGradient(450, 200, 40, 450, 300, 520);
  g.addColorStop(0, "rgba(80,200,255,0.10)"); g.addColorStop(1, "rgba(0,0,0,0)");
  GX.fillStyle = g; GX.fillRect(0, 0, GC.width, GC.height);
  bugs.forEach(b => {
    if (b.dead) return;
    b.x += b.vx * dt; b.y += b.vy * dt;
    if (b.x < 30 || b.x > GC.width - 30) b.vx *= -1;
    if (b.y < 30 || b.y > GC.height - 30) b.vy *= -1;
    const pulse = 0.55 + 0.45 * Math.sin(t * 2 + b.ph);
    const rg = GX.createRadialGradient(b.x, b.y, 0, b.x, b.y, b.r * 3.2);
    rg.addColorStop(0, b.k.c); rg.addColorStop(1, "rgba(0,0,0,0)");
    GX.globalAlpha = 0.85 * pulse; GX.fillStyle = rg;
    GX.beginPath(); GX.arc(b.x, b.y, b.r * 3.2, 0, 6.283); GX.fill();
    GX.globalAlpha = 1; GX.fillStyle = b.k.c;
    GX.beginPath(); GX.arc(b.x, b.y, b.r * 0.55, 0, 6.283); GX.fill();
  });
  GX.globalAlpha = 1; GX.fillStyle = "rgba(223,243,255,0.8)"; GX.font = "15px 'Microsoft YaHei'";
  GX.fillText("已收集：" + [...caught].join(" · "), 20, GC.height - 20);
}

// ===================== 海浪声（WebAudio 合成，不占文件） =====================
let actx = null, soundOn = false, seaGain = null;
function startSea() {
  actx = actx || new (window.AudioContext || window.webkitAudioContext)();
  if (seaGain) return;
  const len = actx.sampleRate * 4;
  const buf = actx.createBuffer(1, len, actx.sampleRate);
  const d = buf.getChannelData(0);
  let last = 0;
  for (let i = 0; i < len; i++) {           // 布朗噪声，像海
    const w = Math.random() * 2 - 1;
    last = (last + 0.02 * w) / 1.02;
    d[i] = last * 3.2;
  }
  const src = actx.createBufferSource(); src.buffer = buf; src.loop = true;
  const lp = actx.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 520;
  seaGain = actx.createGain(); seaGain.gain.value = 0.0;
  src.connect(lp); lp.connect(seaGain); seaGain.connect(actx.destination);
  src.start();
  // 缓慢起伏
  const lfo = actx.createOscillator(); lfo.frequency.value = 0.08;
  const lg = actx.createGain(); lg.gain.value = 0.16;
  lfo.connect(lg); lg.connect(seaGain.gain); lfo.start();
}
document.getElementById("btnSound").onclick = () => {
  soundOn = !soundOn;
  document.getElementById("btnSound").classList.toggle("on", soundOn);
  if (soundOn) { startSea(); actx.resume(); seaGain.gain.value = 0.5; }
  else if (seaGain) seaGain.gain.value = 0.0;
};

// ===================== 主循环 =====================
let t0 = 0, prev = 0;
(function loop(ts){
  requestAnimationFrame(loop);
  ts = ts || 0; const dt = Math.min(0.05, (ts - prev) / 1000 || 0.016); prev = ts;
  t0 = ts / 1000;
  curtains.forEach((m,i)=>{ m.rotation.y = Math.sin(t0*1.2 + i)*0.05; });
  const hour = new Date().getHours();
  const night = (hour >= 22 || hour < 7);
  pets.forEach((sp, k) => {
    const u = sp.userData;
    const waving = u.mode === "wave" && t0 < u.waveUntil;
    const set = (waving && u.waveFrames.length ? u.waveFrames : u.frames);
    const fps = waving ? 18 : (night ? 4 : 12);
    const idx = Math.floor(t0 * fps + k * 3) % set.length;
    if (idx !== u.i || set !== u.lastSet) {
      sp.material.map = set[idx]; sp.material.needsUpdate = true;
      u.i = idx; u.lastSet = set;
    }
    if (!waving && u.mode === "wave") u.mode = "idle";
    // 晚上：发暗、慢下来
    sp.material.color.setHex(night ? 0x7f95ab : u.base);
    sp.position.y = u.y0 + Math.sin(t0 * (night ? 0.6 : 1.6) + k) * (night ? 0.01 : 0.03);
    // 有实时目标（她这会儿在哪儿）就慢慢走过去
    const tgt = HOME[k === 0 ? "sis" : "me"].target;
    if (tgt) {
      sp.position.x += (tgt.x - sp.position.x) * 0.02;
      sp.position.z += (tgt.z - sp.position.z) * 0.02;
      const bub = HOME[k === 0 ? "sis" : "me"].bubble;
      if (bub) bub.position.set(sp.position.x, sp.position.y + 1.15, sp.position.z);
      return;
    }
    // 走路模式里跟着你；否则在原地小步晃
    if (mode === "walk") {
      const dx = walk.pos.x - sp.position.x, dz = walk.pos.z - sp.position.z;
      const d = Math.hypot(dx, dz);
      if (d > 1.9 && d < 7) { sp.position.x += dx / d * 0.02; sp.position.z += dz / d * 0.02; }
    } else {
      sp.position.x = u.x + Math.sin(t0 * 0.35 + k * 2) * 0.22;
      sp.position.z = u.z + Math.cos(t0 * 0.28 + k) * 0.12;
    }
  });
  if (mode === "walk") walkStep(dt);
  if (gameOn) drawGame(dt, t0);
  renderer.render(scene, camera);
})(0);
</script></body></html>
"""

if __name__ == "__main__":
    p = build()
    if p and "--open" in sys.argv:
        exe = next((e for e in EDGE if os.path.exists(e)), None)
        if exe:
            subprocess.Popen([exe, p])
