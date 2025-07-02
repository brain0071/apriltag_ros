from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    zed_wrapper_dir = get_package_share_directory('zed_wrapper')
    apriltag_ros_dir = get_package_share_directory('apriltag_ros')
    param_file = os.path.join(apriltag_ros_dir, 'cfg', 'tags_36h11.yaml')
    zed_launch_file = os.path.join(zed_wrapper_dir, 'launch', 'zed_camera.launch.py')

    return LaunchDescription([
        
        # zed2i
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(zed_launch_file),
            launch_arguments={'camera_model': 'zed2i'}.items()
        ),
        
        # apriltags
        Node(
            package='apriltag_ros',
            executable='apriltag_node',
            name='apriltag_node',
            output='screen',
            remappings=[
                ('image_rect', '/zed/zed_node/left_raw_gray/image_raw_gray'),
                ('camera_info', '/zed/zed_node/left_raw_gray/camera_info'),
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
