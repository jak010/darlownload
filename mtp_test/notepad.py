import ctypes

# from pymtp import MTP, LIBMTP_File
import logging
import os
import pymtp
from pymtp import LIBMTP_File, _libmtp

device = pymtp.MTP()
device.connect()

target = "test.text"
source = ""

print(device.device.default_music_folder)

# metadata = LIBMTP_File(filename=target.encode("utf-8"),
#                        filetype=device.find_filetype(source),
#                        filesize=os.stat(source).st_size,
#                        parent_id=0,
#                        storage_id=0
#                        )
#
# ret = _libmtp.LIBMTP_Send_File_From_File_Descriptor(device.device, source, metadata)
# print(ret)

device.disconnect()
