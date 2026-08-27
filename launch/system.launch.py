import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    plan_file_name = LaunchConfiguration('filename')
    fabric_config = LaunchConfiguration('fabric_config')

    declare_plan_file_name = DeclareLaunchArgument(
        'filename',
        default_value='moma_nav2_1.xml',
        description='Name of the plan file in omron_moma_capabilities/plans'
    )

    declare_fabric_config = DeclareLaunchArgument(
        'fabric_config',
        default_value=PathJoinSubstitution([FindPackageShare('fabric_server'), 'config', 'fabric.yaml']),
        description='Absolute path to the fabric configuration file'
    )

    plan_file_path = PathJoinSubstitution([FindPackageShare('omron_moma_capabilities'), 'plans', plan_file_name])

    fabric_launch_path = os.path.join(get_package_share_directory('fabric_server'), 'launch', 'fabric.launch.py')

    fabric = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(fabric_launch_path),
        launch_arguments={
            'plan_file_path': plan_file_path,
            'fabric_config': fabric_config,
        }.items(),
    )
    
    return LaunchDescription([
        declare_plan_file_name,
        declare_fabric_config,
        fabric
    ])

