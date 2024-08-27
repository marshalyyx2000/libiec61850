import iec61850
import os

# 连接到IED设备
con = iec61850.IedConnection_create()
error = iec61850.IedConnection_connect(con, "172.20.88.99", 102)  # 将 "hostname" 替换为实际设备的地址

if error == iec61850.IED_ERROR_OK:
    # 打开本地文件进行读取
    iec61850.IedConnection_setFilestoreBasepath(con,"./")
    local_file_path = "110kV高唐人和变电站_2.2-1.3_2024_0319_1245_146.SCD.gz"
    # 将文件上传到远程IED设备
    remote_file_path = "/SCD/110kV高唐人和变电站_2.2-1.3_2024_0319_1245_146.SCD.gz"
    error = iec61850.IedConnection_setFile(con, local_file_path,remote_file_path)

    if error == iec61850.IED_ERROR_OK:
        print(f"File {local_file_path} successfully uploaded to {remote_file_path}.")
    else:
        print(f"Failed to upload file to IED: {error}")

    # 关闭连接
    iec61850.IedConnection_close(con)
else:
    print(f"Failed to connect to IED: {error}")

# 销毁连接对象
iec61850.IedConnection_destroy(con)
