#-*- coding:utf-8 -*-
import os
import json
from config import conf,load_config

#从文档中读取成对的对话
def get_input_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as input_file:
            while True:
                she_words = input_file.readline().strip()
                he_words = input_file.readline().strip()

                if not she_words or not he_words:
                    break  # Exit the loop if reached end of file

                yield she_words, he_words
    except FileNotFoundError:
        print(f"Error: The specified input file '{file_path}' is not found.")
        yield None, None  # Signal that there was an error

#格式化输出到同一文件
def write_message_to_file(system_content, she_words, he_words, output_file_path):
    if she_words is None or he_words is None:
        return  # Do nothing if there was an error getting input

    #message = "She is {}. And he is {}.".format(she_words, he_words)
    message_data = {
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": she_words},
            {"role": "assistant", "content": he_words}
        ]
    }
    json_string = json.dumps(message_data, ensure_ascii=False)

    try:
        with open(output_file_path, 'a', encoding='utf-8') as output_file:  # Add encoding='utf-8'
            output_file.write(json_string + '\n')  # Add a newline between each set of messages
        print("Message written to", output_file_path)
    except Exception as e:
        print("Error:", e)

#循环文件夹并执行
def process_the_directory(reform_input, output_file, system_content):
    for input_file in os.listdir(reform_input):
        # Get input from each input file
        print("Message read from", input_file)

        input_file_path = os.path.join(reform_input, input_file)

        for she_words, he_words in get_input_from_file(input_file_path):
            # Write the message to the corresponding output file for each set of input
            write_message_to_file(system_content, she_words, he_words, output_file)

if __name__ == "__main__":
    load_config()
    # 含有初步处理格式的数据文件的文件夹
    reform_input = conf().get("output_dir_2")
    # 统一的输出文件
    output_file = conf().get("output_file")
    # 需要的system content
    system_content = conf().get("system_prompt")

    process_the_directory(reform_input, output_file, system_content)


