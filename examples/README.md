# MCP Scheduler 示例

本目录包含MCP Scheduler常见用例的示例脚本和配置。

## 配置文件示例

### aws_q_config.json

一个专为Amazon Q集成优化的配置文件示例。

**特点：**
- 使用stdio传输模式，适合与Amazon Q集成
- 启用AWS Q模型集成（`use_aws_q_model: true`）
- 不需要OpenAI API密钥
- 包含基本的日志和数据库设置

**使用方法：**

```bash
# 使用AWS Q配置启动调度器
uv run start_with_aws_q.py --config examples/aws_q_config.json
```

## 备份脚本

### backup_mcp_config.sh

一个用于创建Amazon Q MCP配置文件日常备份的shell脚本，使用基于日期的命名方式。

**功能：**
- 创建带有日期后缀的备份（YYYYMMDD格式）
- 创建专用的备份目录
- 包含可选的保留策略，自动删除旧备份
- 提供确认输出

**通过Amazon Q使用：**

您可以通过Amazon Q使用自然语言来创建一个使用此脚本的定时任务：

```
创建一个定时任务，每天晚上10:30运行/home/ec2-user/scheduler-mcp/examples/backup_mcp_config.sh脚本
```

**通过编程API使用：**

```python
# 添加为定时任务
await scheduler.add_command_task(
    name="备份MCP配置",
    schedule="30 22 * * *",  # 每天晚上10:30运行
    command="/path/to/examples/backup_mcp_config.sh",
    description="Amazon Q MCP配置的每日备份",
    do_only_once=False  # 重复执行的任务
)
```

## API客户端示例

### api_client_example.py

一个完整的Python示例脚本，展示如何通过编程方式与MCP Scheduler交互。

**功能：**
- 连接到MCP Scheduler服务
- 创建、运行、更新和删除任务
- 获取任务执行历史
- 处理错误和异常

**使用方法：**

```bash
# 确保已安装MCP客户端库
uv pip install "mcp[client]>=1.4.0"

# 运行示例
./api_client_example.py
```

**学习要点：**
- 如何建立与MCP Scheduler的连接
- 如何调用各种API方法
- 如何处理API响应和错误
- 完整的任务生命周期管理

## Amazon Q集成示例

MCP Scheduler可以与Amazon Q一起使用，通过自然语言创建和管理定时任务。以下是一些示例提示：

1. **创建备份任务：**
   ```
   创建一个定时任务，每晚10:30备份我的~/.aws/amazonq/mcp.json文件
   ```

2. **创建系统监控任务：**
   ```
   设置一个每小时检查系统内存使用情况并记录到文件的任务
   ```

3. **创建提醒：**
   ```
   每周一上午9:00提醒我参加团队会议
   ```

4. **修改现有任务：**
   ```
   将备份任务的运行时间从10:30改为午夜
   ```

5. **列出所有任务：**
   ```
   显示我所有的定时任务
   ```

6. **删除任务：**
   ```
   删除系统监控任务
   ```

## 注意事项

- MCP Scheduler创建的任务是应用级任务，不是系统级crontab任务
- 任务只有在MCP Scheduler服务运行时才会执行
- 如果需要系统级定时任务，请考虑使用操作系统的crontab或systemd定时器
