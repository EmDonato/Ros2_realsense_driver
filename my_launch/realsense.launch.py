from launch import LaunchDescription
from launch_ros.actions import Node

'''
D435i 640×480 @ 30 Hz

RGB:
manual exposure
manual gain
manual WB

Depth:
manual exposure = 8.5 ms
gain = 16

Active stereo:
emitter = ON
laser = 300
High Density = ON

Processing:
align depth      ON
spatial          ON
temporal         OFF
hole filling     OFF
disparity        OFF
decimation       OFF

Other:
pointcloud       OFF
IMU              OFF
IR publication   OFF
'''

def generate_launch_description():
    realsense_node = Node(
        package="realsense2_camera",
        executable="realsense2_camera_node",
        name="realsense",
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
            "depth_module.exposure": 10000,  # 10 ms
            "depth_module.gain": 16,


            "depth_module.emitter_enabled": 1,
            "depth_module.laser_power": 300.0,

            "depth_module.visual_preset": 4,
            "align_depth.enable": True,
            "pointcloud.enable": False,


            "enable_infra1": False,
            "enable_infra2": False,
            "enable_gyro": False,
            "enable_accel": False,


            "publish_tf": True,

            "decimation_filter.enable": False,

            "spatial_filter.enable": True,
            "spatial_filter.filter_magnitude": 2,
            "spatial_filter.filter_smooth_alpha": 0.5,
            "spatial_filter.filter_smooth_delta": 20,
            "spatial_filter.holes_fill": 0,

            "temporal_filter.enable": True,
            "temporal_filter.filter_smooth_alpha": 0.4,
            "temporal_filter.filter_smooth_delta": 20,

            "hole_filling_filter.enable": False,


            "disparity_filter.enable": False,


            "color_qos": "SENSOR_DATA",
            "depth_qos": "SENSOR_DATA",
            "depth_registered_qos": "SENSOR_DATA",
        }],
        output="screen",
    )

    return LaunchDescription([
        realsense_node,
    ])