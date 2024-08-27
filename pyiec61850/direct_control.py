import iec61850
import time
import sys


def main():
    hostname ="172.20.88.99"
    tcp_port = 102

    # Check for command-line arguments
    if len(sys.argv) > 1:
        hostname = sys.argv[1]

    if len(sys.argv) > 2:
        tcp_port = int(sys.argv[2])

    # Create an IED connection
    con = iec61850.IedConnection_create()

    # Connect to the server
    error = iec61850.IedConnection_connect(con, hostname, tcp_port)

    if error == iec61850.IED_ERROR_OK:
        # Direct control example
        control = iec61850.ControlObjectClient_create("GD5000MLD0/LLN0.SetInfProc", con)

        if control:
            ctl_val = iec61850.MmsValue_newBoolean(True)
            iec61850.ControlObjectClient_setOrigin(control, None, 3)

            if iec61850.ControlObjectClient_operate(control, ctl_val, 0):
                print("GD5000MLD0/LLN0.SetSMCDProc operated successfully")
            else:
                print("Failed to operate GD5000MLD0/LLN0.SetSMCDProc")

            iec61850.MmsValue_delete(ctl_val)
            iec61850.ControlObjectClient_destroy(control)

            # Check status value
            st_val = iec61850.IedConnection_readObject(con, "GD5000MLD0/LLN0.SetInfProc.stVal", iec61850.IEC61850_FC_ST)

            if st_val:
                state = iec61850.MmsValue_getBoolean(st_val[0])
            else:
                print("Reading status for GD5000MLD0/LLN0.SetSMCDProc failed!")
        else:
            print("Control object GD5000MLD0/LLN0.SetSMCDProc not found in server")
        # Close the connection
        iec61850.IedConnection_close(con)
    else:
        print("Connection failed!")

    # Destroy the connection
    iec61850.IedConnection_destroy(con)

if __name__ == "__main__":
    main()

