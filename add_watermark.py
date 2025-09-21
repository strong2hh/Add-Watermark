import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from datetime import datetime

def get_exif_datetime(img_path):
    try:
        image = Image.open(img_path)
        exif_data = image._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':
                    # 格式如 '2023:09:21 18:17:46'
                    date_str = value.split(' ')[0].replace(':', '-')
                    return date_str
        return None
    except Exception:
        return None

def add_watermark(img_path, text, font_size, color, position, out_path, xy=None):
    image = Image.open(img_path).convert('RGBA')
    width, height = image.size
    txt_layer = Image.new('RGBA', image.size, (255,255,255,0))
    try:
        font = ImageFont.truetype('arial.ttf', font_size)
    except:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(txt_layer)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # 位置计算
    if xy:
        x, y = xy
    elif position == 'left-top':
        x, y = 10, 10
    elif position == 'right-top':
        x, y = width - text_w - 10, 10
    elif position == 'left-center':
        x, y = 10, (height - text_h)//2
    elif position == 'center':
        x, y = (width - text_w)//2, (height - text_h)//2
    elif position == 'right-center':
        x, y = width - text_w - 10, (height - text_h)//2
    elif position == 'left-bottom':
        x, y = 10, height - text_h - 10
    elif position == 'right-bottom':
        x, y = width - text_w - 10, height - text_h - 10
    else:
        x, y = 10, 10
    draw.text((x, y), text, font=font, fill=color+(128,))  # 半透明
    watermarked = Image.alpha_composite(image, txt_layer).convert('RGB')
    watermarked.save(out_path)

def main():
    parser = argparse.ArgumentParser(description='批量图片添加拍摄时间水印')
    parser.add_argument('dir', help='图片文件夹路径')
    parser.add_argument('--font_size', type=int, default=32, help='字体大小')
    parser.add_argument('--color', type=str, default='255,0,0', help='字体颜色，格式如255,0,0')
    parser.add_argument('--position', choices=['left-top','right-top','left-center','center','right-center','left-bottom','right-bottom'], default='right-bottom', help='水印位置')
    parser.add_argument('--xy', type=str, help='自定义水印坐标，如100,200')
    args = parser.parse_args()

    img_dir = args.dir
    font_size = args.font_size
    color = tuple(map(int, args.color.split(',')))
    position = args.position
    xy = tuple(map(int, args.xy.split(','))) if args.xy else None

    out_dir = os.path.join(img_dir, os.path.basename(img_dir) + '_watermark')
    os.makedirs(out_dir, exist_ok=True)

    for fname in os.listdir(img_dir):
        fpath = os.path.join(img_dir, fname)
        if os.path.isfile(fpath) and fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            date_str = get_exif_datetime(fpath)
            if date_str:
                out_path = os.path.join(out_dir, fname)
                add_watermark(fpath, date_str, font_size, color, position, out_path, xy)
                print(f'已处理: {fname} -> {out_path}')
            else:
                print(f'跳过无拍摄时间: {fname}')

if __name__ == '__main__':
    main()
