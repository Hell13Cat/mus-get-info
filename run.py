from sys import platform
import os
from mutagen.flac import FLAC
import re

def file_name_root_get():
    if platform == "linux" or platform == "linux2":
        path = os.getcwd()
        if not os.path.exists(os.path.join(path, "FLAC Info by Nyako")):
            os.mkdir(os.path.join(path, "FLAC Info by Nyako"))
        return os.path.join(path, "FLAC Info by Nyako")
    elif platform == "win32":
        from win32com.shell import shell, shellcon
        path = shell.SHGetKnownFolderPath(shellcon.FOLDERID_Documents)
        if not os.path.exists(os.path.join(path, "FLAC Info by Nyako")):
            os.mkdir(os.path.join(path, "FLAC Info by Nyako"))
        return os.path.join(path, "FLAC Info by Nyako")
    else:
        print("No use this os!")

def get_ext(file_name):
    UP_name = file_name.upper()
    return UP_name.split(".")[-1]

def get_meta(file_name):
    ext_file = get_ext(file_name)
    audio = FLAC(file_name)
    file_name_small = str(audio.filename).split("\\")[-1]
    metadata = audio.metadata_blocks
    meta_big_np = str(audio.pprint()).split("\n")
    print("--------------")
    print(audio.pprint())
    meta_big = {}
    for ss in meta_big_np:
        if "=" in ss:
            meta_big[(ss.split("=")[0]).upper()] = ss.split("=")[1]
    khz_info = int(re.findall(r'[0-9]{1,7}', str(str(audio.pprint()).split("\n")[0]))[-1]) // 1000
    second_len = float(re.findall(r'[0-9\.]{1,7}', str(str(audio.pprint()).split("\n")[0]))[0])
    file_stats = os.stat(file_name)
    size_file = (file_stats.st_size) // 1024
    bit_file = audio.info.bits_per_sample
    dict_res = {"code":1, "khz":khz_info, "second":second_len, "size":size_file, "bit":bit_file, "ext":ext_file, "name":file_name_small}
    if "ARTIST" in meta_big.keys():
        dict_res["artist"] = meta_big["ARTIST"]
    if "TITLE" in meta_big.keys():
        dict_res["song"] = meta_big["TITLE"]
    return dict_res

def get_list_file(folder):
    dir_root = folder
    filelist = []
    for root, dirs, files in os.walk(dir_root):
        for file in files:
            if get_ext(file) == "FLAC":
                filelist.append(os.path.join(root,file))
    return filelist

def get_time(secs):
    min = int(secs // 60)
    sec = int(secs - min * 60)
    if len(str(sec)) == 2:
        sec_append = ""
    elif len(str(sec)) == 1:
        sec_append = "0"
    else:
        sec_append = "00"
    res = str(min) + ":" + sec_append + str(sec) 
    return res

def get_info_folder(folder_name):
    all_bit = []
    count_size = 0
    count_song = 0
    count_time = 0
    list_file = get_list_file(folder_name)
    list_data = []
    for file_name in list_file:
        list_data.append(get_meta(file_name))
    res_text = ""
    for tt in list_data:
        count_song += 1
        text_add = "[" + tt["ext"] + "] [" + get_time(tt["second"]) + "] " + tt["artist"] + " - " + tt["song"] +\
        " </" + str(tt["khz"]) + " kHz/" + str(tt["bit"]) + " bit/" + str(round(tt["size"] / 1024, 2)) + " mb/>\n"
        res_text += text_add
        count_size += tt["size"]
        count_time += tt["second"]
        all_bit.append(tt["bit"])
    min_bit = 999999999
    max_bit = 0
    for ii in all_bit:
        if ii < min_bit:
            min_bit = ii
        if ii > max_bit:
            max_bit = ii
    if min_bit == max_bit:
        info_bit = str(min_bit)
    else:
        info_bit = str(min_bit) + "-" + str(max_bit)
    text_add = "\n\n\n[" + tt["ext"] + "] [" + get_time(count_time) + "] " + folder_name.split("\\")[-1] +\
    " </" + str(tt["khz"]) + " kHz/" + info_bit + " bit/" + str(round(count_size / 1024, 2)) + " mb/"+\
    str(count_song)+"s"+"/>"
    res_text += text_add
    print(res_text)
    return res_text


def save_info_folder(folder_name):
    res_text = get_info_folder(folder_name)
    save_name = os.path.join(file_name_root_get(), folder_name.split("\\")[-1] + ".txt")
    open(save_name, "w", encoding="utf-8").write(res_text)

folder_name = input("> ")
save_info_folder(folder_name)
fff = input("Press Enter...")