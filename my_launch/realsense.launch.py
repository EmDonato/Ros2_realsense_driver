from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    realsense_node = Node(
        package="realsense2_camera",
        executable="realsense2_camera_node",
        name="realsense",
        # Nessun namespace
        parameters=[{
            "enable_color": True,
            "enable_depth": True,
            "enable_sync": True,

            "rgb_camera.color_format": "RGB8",
            "rgb_camera.color_profile": "640x480x30",
            "rgb_camera.enable_auto_exposure": False,
            "rgb_camera.exposure": 250,
            "rgb_camera.gain": 64,
            "rgb_camera.enable_auto_white_balance": False,
            "rgb_camera.white_balance": 3800.0,

            "depth_module.depth_profile": "640x480x30",
            "depth_module.enable_auto_exposure": False,
            "depth_module.enable_auto_exposure": False,
            "depth_module.exposure": 10000,       # 8,5 ms
            "depth_module.gain": 16,             # gain minimo, meno rumore

            "align_depth.enable": True,
            "pointcloud.enable": False,
            "pointcloud.allow_no_texture_points": False,

            "enable_infra": False,
            "enable_infra1": False,
            "enable_infra2": False,
            "enable_gyro": False,
            "enable_accel": False,

            "publish_tf": True,

            "decimation_filter.enable": False,

            "spatial_filter.enable": True,
            "spatial_filter.filter_smooth_alpha": 0.5,
            "spatial_filter.filter_smooth_delta": 20,

            "temporal_filter.enable": True,
            "temporal_filter.filter_smooth_alpha": 0.4,
            "temporal_filter.filter_smooth_delta": 20,

            "hole_filling_filter.enable": False,

            "color_qos": "SENSOR_DATA",
            "depth_qos": "SENSOR_DATA",
            "depth_registered_qos": "SENSOR_DATA",


        }],
        output="screen",
    )

    return LaunchDescription([
        realsense_node,
    ])