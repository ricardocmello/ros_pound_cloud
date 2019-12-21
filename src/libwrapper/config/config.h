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






