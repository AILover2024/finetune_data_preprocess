
import os
from config import load_config, conf

PREFIX = ["我", "祁煜"]

def get_name(line):
    index_of_colon = line.find("：")
    if index_of_colon != -1:
        name = line[:index_of_colon].strip()
        return name

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_person_lines(file_path, output_file_path):
    # 确保输出文件夹存在
    ensure_directory_exists(os.path.dirname(output_file_path))

    try:
        with open(file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
            cur_person = None
            for line in infile:
                if (line != "\n") or (line is None):
                    cur_person = get_name(line)
                    if cur_person == PREFIX[0]:
                        next_line = next(infile, None)
                        if get_name(next_line) == PREFIX[1]:
                            outfile.write(line)
                            outfile.write(next_line)
                else:
                    continue
            print("End of file reached.")

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {str(e)}")


def test_continuity(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            cur_person = None

            for line in infile:
                cur_person = get_name(line)

                # Check if the current person is "我" and the next person is "陆沉"
                if cur_person == PREFIX[0]:
                    next_line = next(infile, None)
                    if get_name(next_line) == PREFIX[0]:
                        print("存在两个我连续")

                if cur_person == PREFIX[1]:
                    next_line = next(infile, None)
                    if get_name(next_line) == PREFIX[1]:
                        print("存在两个“男主”连续")
            print("End of file reached.")

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {str(e)}")

if __name__ == "__main__":
    load_config();
    directory = conf().get("input_dir")
    out_dir = conf().get("output_dir_1")

    for filename in os.listdir(directory):
        input_file_path = os.path.join(directory, filename)
        output_file_path = os.path.join(out_dir, f"output_{filename}")

        extract_person_lines(input_file_path, output_file_path)
        print(f"Lines with {PREFIX[0]} and {PREFIX[1]} written to {output_file_path}.")
