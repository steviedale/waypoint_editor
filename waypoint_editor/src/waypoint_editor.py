import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import yaml
import time
from visualization_msgs.msg import MarkerArray, Marker
from geometry_msgs.msg import Point
from rclpy.qos import qos_profile_system_default
from waypoint_editor_msgs.srv import SetString
import os


class WaypointEditor(Node):
    def __init__(self):
        super().__init__('waypoint_editor')
        self.load_service = self.create_service(Trigger, "load", self.load_cb)
        self.set_file_service = self.create_service(SetString, "set_file", self.set_file_cb)
        self.clear_service = self.create_service(Trigger, 'clear', self.clear_cb)
        self.file_start = '/home/stevie/workspaces/tera/tera_ws/src/tera_ros2/tera_support/toolpaths/right_side'
        self.file_path = ''
        self.id_count = 0
        # self.file_path = "/home/stevie/workspaces/tera/tera_ws/src/tera_ros2/tera_support/toolpaths/left_side/Critical2/HalfInchSpacing.yaml"
        # self.file_path = "/home/stevie/workspaces/waypoint_ws/src/waypoint_editor/left_side/Critical2/HalfInchSpacing.yaml"
        self.publisher = self.create_publisher(MarkerArray, 'markers', qos_profile_system_default)

    def set_file_cb(self, request, response):
        self.file_path = os.path.join(self.file_start, request.str)
        response.success = True
        return response

    def clear_cb(self, request, response):
        for i in range(self.id_count):
            m = Marker()

    def load_cb(self, request, response):
        self.get_logger().warn("now we're cookin'")

        with open(self.file_path, 'r') as f:
            data = yaml.load(f)

        array = MarkerArray()

        for waypoints in data[0]['region']:
            if 'waypoints' not in waypoints:
                continue

            line_marker = Marker()
            line_marker.header.frame_id = '/base_link'
            line_marker.type = Marker.LINE_STRIP
            line_marker.scale.x = 0.002
            line_marker.color.a = 1.0
            line_marker.color.r = 0.0
            line_marker.color.g = 1.0
            line_marker.color.b = 0.0
            line_marker.id = self.id_count
            self.id_count += 1

            for waypoint in waypoints['waypoints']:
                waypoint = waypoint['tool_poses']
                marker = Marker()
                marker.header.frame_id = '/base_link'
                marker.type = Marker.CUBE
                marker.scale.x = 0.005
                marker.scale.y = 0.005
                marker.scale.z = 0.005
                marker.color.a = 1.0
                marker.color.r = 1.0
                marker.color.g = 0.0
                marker.color.b = 0.0
                marker.pose.position.x = float(waypoint['position']['x'])
                marker.pose.position.y = float(waypoint['position']['y'])
                marker.pose.position.z = float(waypoint['position']['z'])
                marker.pose.orientation.x = float(waypoint['orientation']['x'])
                marker.pose.orientation.y = float(waypoint['orientation']['y'])
                marker.pose.orientation.z = float(waypoint['orientation']['z'])
                marker.pose.orientation.w = float(waypoint['orientation']['w'])
                marker.id = self.id_count

                point = Point()
                point.x = float(waypoint['position']['x'])
                point.y = float(waypoint['position']['y'])
                point.z = float(waypoint['position']['z'])
                line_marker.points.append(point)

                array.markers.append(marker)
                # self.publisher.publish(array)
                # time.sleep(0.5)
                self.id_count += 1

            array.markers.append(line_marker)
            self.publisher.publish(array)

        response.success = True
        return response


def main(args=None):
    rclpy.init(args=args)
    node = WaypointEditor()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
