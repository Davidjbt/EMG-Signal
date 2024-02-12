import serial

ser = serial.Serial('COM5', 115200)  # Adjust the port and baud rate based on your setup
threshold = 70

data = 0

while True:
    try:
        data = int(ser.readline().decode().strip())

        if abs(data) > threshold:
            print('Active')
        else:
            print('No')

    except ValueError:
        print(f"Skipping invalid data: {data}")
