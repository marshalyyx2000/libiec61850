import iec61850
import time
import sys

class command1_termination_handler(iec61850.CommandTermHandler):
    def __init__(self):
        iec61850.CommandTermHandler.__init__(self)

    #def trigger(self):
        
    def triggerCommandTermHandler(parameter,connection ):
        last_appl_error=iec61850.ControlObjectClient_getLastApplError()
        if last_appl_error.error != 0:
            print("Received CommandTermination-.")
            print(f" LastApplError: {last_appl_error.error}")
            print(f"      addCause: {last_appl_error.addCause}")
        else:
            print("Received CommandTermination+.")

def main():
    hostname ="172.9.1.123"
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
        control = iec61850.ControlObjectClient_create("PT01APROT/LLN0.FuncEna1", con)

        if control:
            ctl_val = iec61850.MmsValue_newBoolean(True)
            iec61850.ControlObjectClient_setOrigin(control, None, 3)

            if iec61850.ControlObjectClient_operate(control, ctl_val, 0):
                print("PT01APROT/LLN0$ST$FuncEna1 operated successfully")
            else:
                print("Failed to operate PT01APROT/LLN0.FuncEna1")

            iec61850.MmsValue_delete(ctl_val)
            iec61850.ControlObjectClient_destroy(control)

            # Check status value
            st_val = iec61850.IedConnection_readObject(con, "PT01APROT/LLN0.FuncEna1.stVal", iec61850.IEC61850_FC_ST)

            if st_val:
                state = iec61850.MmsValue_getBoolean(st_val[0])
            else:
                print("Reading status for PT01APROT/LLN0.FuncEna1 failed!")
        else:
            print("Control object PT01APROT/LLN0.FuncEna1 not found in server")

        # Select before operate example
        control = iec61850.ControlObjectClient_create("PT01APROT/LLN0.FuncEna1", con)

        if control:
            if iec61850.ControlObjectClient_select(control):
                ctl_val = iec61850.MmsValue_newBoolean(True)

                if iec61850.ControlObjectClient_operate(control, ctl_val, 0):
                    print("PT01APROT/LLN0.FuncEna1 operated successfully")
                else:
                    print("Failed to operate PT01APROT/LLN0.FuncEna1")

                iec61850.MmsValue_delete(ctl_val)
            else:
                print("Failed to select PT01APROT/LLN0.FuncEna1")

            iec61850.ControlObjectClient_destroy(control)
        else:
            print("Control object PT01APROT/LLN0.FuncEna1 not found in server")

        # Direct control with enhanced security example
        control = iec61850.ControlObjectClient_create("PT01APROT/LLN0.FuncEna1", con)

        if control:
            #hander=command1_termination_handler.triggerCommandTermHandler
            #iec61850.ControlObjectClient_setCommandTerminationHandler(control, iec61850.CommandTermHandler., con)
            ctl_val = iec61850.MmsValue_newBoolean(True)

            if iec61850.ControlObjectClient_operate(control, ctl_val, 0):
                print("PT01APROT/LLN0.FuncEna1 operated successfully")
            else:
                print("Failed to operate PT01APROT/LLN0.FuncEna1")

            iec61850.MmsValue_delete(ctl_val)
            time.sleep(1)
            iec61850.ControlObjectClient_destroy(control)

            st_val = iec61850.IedConnection_readObject(con, "PT01APROT/LLN0.FuncEna1.stVal", iec61850.IEC61850_FC_ST)

            if st_val:
                state = iec61850.MmsValue_getBoolean(st_val[0])
                print(f"New status of PT01APROT/LLN0.FuncEna1.stVal: {state}")
                iec61850.MmsValue_delete(st_val[0])
            else:
                print("Reading status for PT01APROT/LLN0.FuncEna1 failed!")
        else:
            print("Control object PT01APROT/LLN0.FuncEna1 not found in server")

        # Select before operate with enhanced security example
        control = iec61850.ControlObjectClient_create("PT01APROT/LLN0.FuncEna1", con)

        if control:
            #iec61850.ControlObjectClient_setCommandTerminationHandler(control, command1_termination_handler, None)
            ctl_val = iec61850.MmsValue_newBoolean(True)

            if iec61850.ControlObjectClient_selectWithValue(control, ctl_val):
                if iec61850.ControlObjectClient_operate(control, ctl_val, 0):
                    print("PT01APROT/LLN0.FuncEna1 operated successfully")
                else:
                    print("Failed to operate PT01APROT/LLN0.FuncEna14")
            else:
                print("Failed to select PT01APROT/LLN0.FuncEna1")

            iec61850.MmsValue_delete(ctl_val)
            time.sleep(1)
            iec61850.ControlObjectClient_destroy(control)
        else:
            print("Control object PT01APROT/LLN0.FuncEna1 not found in server")

        # Direct control with enhanced security (expect CommandTermination-) example
        control = iec61850.ControlObjectClient_create("PT01APROT/LLN0.FuncEna1", con)

        if control:
            #iec61850.ControlObjectClient_setCommandTerminationHandler(control, command1_termination_handler, None)
            ctl_val = iec61850.MmsValue_newBoolean(True)

            if iec61850.ControlObjectClient_operate(control, ctl_val, 0):
                print("PT01APROT/LLN0.FuncEna1 operated successfully")
            else:
                print("Failed to operate PT01APROT/LLN0.FuncEna1")

            iec61850.MmsValue_delete(ctl_val)
            time.sleep(1)
            iec61850.ControlObjectClient_destroy(control)
        else:
            print("Control object PT01APROT/LLN0.FuncEna1 not found in server")

        # Close the connection
        iec61850.IedConnection_close(con)
    else:
        print("Connection failed!")

    # Destroy the connection
    iec61850.IedConnection_destroy(con)

if __name__ == "__main__":
    main()
