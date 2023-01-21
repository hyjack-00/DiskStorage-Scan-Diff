# DiskStorage-Scan-Diff

Running out of disk space but don't know why? Scan the disk & Compare to the last scan.

用光了硬盘空间但是又不知道要清理哪里？扫描硬盘，比较结果以找出最近的存储空间变化



### Intro

python script - Scannig hard disk files storage and Finding out major differences by comparing with last scanning result.

python 脚本 - 扫描硬盘所有文件的存储空间，对比上一次的扫描结果，以找出主要的变化



### Usage

设定好下面的自定义参数，然后直接运行 python 脚本即可

- 第一次运行 / 不存在扫描记录时，只会扫描不会进行对比
- 存在扫描记录时，取最新的记录进行对比

对比的结果保存在文件中，如果数量较少（<=30）则直接输出在命令台

> 无法访问的文件大小为 -1 (Byte)



### Customization

自定义参数

- `TARGET_PATH` 
- `IGNORE_PATHS`
- `DIFF_THRESHOLD` 筛选阈值：只有存储空间变化超过这个阈值的文件才会保留下来
- `IGNORE_SUFFIX`：扫描结果中忽略的文件后缀（只适用于 `SUFFIX_MERGE` 模式）
- `SCAN_RES_PATH` 扫描结果的存储路径，默认 `./scan_result`（只适用于 `NEW_SAVED` 模式）
- `DIFF_RES_PATH` 对比结果的存储路径，默认 `./diff_result`

模式选择

- `NEW_SAVED` 将新的扫描结果以文件保存下来
  - 关闭时，可以保留之前的扫描结果用作继续对比
- `SINGLE_FILE` 启用该模式，将会记录单个文件的大小
- `SUFFIX_MERGE` 启用该模式，将在同一个文件夹下，把 合并处理同一后缀名的文件大小 也纳入记录
  - 处理体积小但零散大量的文件，比如游戏的 highlight 自动录像
- `SORTED` 对比结果按空间大小排序
  - 因为不是按文件，实际观感可能不好






