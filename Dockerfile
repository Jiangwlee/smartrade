# 使用 Ubuntu 作为基础镜像
# 第一阶段：构建阶段
FROM python:3.12

# 设置阿里云镜像源
RUN echo "deb https://mirrors.aliyun.com/debian/ bookworm main non-free non-free-firmware contrib\ndeb-src https://mirrors.aliyun.com/debian/ bookworm main non-free non-free-firmware contrib\ndeb https://mirrors.aliyun.com/debian-security/ bookworm-security main\ndeb-src https://mirrors.aliyun.com/debian-security/ bookworm-security main\ndeb https://mirrors.aliyun.com/debian/ bookworm-updates main non-free non-free-firmware contrib\ndeb-src https://mirrors.aliyun.com/debian/ bookworm-updates main non-free non-free-firmware contrib\ndeb https://mirrors.aliyun.com/debian/ bookworm-backports main non-free non-free-firmware contrib\ndeb-src https://mirrors.aliyun.com/debian/ bookworm-backports main non-free non-free-firmware contrib" > /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y cron supervisor

# 将应用程序文件复制到容器中
COPY crawlers/dist /workspace
COPY smartrade/ /workspace
RUN pip install /workspace/crawlers-0.0.1-py3-none-any.whl && \
    pip install -i https://mirrors.aliyun.com/pypi/simple/ "fastapi[standard]"

# 复制cron和supervisor配置
COPY smartrade_cron /workspace
COPY supervisord.conf /workspace
RUN cp /workspace/smartrade_cron /etc/cron.d/smartrade_cron && \
    mkdir -p /var/log/supervisor && \
    touch /var/log/supervisor/supervisord.log && \
    cp /workspace/supervisord.conf /etc/supervisor/conf.d/supervisord.conf && \
    chmod 0644 /etc/cron.d/smartrade_cron && \
    crontab /etc/cron.d/smartrade_cron

WORKDIR /workspace/src/smartrade/

# 启动命令
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
