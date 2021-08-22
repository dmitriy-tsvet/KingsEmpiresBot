
def read_txt_file(path: str):
    with open("data/{}.txt".format(path), "r", encoding="utf-8") as file:
        text = file.read()
    return text
