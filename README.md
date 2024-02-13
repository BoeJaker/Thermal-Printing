# Thermal-Printing
A collection of useful scripts for thermal printers  
  
To use the server script your user will need write permission for the usb printer. Instructions below:  
    
Find the device name:
```lsusb```  
<device_name> usually look like lp0, lp1 ect  
  
Give your user write permissions:
```sudo chmod +w /dev/usb/<device_name>```  
  
Test its wroking with:  
```echo "Hello World" > /dev/usb/<device_name>  


