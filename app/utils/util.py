import asyncio
import os

import pyzipper


async def auto_delete(path, delay):
    await asyncio.sleep(delay)
    if os.path.exists(path):
        os.remove(path)


def zip_single_video(file_path, output_zip, password):
    """
    将单个视频文件打包成加密压缩包

    :param file_path: 视频文件路径
    :param output_zip: 输出 zip 文件路径
    :param password: 压缩包密码
    """
    if not os.path.isfile(file_path):
        print(f"文件不存在: {file_path}")
        return

    with pyzipper.AESZipFile(output_zip,
                             'w',
                             compression=pyzipper.ZIP_DEFLATED,
                             encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password.encode('utf-8'))
        zipf.write(file_path, arcname=os.path.basename(file_path))

    print(f"加密压缩完成: {output_zip}")
