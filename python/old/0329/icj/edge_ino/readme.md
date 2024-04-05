https://learn.sparkfun.com/tutorials/9dof-razor-imu-m0-hookup-guide#using-the-mpu-9250-dmp-arduino-library





sing library Wire at version 1.0 in folder: /home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/libraries/Wire 
Using library DHT sensor library at version 1.4.6 in folder: /home/cherry/Arduino/libraries/DHT_sensor_library 
Using library Adafruit Unified Sensor at version 1.1.14 in folder: /home/cherry/Arduino/libraries/Adafruit_Unified_Sensor 
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-size -A /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sensors.ino.elf
Sketch uses 10000 bytes (34%) of program storage space. Maximum is 28672 bytes.
Global variables use 458 bytes (17%) of dynamic memory, leaving 2102 bytes for local variables. Maximum is 2560 bytes.
Connecting to programmer: .avrdude: butterfly_recv(): programmer is not responding

avrdude: butterfly_recv(): programmer is not responding



FQBN: arduino:avr:leonardo
Using board 'leonardo' from platform in folder: /home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6
Using core 'arduino' from platform in folder: /home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6

Detecting libraries used...
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-g++ -c -g -Os -w -std=gnu++11 -fpermissive -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -Wno-error=narrowing -flto -w -x c++ -E -CC -mmcu=atmega32u4 -DF_CPU=16000000L -DARDUINO=10607 -DARDUINO_AVR_LEONARDO -DARDUINO_ARCH_AVR -DUSB_VID=0x2341 -DUSB_PID=0x8036 -DUSB_MANUFACTURER="Unknown" -DUSB_PRODUCT="Arduino Leonardo" -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/cores/arduino -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/variants/leonardo /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sketch/sensors.ino.cpp -o /dev/null
Alternatives for Wire.h: [Wire@1.0]
ResolveLibrary(Wire.h)
  -> candidates: [Wire@1.0]
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-g++ -c -g -Os -w -std=gnu++11 -fpermissive -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -Wno-error=narrowing -flto -w -x c++ -E -CC -mmcu=atmega32u4 -DF_CPU=16000000L -DARDUINO=10607 -DARDUINO_AVR_LEONARDO -DARDUINO_ARCH_AVR -DUSB_VID=0x2341 -DUSB_PID=0x8036 -DUSB_MANUFACTURER="Unknown" -DUSB_PRODUCT="Arduino Leonardo" -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/cores/arduino -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/variants/leonardo -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/libraries/Wire/src /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sketch/sensors.ino.cpp -o /dev/null
Alternatives for DHT.h: [DHT sensor library@1.4.6]
ResolveLibrary(DHT.h)
  -> candidates: [DHT sensor library@1.4.6]
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-g++ -c -g -Os -w -std=gnu++11 -fpermissive -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -Wno-error=narrowing -flto -w -x c++ -E -CC -mmcu=atmega32u4 -DF_CPU=16000000L -DARDUINO=10607 -DARDUINO_AVR_LEONARDO -DARDUINO_ARCH_AVR -DUSB_VID=0x2341 -DUSB_PID=0x8036 -DUSB_MANUFACTURER="Unknown" -DUSB_PRODUCT="Arduino Leonardo" -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/cores/arduino -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/variants/leonardo -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/libraries/Wire/src -I/home/cherry/Arduino/libraries/DHT_sensor_library /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sketch/sensors.ino.cpp -o /dev/null
Using cached library dependencies for file: /home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/libraries/Wire/src/Wire.cpp
Using cached library dependencies for file: /home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/libraries/Wire/src/utility/twi.c
Using cached library dependencies for file: /home/cherry/Arduino/libraries/DHT_sensor_library/DHT.cpp
Using cached library dependencies for file: /home/cherry/Arduino/libraries/DHT_sensor_library/DHT_U.cpp
Alternatives for Adafruit_Sensor.h: [Adafruit Unified Sensor@1.1.14]
ResolveLibrary(Adafruit_Sensor.h)
  -> candidates: [Adafruit Unified Sensor@1.1.14]
Using cached library dependencies for file: /home/cherry/Arduino/libraries/Adafruit_Unified_Sensor/Adafruit_Sensor.cpp
Generating function prototypes...
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-g++ -c -g -Os -w -std=gnu++11 -fpermissive -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -Wno-error=narrowing -flto -w -x c++ -E -CC -mmcu=atmega32u4 -DF_CPU=16000000L -DARDUINO=10607 -DARDUINO_AVR_LEONARDO -DARDUINO_ARCH_AVR -DUSB_VID=0x2341 -DUSB_PID=0x8036 -DUSB_MANUFACTURER="Unknown" -DUSB_PRODUCT="Arduino Leonardo" -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/cores/arduino -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/variants/leonardo -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/libraries/Wire/src -I/home/cherry/Arduino/libraries/DHT_sensor_library -I/home/cherry/Arduino/libraries/Adafruit_Unified_Sensor /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sketch/sensors.ino.cpp -o /tmp/4040754765/sketch_merged.cpp
/home/cherry/.arduino15/packages/builtin/tools/ctags/5.8-arduino11/ctags -u --language-force=c++ -f - --c++-kinds=svpf --fields=KSTtzns --line-directives /tmp/4040754765/sketch_merged.cpp
Compiling sketch...
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-g++ -c -g -Os -w -std=gnu++11 -fpermissive -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -Wno-error=narrowing -MMD -flto -mmcu=atmega32u4 -DF_CPU=16000000L -DARDUINO=10607 -DARDUINO_AVR_LEONARDO -DARDUINO_ARCH_AVR -DUSB_VID=0x2341 -DUSB_PID=0x8036 "-DUSB_MANUFACTURER=\"Unknown\"" "-DUSB_PRODUCT=\"Arduino Leonardo\"" -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/cores/arduino -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/variants/leonardo -I/home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/libraries/Wire/src -I/home/cherry/Arduino/libraries/DHT_sensor_library -I/home/cherry/Arduino/libraries/Adafruit_Unified_Sensor /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sketch/sensors.ino.cpp -o /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sketch/sensors.ino.cpp.o
Compiling libraries...
Compiling library "Wire"
Using previously compiled file: /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/Wire/Wire.cpp.o
Using previously compiled file: /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/Wire/utility/twi.c.o
Compiling library "DHT sensor library"
Using previously compiled file: /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/DHT_sensor_library/DHT.cpp.o
Using previously compiled file: /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/DHT_sensor_library/DHT_U.cpp.o
Compiling library "Adafruit Unified Sensor"
Using previously compiled file: /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/Adafruit_Unified_Sensor/Adafruit_Sensor.cpp.o
Compiling core...
Using precompiled core: /tmp/arduino/cores/arduino_avr_leonardo_9e9cdc99fa190de80b3f9f928c46747e/core.a
Linking everything together...
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-gcc -w -Os -g -flto -fuse-linker-plugin -Wl,--gc-sections -mmcu=atmega32u4 -o /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sensors.ino.elf /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sketch/sensors.ino.cpp.o /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/Wire/Wire.cpp.o /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/Wire/utility/twi.c.o /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/DHT_sensor_library/DHT.cpp.o /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/DHT_sensor_library/DHT_U.cpp.o /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/libraries/Adafruit_Unified_Sensor/Adafruit_Sensor.cpp.o /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/../../cores/arduino_avr_leonardo_9e9cdc99fa190de80b3f9f928c46747e/core.a -L/tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6 -lm
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-objcopy -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sensors.ino.elf /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sensors.ino.eep
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-objcopy -O ihex -R .eeprom /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sensors.ino.elf /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sensors.ino.hex

Using library Wire at version 1.0 in folder: /home/cherry/.arduino15/packages/arduino/hardware/avr/1.8.6/libraries/Wire 
Using library DHT sensor library at version 1.4.6 in folder: /home/cherry/Arduino/libraries/DHT_sensor_library 
Using library Adafruit Unified Sensor at version 1.1.14 in folder: /home/cherry/Arduino/libraries/Adafruit_Unified_Sensor 
/home/cherry/.arduino15/packages/arduino/tools/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin/avr-size -A /tmp/arduino/sketches/3A1B440EB19933555B05387038C51FC6/sensors.ino.elf
Sketch uses 10000 bytes (34%) of program storage space. Maximum is 28672 bytes.
Global variables use 458 bytes (17%) of dynamic memory, leaving 2102 bytes for local variables. Maximum is 2560 bytes.
Connecting to programmer: .
Found programmer: Id = "-1,-1,-"; type = 1
    Software Version = 9.0; Hardware Version = ,.3
avrdude: error: buffered memory access not supported. Maybe it isn't
a butterfly/AVR109 but a AVR910 device?
avrdude: initialization failed, rc=-1
         Double check connections and try again, or use -F to override
         this check.

avrdude: error: programmer did not respond to command: leave prog mode

