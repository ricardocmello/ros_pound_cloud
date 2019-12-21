# ros-pound-cloud-pkg
This is NOT the original ros-pound package by Dr. Danilo Tardiolli, which you'll find at https://github.com/dantard/unizar-pound-ros-pkg. 

This is a modified version of ros-pound, the PoundCloud. The main modifications can be listed as:

* The `ros-pound` ROS node can now deal with WiFi working on infrastructure mode (your regular WiFi connection to an access point/router); in fact, it does not matter if you're using WiFi or cable, it ~~will~~ should work as long as you have a valid IP on that interface; this also means that the multi-hop feature deprecated and shouldn't be used;
* Machines using `ros-pound` to communicate are not bounded to a base IP. This is particularly useful if you're using a network which you do not own, such as your university network. You should configure the pair node-IP as a dictionary under the field `node_ip` on `libwrapper/config/config.yaml`;
* In case you want to communicate a single machine with a local IP (behind a NAT) and a remote machine with a public IP, you can use the `commwrapper.py` ROS node to stablish bidirectional communication between them before automatically initializing `ros-pound`.

To install, clone this repository inside your ROS workspace and rebuild your workspace (`catkin_make`).

Switch to branch 'example' to see a simple working example on how to use the PoundCloud. 

Usage of the `ros-pound` node:
`rosrun ros_pound ros-pound --node-id 0`

Parameter `node-id` specifies the identifier of the local node. The IP of each node should be configured at `libwrapper/config/config.yaml` as:
`node_ip: {0: 10.30.0.44, 1: 10.30.0.56}`

Usage of the `commwrapper` node:
`rosrun ros_pound commwrapper.py 0`

The parameter passed is the `node-id`. In case you're using `commwrapper`, you must asign node 0 to be the machine with a local IP and node 1 to be the machine with a public IP.

By default, ros-pound uses UDP/IP communication. 

The topics to be transported must be specified in the `libwrapper/config/config.h` file with the format:

`TOPIC(type, topic_name, source, dest, priority, period, time_to_live);`

where

* `type` specifies the data type for example `std_msgs::Float64` 
* `topic_name` specifies the name of the topic, for example `"float_number"` 
* `source` is the source node of the topic, for example `0` (number)
* `dest` specifies the destination node(s) as text for example `"0,1,2"` (string) however for the moment Pound only support unicast (only one node should be specified) 
* `priority` specifies the priority associated to the topic for example `56`. Must be between 0 and 127 
* `period` the expected period of the topic in ms, for example `100` 
* `time_to_live` period during the which the message is considered valid in ms, for example `500` 

The data type used must be specified in the `config/data_types.h` file. For example:

`#include <std_msgs/Float64.h>`

The complete list of options for the YAML file is:

```     
node_ip: {0: 10.30.0.44, 1: 10.30.0.56}
node_port_rx: {0: 26000, 1: 26001}
node_port_tx: {0: 26500, 1: 26501}

feedback: false
auto_tuning: false

queue: 50

rate_mbps: 54.0
quiet: true
```




