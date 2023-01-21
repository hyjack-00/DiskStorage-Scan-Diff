
import os
import time

# 扫描参数
TARGET_PATH = "C:\\"
IGNORE_PATHS = ["C:\\Windows", "C:\\$Recycle.Bin\\"]
DIFF_THRESHOLD = 200 * 1024 * 1024  # bytes
IGNORE_SUFFIX = ["dll", "exe"]

IS_NEW_SAVED = 0  # 是否保存 new_scan（试筛选模式）
IS_SUFFIX_MERGE = 1  # 合并处理同一后缀名的文件大小
IS_SINGLE_FILE = 1  # 单个文件的大小
IS_SORTED = 0  # diff result 对大小进行排序

SCAN_RES_PATH = ".\\scan_result\\"
DIFF_RES_PATH = ".\\diff_result\\"


# 尝试读取上一次扫描记录
last_scan = {}
last_scan_file = None
try:
    scan_files = os.listdir(SCAN_RES_PATH)
    scan_files.sort()
    last_scan_file = scan_files[-1]
    print("Last scan: " + last_scan_file)

    with open(SCAN_RES_PATH + last_scan_file, "r", encoding='utf-8') as f:
        for line in f:
            path, size = line.strip().split(': ')
            last_scan[path] = int(size.split()[0])
except:  # 还未产生扫描记录
    print("First scan")

# 开始本次扫描
print("Scanning...")
new_scan = {}
current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())  # 年月日时分秒
new_scan_path = SCAN_RES_PATH + f"scan_result_{current_time}.txt"
with open(new_scan_path, "w", encoding='utf-8') as f:
    for folder, sub_folders, filenames in os.walk(TARGET_PATH):
        for ignore_path in IGNORE_PATHS:
            if folder.startswith(ignore_path):
                sub_folders[:] = []
                continue
            if IS_SUFFIX_MERGE:  # 以文件后缀名区分模式
                suffixes = {}
                for filename in filenames:
                    path = os.path.join(folder, filename)
                    try:
                        size = os.path.getsize(path)
                        suffix = filename.split('.')[-1]
                        path_suffix = os.path.join(folder, suffix)
                        if path_suffix in suffixes.keys():
                            suffixes[path_suffix] += size
                        else:
                            suffixes[path_suffix] = size
                    except:
                        f.write(f"{path}: -1 (Could not be scanned)\n")

                for path, size in suffixes.items():
                    if os.path.basename(path) not in IGNORE_SUFFIX:
                        new_scan[path] = size
                        f.write(f"{path}: {size} bytes\n")

            if IS_SINGLE_FILE:  # 普通模式
                for filename in filenames:
                    path = os.path.join(folder, filename)
                    try:
                        size = os.path.getsize(path)
                        new_scan[path] = size
                        f.write(f"{path}: {size} bytes\n")
                    except:
                        f.write(f"{path}: -1 (Could not be scanned)\n")

if not IS_NEW_SAVED:
    os.remove(new_scan_path)

# 对比扫描结果
if last_scan_file:
    print("Differing...")
    diff_scan = {}
    with open(DIFF_RES_PATH + f"diff_result_{current_time}.txt", "w", encoding='utf-8') as f:
        for new_path, new_size in new_scan.items():
            if new_path in last_scan:
                diff = new_size - last_scan[new_path]
                if abs(diff) >= DIFF_THRESHOLD:
                    diff_scan[new_path] = diff
                    if not IS_SORTED:
                        f.write(f"{int(diff/1024/1024)} MB change : {new_path}\n")
            elif new_size >= DIFF_THRESHOLD:  # 新建文件
                diff_scan[new_path] = new_size
                if not IS_SORTED:
                    f.write(f"{int(new_size/1024/1024)} MB new : {new_path}\n")

        for old_path, old_size in last_scan.items():
            if old_path in new_scan:
                pass
            elif old_size >= DIFF_THRESHOLD:  # 删除文件
                diff_scan[old_path] = -old_size
                if not IS_SORTED:
                    f.write(f"{-int(old_size/1024/1024)} MB delete : {old_path}\n")

        if IS_SORTED:  # 结果排序模式：统一写入
            diff_scan = sorted(diff_scan.items(), key=lambda x: x[1])
            for path, size in diff_scan:
                f.write(f"{int(size/1024/1024)} MB : {path}\n")

    count = len(diff_scan)
    units = ["", "files", "suffixes", "files or suffixes"]
    unit = units[IS_SINGLE_FILE + 2 * IS_SUFFIX_MERGE]
    if count:
        print(f"{count} {unit} have changed size more than {DIFF_THRESHOLD} Bytes.")
    else:
        print(f"No {unit} have changed size more than {DIFF_THRESHOLD} Bytes.")

    if count <= 30:
        for path, size in diff_scan.items():
            print(f"{int(size/1024/1024)} MB : {path}")
    else:
        print(f"more than 30 {unit} changed.")

print("All done")
# os.system("pause")
