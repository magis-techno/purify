import os
import json
from pathlib import Path

REPORT_DIR = Path('report')
REPORT_DIR.mkdir(exist_ok=True)

ROOT = Path('.')

# 一级目录统计
summary = []
# 文件路径清单
all_file_paths = []

# 统计根目录下的文件
root_files = [f for f in ROOT.iterdir() if f.is_file()]
root_size = sum(f.stat().st_size for f in root_files)
summary.append({
    '目录': './',
    '文件数量': len(root_files),
    '总大小(GB)': round(root_size / (1024**3), 3)
})
for f in root_files:
    all_file_paths.append(f.name)

# 统计一级目录
for item in ROOT.iterdir():
    if item.is_dir() and item.name != 'report':
        file_count = 0
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(item):
            for fname in filenames:
                fpath = Path(dirpath) / fname
                rel_path = fpath.relative_to(ROOT)
                all_file_paths.append(str(rel_path))
                file_count += 1
                try:
                    total_size += fpath.stat().st_size
                except Exception:
                    pass
        summary.append({
            '目录': f'./{item.name}/',
            '文件数量': file_count,
            '总大小(GB)': round(total_size / (1024**3), 3)
        })

# 输出为json
json_path = REPORT_DIR / 'summary.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump({
        '一级目录统计': summary,
        '文件路径清单': all_file_paths
    }, f, ensure_ascii=False, indent=2)

print(f'统计完成，报告已生成：{json_path}') 