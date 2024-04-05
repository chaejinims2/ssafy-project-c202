import time
import struct
from pinpong.board import Board, I2C

#Specify the port initialization under Linux
Board("leonardo","/dev/ttyACM0").begin() 

# MPU605 settings
MPU6050_ADDR = 0x68  # I2C address of mpu6050
MPU6050_POWER_MAN = 0x68  # Power management register



# Set sensitivity 
MPU6050_GYRO_REG = 0x1b
MPU6050_ACCL_REG = 0x1c


# # 16비트 정수 처리
# r1 = b'\x01\x02'
# val = struct.unpack('h', r1)[0]


# Initialize I2C
mpu6050 = I2C()




def read_data_from_channel(channel):

    # wakes up the MPU-6050
    mpu6050.writeto(0x68, [MPU6050_POWER_MAN, 0])

    # Set sensitivity
    mpu6050.writeto(0x68, [MPU6050_GYRO_REG, channel])
    mpu6050.writeto(0x68, [MPU6050_ACCL_REG, channel])
    
    
    time.sleep(0.1)  

    # Read 

    mpu6050.writeto(MPU6050_ADDR, [0x00])
    # Read 14 bytes
    data = mpu6050.readfrom(0x3B, 14)
    
    
    values = []
    for i in range(0, 14, 2):
        value = (data[i] << 8) | data[i+1]  # Combine two bytes into one 16-bit integer
        values.append(value)
    print(values)
    # print(values[3]/340.00+36.53)




# Main loop
while True:

    read_data_from_channel(0)

    time.sleep(0.5)
