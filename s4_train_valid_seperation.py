import json
import random
from config import conf, load_config
'''

读取指定all.jsonl文件的所有行，放入一个新的文件“valid.jsonl”中，
并将剩余的80行也放入一个新的文件“train.jsonl”中

↓↓↓在这里指定文件名称↓↓↓
'''
load_config()


input_file = conf().get("output_file") # txt,json都可以
valid_file = conf().get("valid_file")
train_file = conf().get("train_file")

# 读取原始JSONL文件中的所有行
with open(input_file, 'r', encoding='utf-8') as infile:
    all_lines = infile.readlines()

# 计算要选择的行数（20%）
num_total_lines = len(all_lines)
num_valid_lines = int(0.2 * num_total_lines)

# 随机选择20%的行作为验证集
valid_indices = random.sample(range(num_total_lines), num_valid_lines)
valid_lines = [all_lines[i] for i in valid_indices]

# 剩余的80%行作为训练集
train_lines = [line for i, line in enumerate(all_lines) if i not in valid_indices]

# 将选定的行写入验证文件
with open(valid_file, 'w', encoding='utf-8') as valid_outfile:
    valid_outfile.writelines(valid_lines)

# 将剩余的行写入训练文件
with open(train_file, 'w', encoding='utf-8') as train_outfile:
    train_outfile.writelines(train_lines)

print("已生成验证文件 '{}'，包含 {} 行。".format(valid_file, len(valid_lines)))
print("已生成训练文件 '{}'，包含 {} 行。".format(train_file, len(train_lines)))
