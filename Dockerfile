ARG ROS_DISTRO=humble
FROM ros:${ROS_DISTRO}-ros-base-jammy

SHELL ["/bin/bash", "-c"]

ARG ROS_DISTRO=humble
ARG LIBREALSENSE_REF=v2.56.5
ARG REALSENSE_ROS_REF=4.56.4
ARG BUILD_JOBS=2
ARG TARGETARCH
ARG USERNAME=root



RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libeigen3-dev \
    libssl-dev \
    libudev-dev \
    libusb-1.0-0-dev \
    pkg-config \
    python3-colcon-common-extensions \
    ros-${ROS_DISTRO}-cv-bridge \
    ros-${ROS_DISTRO}-diagnostic-updater \
    ros-${ROS_DISTRO}-image-transport \
    ros-${ROS_DISTRO}-lifecycle-msgs \
    ros-${ROS_DISTRO}-rclcpp-action \
    ros-${ROS_DISTRO}-rclcpp-components \
    ros-${ROS_DISTRO}-rclcpp-lifecycle \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    ros-${ROS_DISTRO}-tf2-ros \
    ros-${ROS_DISTRO}-xacro \
    ros-${ROS_DISTRO}-compressed-image-transport \
    ros-${ROS_DISTRO}-compressed-depth-image-transport \
    && rm -rf /var/lib/apt/lists/*

RUN case "${TARGETARCH}" in \
        amd64) LIBUSB_ARCH=x86_64-linux-gnu ;; \
        arm64) LIBUSB_ARCH=aarch64-linux-gnu ;; \
        *) echo "Unsupported target architecture: ${TARGETARCH}" >&2; exit 1 ;; \
    esac && \
    git clone --depth 1 --branch ${LIBREALSENSE_REF} \
        https://github.com/realsenseai/librealsense.git /tmp/librealsense && \
    cmake -S /tmp/librealsense -B /tmp/librealsense/build \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_EXAMPLES=OFF \
        -DBUILD_GRAPHICAL_EXAMPLES=OFF \
        -DBUILD_PYTHON_BINDINGS=OFF \
        -DBUILD_TOOLS=OFF \
        -DBUILD_UNIT_TESTS=OFF \
        -DLIBUSB_INC=/usr/include/libusb-1.0 \
        -DLIBUSB_LIB=/usr/lib/${LIBUSB_ARCH}/libusb-1.0.so \
        -DFORCE_RSUSB_BACKEND=ON && \
    cmake --build /tmp/librealsense/build --parallel ${BUILD_JOBS} && \
    cmake --install /tmp/librealsense/build && \
    mkdir -p /etc/udev/rules.d && \
    cp /tmp/librealsense/config/99-realsense-libusb.rules \
        /etc/udev/rules.d/99-realsense-libusb.rules && \
    ldconfig && \
    rm -rf /tmp/librealsense

WORKDIR /ws

RUN git clone --depth 1 --branch ${REALSENSE_ROS_REF} \
    https://github.com/realsenseai/realsense-ros.git src/realsense-ros

COPY config/ config/

RUN source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build --merge-install \
        --cmake-args \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_TESTING=OFF

COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    chown -R ${USERNAME}:${USERNAME} /ws

ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

USER ${USERNAME}

ENTRYPOINT ["/entrypoint.sh"]
CMD ["ros2", "launch", "realsense2_camera", "rs_launch.py", "camera_name:=realsense", "config_file:=/ws/config/params.yaml"]
