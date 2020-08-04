# coding=utf-8
import os
import zipfile


def un_zip(file_name, dir_prefix=None):
    """unzip zip file"""
    is_zip = zipfile.is_zipfile(file_name)
    release_file_dir = file_name[:-4]
    if is_zip:
        zip_file_contents = zipfile.ZipFile(file_name, 'r')
        for file in zip_file_contents.namelist():
            zip_file_contents.extract(file, release_file_dir)  # 解压缩ZIP文件
            try:
                filename = file.encode('cp437').decode('gbk')  # 先使用cp437编码，然后再使用gbk解码
                os.chdir(release_file_dir)  # 切换到目标目录
                os.rename(file, filename)  # 重命名文件
            except:
                pass
        zip_file_contents.close()
        if dir_prefix is not None:
            os.chdir(dir_prefix)  # 切换到解压目录
    return is_zip, release_file_dir+"/"
