# smartrade

一个聪明的自动化复盘系统

# 部署

编译crawlers:
```
# cd crawlers
# hatch build
```

构建后端 docker:

```
# docker build -t jiangwl/smartrade .
```

编译前端代码：

```
# cd smartrade-frontend
# npm run build
```

将前端代码拷贝到 www 目录

```
# cp dist ../www/
```

启动：

```
docker compose up
```
