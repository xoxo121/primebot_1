import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class LineFollowerNode(Node):
    def __init__(self):
        super().__init__('line_follower_node')

        # Initialize publishers and subscribers
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscribers = {
            'infrared_1': self.create_subscription(LaserScan, '/infrared_1', self.infrared_callback, 10),
            'infrared_2': self.create_subscription(LaserScan, '/infrared_2', self.infrared_callback, 10),
            'infrared_3': self.create_subscription(LaserScan, '/infrared_3', self.infrared_callback, 10),
            'infrared_4': self.create_subscription(LaserScan, '/infrared_4', self.infrared_callback, 10),
            'infrared_5': self.create_subscription(LaserScan, '/infrared_5', self.infrared_callback, 10),
        }
        
        # Initialize state
        self.infrared_data = {
            'infrared_1': None,
            'infrared_2': None,
            'infrared_3': None,
            'infrared_4': None,
            'infrared_5': None
        }

        # Timer for periodic updates
        self.timer = self.create_timer(0.1, self.control_robot)

    def infrared_callback(self, msg: LaserScan):
        topic_name = self.get_topic_name(msg)  # Get topic name for the incoming message
        if topic_name in self.infrared_data:
            self.infrared_data[topic_name] = msg.ranges  # Store range data

    def get_topic_name(self, msg):
        for topic_name, sub in self.subscribers.items():
            if msg._topic_name == sub.topic_name:
                return topic_name
        return None

    def control_robot(self):
        if not all(data is not None for data in self.infrared_data.values()):
            return
        
        # Extract sensor data
        left_sensors = [min(self.infrared_data['infrared_1']), min(self.infrared_data['infrared_2'])]
        right_sensors = [min(self.infrared_data['infrared_4']), min(self.infrared_data['infrared_5'])]
        center_sensor = min(self.infrared_data['infrared_3'])

        # Compute control commands
        twist_msg = Twist()
        twist_msg.linear.x = 0.2  # Default move forward speed

        if center_sensor < 0.1:  # If the center sensor detects a line
            twist_msg.angular.z = 0.0  # No turn
        elif min(left_sensors) < 0.1:  # If the left sensors detect the line
            twist_msg.angular.z = 0.5  # Turn right
        elif min(right_sensors) < 0.1:  # If the right sensors detect the line
            twist_msg.angular.z = -0.5  # Turn left
        else:
            twist_msg.angular.z = 0.0  # No turn if no line detected

        # Publish control commands
        self.cmd_vel_publisher.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = LineFollowerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
