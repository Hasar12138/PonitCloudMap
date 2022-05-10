# Ouster Part
## Wired Connection Setting
![图片](https://raw.github.com/Hasar12138/PonitCloudMap/main/Wired%20connection.png)
## Build Ouster-ros package
``` shell
mkdir  -p workspace/src
cd workspace/src 
git clone https://github.com/ouster-lidar/ouster_example.git
cd ..
catkin_make
``` 
# Source the Ouster Package
``` shell
source devel/setup.bash
```
# Run the Package
``` shell
roslaunch ouster_ros ouster.launch sensor_hostname:=os-122145000795.local metadata:=./meta.json viz:=true
```
Wait for 10s......

# Picam360 part
## Install usb_cam package
``` shell
sudo apt install ros-melodic-usb-cam
```
## Run the package
``` shell
roslaunch usb_cam usb_cam-test.launch
```
### config to the launch file 
``` shell
roscd usb_cam/launch/
code code usb_cam-test.launch
```
### launch file 
``` launch
<launch>
  <node name="usb_cam" pkg="usb_cam" type="usb_cam_node" output="screen" >
    <param name="video_device" value="/dev/video0" />    >>>>>>> Chnage to /dev/video2<<<<<<<<<<<<<<
    <param name="image_width" value="1280" />
    <param name="image_height" value="720" />
    <param name="pixel_format" value="yuyv" />
    <param name="camera_frame_id" value="usb_cam" />
    <param name="io_method" value="mmap"/>
  </node>
  <node name="image_view" pkg="image_view" type="image_view" respawn="false" output="screen">
    <remap from="image" to="/usb_cam/image_raw"/>
    <param name="autosize" value="true" />
  </node>
</launch>
```


# Make ROS bag
``` shell
rosbag record [TOPIC_NAME_1] [TOPIC_NAME_2]  # record specific topic 
rosbag record -a  # record all topic 
```


