# 使用 Ubuntu 作为基础镜像
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

# 更新源，安装必要的软件包
RUN sed -i 's|http://[^ ]*|http://mirrors.aliyun.com/ubuntu|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y curl cron supervisor

# 将应用程序文件复制到容器中
COPY crawlers/dist /workspace
COPY aimodels/ /workspace
RUN pip install crawlers-0.0.1-py3-none-any.whl && \
    pip install -i https://mirrors.aliyun.com/pypi/simple/ "fastapi[standard]" pandas scikit-learn

# 复制cron和supervisor配置
COPY smartrade_cron /workspace
COPY supervisord.conf /workspace
RUN cp /workspace/smartrade_cron /etc/cron.d/smartrade_cron && \
    mkdir -p /var/log/supervisor && \
    touch /var/log/supervisor/supervisord.log && \
    cp /workspace/supervisord.conf /etc/supervisor/conf.d/supervisord.conf && \
    chmod 0644 /etc/cron.d/smartrade_cron && \
    crontab /etc/cron.d/smartrade_cron

WORKDIR /workspace/src/aimodels/

# 启动命令
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
