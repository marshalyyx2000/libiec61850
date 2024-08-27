import iec61850
def list_remote_files(mms_host, directory_path):
    connection = iec61850.IedConnection_create()
    result = iec61850.IedConnection_connect(connection, mms_host, 102)
    if result != 0:
        print(f"连接到 MMS 服务器失败。错误代码: {result}")
        iec61850.IedConnection_destroy(connection)
        return
    directory_entries = iec61850.LinkedList_create()
    directory_entries = iec61850.IedConnection_getFileDirectory(connection, directory_path)    
    if not directory_entries:
        print("获取文件目录失败。")
        iec61850.IedConnection_destroy(connection)
        return

    iec61850.LinkedList_printStringList(directory_entries[0])
    size = iec61850.LinkedList_size(directory_entries[0])
    print(f"Linked List Size: {size}")
    print(f"Files in directory '{directory_path}':")


    direcEntry = iec61850.LinkedList_create()
    direcEntry = iec61850.LinkedList_getNext(directory_entries[0])
    while direcEntry:
        print(iec61850.FileDirectoryEntry_getFileName(iec61850.toFileDirectoryEntry(direcEntry.data)))
        direcEntry = iec61850.LinkedList_getNext(direcEntry)

    iec61850.IedConnection_close(connection)


# 示例使用
list_remote_files("172.9.1.123", "/SecondDevCheck/")



