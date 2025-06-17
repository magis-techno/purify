import os
import json
from pathlib import Path

REPORT_DIR = Path('report')
REPORT_DIR.mkdir(exist_ok=True)

ROOT = Path('.')

result = {}

def skip_second_level(rel_path):
    """
    输入: Path('二级/三级/四级/文件')
    输出: Path('三级/四级')
    如果只有二级目录，则返回''
    """
    parts = rel_path.parts
    if len(parts) < 2:
        return ''
    # 跳过第二级目录
    return str(Path(*parts[2:-1])) if len(parts) > 2 else ''

# 统计根目录
root_files = [f for f in ROOT.iterdir() if f.is_file()]
root_size = sum(f.stat().st_size for f in root_files)
root_paths = [''] if root_files else []
result['./'] = {
    '总文件数': len(root_files),
    '总大小(GB)': round(root_size / (1024**3), 3),
    '归纳相对路径': root_paths
}

# 统计一级目录
for item in ROOT.iterdir():
    if item.is_dir() and item.name != 'report':
        all_paths = set()
        file_count = 0
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(item):
            for fname in filenames:
                file_count += 1
                fpath = Path(dirpath) / fname
                try:
                    total_size += fpath.stat().st_size
                except Exception:
                    pass
                rel_path = fpath.relative_to(item)
                # 剔除2级目录
                path_wo_2nd = skip_second_level(rel_path)
                all_paths.add(path_wo_2nd)
        result[f'./{item.name}/'] = {
            '总文件数': file_count,
            '总大小(GB)': round(total_size / (1024**3), 3),
            '归纳相对路径': sorted([p for p in all_paths if p != ''] or [''])
        }

# 输出为json
json_path = REPORT_DIR / 'summary.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f'统计完成，报告已生成：{json_path}') 