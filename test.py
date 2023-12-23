import serial.tools.list_ports

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    serial_ports = [port.device for port in ports]
    return serial_ports

if __name__ == "__main__":
    serial_ports = get_serial_ports()

    if serial_ports:
        print("Serial Ports:")
        for port in serial_ports:
            print(f"Port: {port}")
    else:
        print("No serial ports found.")
