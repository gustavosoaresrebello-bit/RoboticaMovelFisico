# Usa a imagem oficial do ROS Noetic (que já vem com Ubuntu 20.04)
FROM osrf/ros:noetic-desktop-full

# Instala ferramentas básicas e dependências de build
RUN apt-get update && apt-get install -y \
    python3-rosdep \
    python3-rosinstall \
    python3-vcstools \
    python3-catkin-tools \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Inicializa o rosdep
RUN rosdep update

# Configura o shell padrão para bash e faz o source do ROS no .bashrc
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

WORKDIR /home/workspace