/** TOPIC / SERVICES DEFINITION
*
*  TOPIC(type, topic, source, dest, priority, period, time_to_live)
*  QOSTOPIC(type, topic, source, dest, priority, period, time_to_live, queue_length)
*  TFTOPIC(topic, source, dest, priority, period, time_to_live)
*
*  SERVICE(type, topic, source, priority, time_to_live)
*
*/
/* Examples:
TOPIC(std_msgs::Int32,      "int",      0, "1", 75, 1000, 3000);
TFTOPIC(                    "/tf",      0, "1", 11,   10, 100);
*/

/* Convention:
    Node 0, Robot
    Node 1, Cloud
*/

/*  
We want to send the pose information generated 
by the turtlesim node at our "robot" (0) to our "cloud" (1)
*/

TOPIC(turtlesim::Pose, "/turtle1/pose", 0, "1", 100, 15, 1000);

/*  
And we want to send the velocity commands to control our "robot" (0)
*/

TOPIC(geometry_msgs::Twist, "/turtle1/cmd_vel", 1, "0", 100, 500, 1000);

/*  
Note that we can verify that the pose is published by turtlesim every 15 ms (or so) 
but we can only estimate how frequently the teleop_key will be publishing (500 ms seems 
reasonable for someone operating a keyboard) 
*/





