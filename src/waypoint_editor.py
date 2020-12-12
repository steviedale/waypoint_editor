import rclpy
from rclpy.node import Node


class WaypointEditor(Node):
    def __init__(self):
        super().__init__('waypoint_editor')
        self.get_logger().warn("now we're cookin'")


def main(args=None):
    rclpy.init(args=args)
    node = WaypointEditor()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
