import os
import csv
from pathlib import Path

REPORT_DIR = Path('report')
REPORT_DIR.mkdir(exist_ok=True)

ROOT = Path('.')

summary = []

# 统计根目录下的文件
root_files = [f for f in ROOT.iterdir() if f.is_file()]
root_size = sum(f.stat().st_size for f in root_files)
summary.append({
    '目录': './',
    '文件数量': len(root_files),
    '总大小(GB)': round(root_size / (1024**3), 3),
    '二级目录归纳': ''
})

# 统计一级目录
for item in ROOT.iterdir():
    if item.is_dir() and item.name != 'report':
        # 统计所有文件（包括所有子目录）
        file_count = 0
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(item):
            file_count += len(filenames)
            for fname in filenames:
                fpath = Path(dirpath) / fname
                try:
                    total_size += fpath.stat().st_size
                except Exception:
                    pass
        # 统计二级目录
        subdirs = [d.name for d in item.iterdir() if d.is_dir()]
        summary.append({
            '目录': f'./{item.name}/',
            '文件数量': file_count,
            '总大小(GB)': round(total_size / (1024**3), 3),
            '二级目录归纳': ', '.join(subdirs)
        })

# 输出为markdown表格
md_path = REPORT_DIR / 'summary.md'
with open(md_path, 'w', encoding='utf-8') as f:
    f.write('| 目录 | 文件数量 | 总大小(GB) | 二级目录归纳 |\n')
    f.write('|------|----------|------------|--------------|\n')
    for row in summary:
        f.write(f"| {row['目录']} | {row['文件数量']} | {row['总大小(GB)']} | {row['二级目录归纳']} |\n")

# 输出为csv
csv_path = REPORT_DIR / 'summary.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['目录', '文件数量', '总大小(GB)', '二级目录归纳'])
    writer.writeheader()
    for row in summary:
        writer.writerow(row)

print(f'统计完成，报告已生成：{md_path} 和 {csv_path}') 