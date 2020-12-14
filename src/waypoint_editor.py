import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import yaml
import time
from visualization_msgs.msg import MarkerArray, Marker
from geometry_msgs.msg import Point
from rclpy.qos import qos_profile_system_default


class WaypointEditor(Node):
    def __init__(self):
        super().__init__('waypoint_editor')
        self.service = self.create_service(Trigger, "load", self.load_cb)
        self.file_path = "/home/stevie/workspaces/tera/tera_ws/src/tera_ros2/tera_support/toolpaths/left_side/Critical2/HalfInchSpacing.yaml"
        # self.file_path = "/home/stevie/workspaces/waypoint_ws/src/waypoint_editor/left_side/Critical2/HalfInchSpacing.yaml"
        self.publisher = self.create_publisher(MarkerArray, 'markers', qos_profile_system_default)

    def load_cb(self, request, response):
        self.get_logger().warn("now we're cookin'")

        with open(self.file_path, 'r') as f:
            data = yaml.load(f)

        array = MarkerArray()
        id = 0

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
            line_marker.id = id
            id += 1

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
                marker.id = id

                point = Point()
                point.x = float(waypoint['position']['x'])
                point.y = float(waypoint['position']['y'])
                point.z = float(waypoint['position']['z'])
                line_marker.points.append(point)

                array.markers.append(marker)
                # self.publisher.publish(array)
                # time.sleep(0.5)
                id += 1

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
