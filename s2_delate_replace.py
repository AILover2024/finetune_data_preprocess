import os
from pathlib import Path
from config import load_config,conf

#处理文件的每一行并跳过空行
def process_lines(input_file, output_file, replacements):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:

                #Skip all empty lines
                if not line.strip():
                    continue

                modified_line = delete_colon(line)
                modified_line = replace_characters(modified_line, replacements)

                outfile.write(modified_line)

        print("Processing complete. Check the output file:", output_file)
    except FileNotFoundError:
        print("Error: Input file not found. 或者是没有输出文件路径，请新目录。")
    except Exception as e:
        print("An error occurred:", str(e))

#删除每行开头的名字和冒号
def delete_colon(line):
    # Find the index of the first "：" character
    index_of_colon = line.find("：")

    # If ":" is found, write the substring after it to the output file
    if index_of_colon != -1:
        modified_line = line[index_of_colon + 1:]
    else:
        # If ":" is not found, write the entire line to the output file
        modified_line = line
    return modified_line

#替换字符
def replace_characters(line, replacements):
    for replace_char, replacement_char in replacements:
        line = line.replace(replace_char, replacement_char)
    return line

#生成每个文件对应的输出文件
def process_files_in_directory(directory, replacements,output_directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            
            output_file_name = f"dele_prefix_{filename}"

            output_file_path = os.path.join(output_directory, output_file_name)
            print("file_path:", file_path)
            process_lines(file_path, output_file_path, replacements)

# 含有需要处理数据文件的文件夹
if __name__ == "__main__":  
    load_config()
    input_directory = conf().get("output_dir_1")
    output_directory = conf().get("output_dir_2")
    
    Path(output_directory).mkdir(exist_ok=True)

    # 将第一个字符（英文）替换为第二个（中文）
    replacements = [(',', '，'),
                    ('"', '”'),
                    ('!', '！'),
                    ('?', '？')
                    # Add more tuples as needed
                    ]

    print("Current Working Directory: ", os.getcwd())
    process_files_in_directory(input_directory, replacements,output_directory)