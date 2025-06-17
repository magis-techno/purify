import os
import json
from pathlib import Path

REPORT_DIR = Path('report')
REPORT_DIR.mkdir(exist_ok=True)

ROOT = Path('.')

result = {}

def collect_file_info(base_dir, rel_base):
    """
    遍历 base_dir 下所有文件，返回：
    - 路径归纳字典 { parent_path: { '文件数': n, '文件列表': [...] } }
    - 文件总数
    - 文件总大小
    """
    path_summary = {}
    total_count = 0
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(base_dir):
        rel_dir = Path(dirpath).relative_to(rel_base)
        # parent_path: '' 表示一级目录本身，其他为更深层相对路径
        parent_path = str(rel_dir) if str(rel_dir) != '.' else ''
        for fname in filenames:
            total_count += 1
            fpath = Path(dirpath) / fname
            try:
                total_size += fpath.stat().st_size
            except Exception:
                pass
            if parent_path not in path_summary:
                path_summary[parent_path] = {'文件数': 0, '文件列表': []}
            path_summary[parent_path]['文件数'] += 1
            path_summary[parent_path]['文件列表'].append(fname)
    return path_summary, total_count, round(total_size / (1024**3), 3)

# 统计根目录
root_files = [f for f in ROOT.iterdir() if f.is_file()]
root_size = sum(f.stat().st_size for f in root_files)
root_path_summary = {}
if root_files:
    root_path_summary[''] = {
        '文件数': len(root_files),
        '文件列表': [f.name for f in root_files]
    }
result['./'] = {
    '总文件数': len(root_files),
    '总大小(GB)': round(root_size / (1024**3), 3),
    '路径归纳': root_path_summary
}

# 统计一级目录
for item in ROOT.iterdir():
    if item.is_dir() and item.name != 'report':
        path_summary, total_count, total_size = collect_file_info(item, item)
        result[f'./{item.name}/'] = {
            '总文件数': total_count,
            '总大小(GB)': total_size,
            '路径归纳': path_summary
        }

# 输出为json
json_path = REPORT_DIR / 'summary.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'统计完成，报告已生成：{json_path}') 