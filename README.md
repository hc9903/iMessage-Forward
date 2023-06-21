# iMessage-Forward
通过 Mac 转发 iMessage 信息

# 依赖
```
pip install git+https://github.com/my-other-github-account/imessage_tools.git
```

# 使用方法
执行 `crontab -e`, 添加以下内容
```
* * * * * /opt/homebrew/bin/python3 ~/imessage_forwarder/forwarder.py
```

对于高版本 macOS, 可能需要在设置中授予 cron 完全磁盘访问权限
