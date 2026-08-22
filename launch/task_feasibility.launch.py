from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    params_file = PathJoinSubstitution(
        [FindPackageShare('omron_moma_capabilities'), 'config', 'task_feasibility.yaml']
    )
    return LaunchDescription(
        [
            Node(
                package='mobile_manipulator',
                executable='task_feasibility_service_node',
                name='task_feasibility_service_node',
                output='screen',
                parameters=[params_file],
            )
        ]
    )