from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    
    apriltag_ros_dir = get_package_share_directory('apriltag_ros')
    param_file = os.path.join(apriltag_ros_dir, 'cfg', 'tags_36h10.yaml')
    cam_yaml_path = '/home/naodai/Workspace/camera_usb_ws/src/apriltag_ros/cfg/camera_info.yaml'
    cam_info_url = 'file://' + cam_yaml_path  

    return LaunchDescription([
        
       Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            name='usb_cam',
            namespace='camera1',
            output='screen',
            parameters=[{
                'camera_name': 'camera1',
                'video_device': '/dev/video0',
                'image_width': 640,
                'image_height': 480,
                'framerate': 30.0,
                'camera_info_url': cam_info_url,
            }],
        ),
        
        # apriltags
        Node(
            package='apriltag_ros',
            executable='apriltag_node',
            name='apriltag_node',
            output='screen',
            remappings=[
                ('image_rect', '/camera1/image_raw'),
                ('camera_info', '/camera1/camera_info'),
            ],
            parameters=[param_file],
        ),
        
        # apriltags odometry
        Node(
            package='tank_odometry',
            executable='odometry_node',
            name='odometry_node',
            output='screen',
        )

    ])
