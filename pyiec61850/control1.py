import iec61850
import time
import sys

def control_softborad(con,ref,value):
     control = iec61850.ControlObjectClient_create(ref, con)
     if control:
          #iec61850.ControlObjectClient_setCommandTerminationHandler(control, command1_termination_handler, None)
          ctl_val = iec61850.MmsValue_newBoolean(value)
          #ret=0
          if value==True:
            message="投入压板"
            #ret=1
          else:
            message="退出压板"
          if iec61850.ControlObjectClient_selectWithValue(control, ctl_val):
              if iec61850.ControlObjectClient_operate(control, ctl_val, 0):
                   print(f"{ref} {message}operated successfully")
              else:
                   print(f"{message} Failed to operate {ref}")
          else:
               print(f"{message} Failed to select {ref}")

          iec61850.MmsValue_delete(ctl_val)
          time.sleep(1)
          iec61850.ControlObjectClient_destroy(control)

def read_softborad_value(con,ref):
     st_val = iec61850.IedConnection_readObject(con, ref, iec61850.IEC61850_FC_ST)
     if st_val:
          state = iec61850.MmsValue_getBoolean(st_val[0])
          print(f"Reading status for {ref}",state)
          return state
     else:
          print(f"Reading status for {ref} failed!")
          return -1


def main():
    hostname ="172.9.1.123"
    tcp_port = 102

    # Check for command-line arguments
    if len(sys.argv) >1:
        hostname = sys.argv[1]

    if len(sys.argv) > 2:
        tcp_port = int(sys.argv[2])

    # Create an IED connection
    con = iec61850.IedConnection_create()

    # Connect to the server
    error = iec61850.IedConnection_connect(con, hostname, tcp_port)

    if error == iec61850.IED_ERROR_OK:
         ref="PT01APROT/LLN0.FuncEna1"
         full_ref=ref+".stVal"
         value=read_softborad_value(con, full_ref)
         if value==True:
            control_softborad(con, ref, False)
         elif value==False:
            control_softborad(con, ref, True)
         
         iec61850.IedConnection_close(con)
    else:
         print("Connection failed!")

    # Destroy the connection
    iec61850.IedConnection_destroy(con)

if __name__ == "__main__":
     main()
