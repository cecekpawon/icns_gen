import os
import glob
from PIL import Image
import io

# icon_typeを返します
def get_icon_type(width: int, is_scale2x: bool):
    icon_type = None
    if width == 16:
        if is_scale2x == False:
            icon_type = b"icp4"
    elif width == 32:
        if is_scale2x == False:
            icon_type = b"icp5"
        else:
            icon_type = b"ic11"
    elif width == 64:
        if is_scale2x == False:
            icon_type = b"icp6"
        else:
            icon_type = b"ic12"
    elif width == 128:
        if is_scale2x == False:
            icon_type = b"ic07"
    elif width == 256:
        if is_scale2x == False:
            icon_type = b"ic08"
        else:
            icon_type = b"ic13"
    elif width == 512:
        if is_scale2x == False:
            icon_type = b"ic09"
        else:
            icon_type = b"ic14"
    elif width == 1024:
        icon_type = b"ic10"

    return icon_type


# 複数のpngファイルから、icnsファイルを作成します
def icns_gen(input_folder: str, output: str = None):
    """
    入力フォルダを確認します
    """
    if input_folder == None:
        print("No input folder specified.")
        return 1

    if not os.path.exists(input_folder):
        print("input folder does not exist.")
        return 1

    if not os.path.isdir(input_folder):
        print("It's not a folder.")
        return 1

    """
        出力を確認します
    """
    icns_file_name = "icon.icns"
    output_folder = output
    output_file = None
    if output_folder == None:
        # 指定がなければ同じフォルダ
        output_folder = input_folder

    if os.path.isdir(output_folder):
        # 指定がフォルダならファイル名を追加
        output_file = os.path.join(output_folder, icns_file_name)
    else:
        output_file = output_folder

    """
        変換します
        https://en.wikipedia.org/wiki/Apple_Icon_Image_format
    """
    # 全データ
    icns_data = b""
    size_all = 0

    files = glob.glob(os.path.join(input_folder, "*.png"))
    for file in files:
        print(file)
        img = Image.open(file)

        # icon_typeを判別
        is_scale2x = "@2x" in file
        icon_type = get_icon_type(img.width, is_scale2x)
        if icon_type == None:
            continue
        else:
            print(icon_type)
        icns_data = icns_data + icon_type

        # 実データを追加
        output = io.BytesIO()
        img.save(output, format="PNG")
        g = output.getvalue()
        size_icon = 4 + 4 + len(g)
        icns_data = icns_data + size_icon.to_bytes(4, "big")
        icns_data = icns_data + g
        size_all = size_all + size_icon

    with open(output_file, "wb") as f:
        f.write(b"icns")
        size_all = 4 + 4 + size_all
        f.write(size_all.to_bytes(4, "big"))
        f.write(icns_data)


if __name__ == "__main__":
    icns_gen("./icons")
