# MCP Scheduler

A robust task scheduler server built with Model Context Protocol (MCP) for scheduling and managing various types of automated tasks.

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

MCP Scheduler is a versatile task automation system that allows you to schedule and run different types of tasks:

- **Shell Commands**: Execute system commands on a schedule
- **API Calls**: Make HTTP requests to external services
- **AI Tasks**: Generate content through OpenAI models
- **Reminders**: Display desktop notifications with sound

The scheduler uses cron expressions for flexible timing and provides a complete history of task executions. It's built on the Model Context Protocol (MCP), making it easy to integrate with AI assistants and other MCP-compatible clients.

## Features

- **Multiple Task Types**: Support for shell commands, API calls, AI content generation, and desktop notifications
- **Cron Scheduling**: Familiar cron syntax for precise scheduling control
- **Run Once or Recurring**: Option to run tasks just once or repeatedly on schedule
- **Execution History**: Track successful and failed task executions
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Interactive Notifications**: Desktop alerts with sound for reminder tasks
- **MCP Integration**: Seamless connection with AI assistants and tools
- **Robust Error Handling**: Comprehensive logging and error recovery

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://astral.sh/uv) (recommended package manager)

### Installing uv (recommended)

```bash
# For Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# For Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installing uv, restart your terminal to ensure the command is available.

### Project Setup with uv (recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-scheduler.git
cd mcp-scheduler

# Create and activate a virtual environment with uv
uv venv
source .venv/bin/activate  # On Unix/MacOS
# or
.venv\Scripts\activate     # On Windows

# Install dependencies with uv
uv pip install -r requirements.txt
```

### Standard pip installation (alternative)

If you prefer using standard pip:

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-scheduler.git
cd mcp-scheduler

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/MacOS
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
# Activate the virtual environment first
source .venv/bin/activate  # On Unix/MacOS
# or
.venv\Scripts\activate     # On Windows

# Run with default settings (stdio transport)
uv run main.py

# Run with AWS Q integration (recommended for Amazon Q users)
uv run start_with_aws_q.py

# Run with debug mode for detailed logging
uv run main.py --debug

# Run with custom configuration file
uv run main.py --config /path/to/config.json
```

The server uses stdio transport by default, which is ideal for integration with Amazon Q and other MCP clients. The server automatically handles the communication protocol based on the environment.

### Integrating with Amazon Q, Claude Desktop or other MCP Clients

### Amazon Q Integration

To use MCP Scheduler with Amazon Q:

1. Make sure you have Amazon Q CLI installed
2. Run the scheduler with the AWS Q model patch:

```bash
# Start the scheduler with AWS Q integration
python start_with_aws_q.py
```

This will automatically register the scheduler with Amazon Q, allowing you to create and manage tasks through natural language commands.

Example commands:
- "Create a scheduled task to backup my config file every night at 10:30 PM"
- "Show me all my scheduled tasks"
- "Run the backup task now"

See the `examples` directory for more usage examples with Amazon Q.

### Claude Desktop Integration

To use your MCP Scheduler with Claude Desktop:

1. Make sure you have Claude Desktop installed
2. Open your Claude Desktop App configuration at:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
3. Create the file if it doesn't exist, and add your server:

```json
{
  "mcpServers": [
    {
      "type": "stdio",
      "name": "MCP Scheduler",
      "command": "python",
      "args": ["/path/to/your/mcp-scheduler/main.py"]
    }
  ]
}
```

Alternatively, use the `fastmcp` utility if you're using the FastMCP library:

```bash
# Install your server in Claude Desktop
fastmcp install main.py --name "Task Scheduler"
```

### Command Line Options

```
--address        Server address (default: localhost)
--port           Server port (default: 8080)
--transport      Transport mode (stdio or sse) (default: stdio)
--log-level      Logging level (default: INFO)
--log-file       Log file path (default: mcp_scheduler.log)
--db-path        SQLite database path (default: scheduler.db)
--config         Path to JSON configuration file
--ai-model       AI model to use for AI tasks (default: gpt-4o)
--version        Show version and exit
--debug          Enable debug mode with full traceback
--fix-json       Enable JSON fixing for malformed messages
```

When using with Amazon Q, most of these options are automatically configured by the `start_with_aws_q.py` script.
--config         Path to JSON configuration file
--ai-model       AI model to use for AI tasks (default: gpt-4o)
--version        Show version and exit
--debug          Enable debug mode with full traceback
--fix-json       Enable JSON fixing for malformed messages
```

### Configuration File

You can use a JSON configuration file instead of command-line arguments:

```json
{
  "server": {
    "name": "mcp-scheduler",
    "version": "0.1.0",
    "address": "localhost",
    "port": 8080,
    "transport": "stdio"
  },
  "database": {
    "path": "scheduler.db"
  },
  "logging": {
    "level": "INFO",
    "file": "mcp_scheduler.log"
  },
  "scheduler": {
    "check_interval": 5,
    "execution_timeout": 300
  },
  "ai": {
    "model": "gpt-4o",
    "use_aws_q_model": true,
    "openai_api_key": "your-api-key"  // Only needed if not using AWS Q model
  }
}
```

When using with Amazon Q, the `use_aws_q_model` should be set to `true` and no API key is required.

## 重要说明

### 任务类型和限制

MCP Scheduler是一个应用级任务调度服务，而不是系统级定时任务管理器：

- **应用级任务**：MCP Scheduler创建的任务存储在其自己的数据库中，只有在MCP Scheduler服务运行时才会执行
- **非系统级**：这些任务不是系统crontab或systemd定时器，不会在系统启动时自动运行
- **服务依赖**：如果MCP Scheduler服务停止，任务将不会执行
- **用户权限**：任务以运行MCP Scheduler的用户权限执行，而不是root权限

如果您需要系统级定时任务（在系统启动时自动运行或需要root权限），请考虑：

1. 使用操作系统的`crontab -e`或`systemctl`直接创建系统级定时任务
2. 创建一个MCP Scheduler任务，该任务执行脚本来管理系统级定时任务

### 持久化和服务管理

为确保MCP Scheduler在系统重启后继续运行，您可以：

1. 将其设置为系统服务（使用systemd）
2. 在用户登录时自动启动
3. 在云环境中作为容器或服务运行

## MCP Tool Functions

The MCP Scheduler provides the following tools:

### Task Management

- `list_tasks`: Get all scheduled tasks
- `get_task`: Get details of a specific task
- `add_command_task`: Add a new shell command task
- `add_api_task`: Add a new API call task
- `add_ai_task`: Add a new AI task
- `add_reminder_task`: Add a new reminder task with desktop notification
- `update_task`: Update an existing task
- `remove_task`: Delete a task
- `enable_task`: Enable a disabled task
- `disable_task`: Disable an active task
- `run_task_now`: Run a task immediately

### Execution and Monitoring

- `get_task_executions`: Get execution history for a task
- `get_server_info`: Get server information

## Cron Expression Guide

MCP Scheduler uses standard cron expressions for scheduling. Here are some examples:

- `0 0 * * *` - Daily at midnight
- `0 */2 * * *` - Every 2 hours
- `0 9-17 * * 1-5` - Every hour from 9 AM to 5 PM, Monday to Friday
- `0 0 1 * *` - At midnight on the first day of each month
- `0 0 * * 0` - At midnight every Sunday

## Environment Variables

The scheduler can be configured using environment variables:

- `MCP_SCHEDULER_NAME`: Server name (default: mcp-scheduler)
- `MCP_SCHEDULER_VERSION`: Server version (default: 0.1.0)
- `MCP_SCHEDULER_ADDRESS`: Server address (default: localhost)
- `MCP_SCHEDULER_PORT`: Server port (default: 8080)
- `MCP_SCHEDULER_TRANSPORT`: Transport mode (default: stdio)
- `MCP_SCHEDULER_LOG_LEVEL`: Logging level (default: INFO)
- `MCP_SCHEDULER_LOG_FILE`: Log file path
- `MCP_SCHEDULER_DB_PATH`: Database path (default: scheduler.db)
- `MCP_SCHEDULER_CHECK_INTERVAL`: How often to check for tasks (default: 5 seconds)
- `MCP_SCHEDULER_EXECUTION_TIMEOUT`: Task execution timeout (default: 300 seconds)
- `MCP_SCHEDULER_AI_MODEL`: OpenAI model for AI tasks (default: gpt-4o)
- `MCP_SCHEDULER_USE_AWS_Q_MODEL`: Use AWS Q model for AI tasks (default: false)
- `OPENAI_API_KEY`: API key for OpenAI tasks (not needed when using AWS Q model)

## Examples

MCP Scheduler可以通过两种方式使用：通过Amazon Q等MCP客户端的自然语言交互，或者通过编程方式直接调用API。

### 通过Amazon Q使用（推荐）

使用Amazon Q创建和管理任务非常简单，只需使用自然语言描述您想要的任务：

1. **创建命令任务**：
   ```
   创建一个定时任务，每天晚上10:30备份我的数据库到/backups目录
   ```

2. **创建API调用任务**：
   ```
   设置一个每6小时获取一次天气数据的任务
   ```

3. **创建AI任务**：
   ```
   每周一早上9点生成一份上周销售数据的摘要报告
   ```

4. **创建提醒任务**：
   ```
   每周二和周四上午9:30提醒我参加团队会议
   ```

5. **查看所有任务**：
   ```
   显示所有定时任务
   ```

6. **立即运行任务**：
   ```
   立即运行备份任务
   ```

### 通过编程API使用

如果您正在开发应用程序或脚本，可以通过编程方式与MCP Scheduler交互。以下是建立调用关系的简要指南：

### 1. 安装必要的依赖

```bash
# 使用uv安装（推荐）
uv pip install "mcp[client]>=1.4.0"
```

### 2. 建立连接并调用API

```python
import asyncio
from mcp.client import StdioClient

async def main():
    # 启动MCP Scheduler作为子进程
    process_args = ["uv", "run", "/path/to/scheduler-mcp/main.py"]
    async with StdioClient.create_subprocess(process_args) as client:
        # 获取服务器信息
        server_info = await client.call("get_server_info")
        print(f"连接到 {server_info['name']} 版本 {server_info['version']}")
        
        # 列出所有任务
        tasks = await client.call("list_tasks")
        print(f"当前有 {len(tasks)} 个任务")
        
        # 添加一个命令任务
        cmd_task = await client.call(
            "add_command_task", 
            {
                "name": "系统状态检查",
                "schedule": "*/30 * * * *",  # 每30分钟
                "command": "vmstat > /tmp/vmstat_$(date +%Y%m%d_%H%M).log",
                "description": "记录系统状态",
                "do_only_once": False
            }
        )
        print(f"创建命令任务: {cmd_task['id']}")
        
        # 立即运行一个任务
        run_result = await client.call(
            "run_task_now", 
            {"task_id": cmd_task['id']}
        )
        print(f"任务执行结果: {run_result['execution']['status']}")

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())
```

### 3. 连接到已运行的MCP Scheduler

如果MCP Scheduler已经在HTTP模式下运行，可以使用SSE客户端连接：

```python
import asyncio
from mcp.client import SseClient

async def connect_to_running_scheduler():
    async with SseClient("http://localhost:8080") as client:
        tasks = await client.call("list_tasks")
        print(f"当前有 {len(tasks)} 个任务")

asyncio.run(connect_to_running_scheduler())
```

### 4. 错误处理

```python
import asyncio
from mcp.client import StdioClient
from mcp.errors import McpError

async def robust_scheduler_client():
    try:
        process_args = ["uv", "run", "/path/to/scheduler-mcp/main.py"]
        async with StdioClient.create_subprocess(process_args) as client:
            try:
                result = await client.call("list_tasks")
                return result
            except McpError as e:
                print(f"MCP API错误: {e}")
                return []
    except Exception as e:
        print(f"连接错误: {e}")
        return []

asyncio.run(robust_scheduler_client())
```

### 完整示例

查看 `examples/api_client_example.py` 获取完整的API使用示例，包括：
- 连接到MCP Scheduler服务
- 创建、运行、更新和删除任务
- 获取任务执行历史
- 错误处理和异常管理

```bash
# 运行示例
cd examples
./api_client_example.py
```

### 示例脚本

`examples`目录包含了可直接使用的脚本和配置，适用于常见用例：

- `backup_mcp_config.sh`：一个用于备份Amazon Q MCP配置文件的脚本，包含基于日期的命名和保留策略

## MCP Tool Discovery

MCP Scheduler supports automatic tool discovery through the Model Context Protocol:

### Stdio Mode (Default)

When running in stdio mode (the default), tool discovery happens automatically through the MCP protocol. This is the recommended mode for use with Amazon Q and other MCP clients that support stdio communication.

```bash
# Run in stdio mode (default)
uv run main.py
```

### HTTP Mode (Optional)

If you need to run the server in HTTP mode, you can use the SSE transport and access the schema through the well-known endpoint:

```bash
# Run with HTTP server transport
uv run main.py --transport sse --port 8080
```

In HTTP mode, the server exposes a well-known endpoint for tool/schema auto-discovery:
- **Endpoint:** `/.well-known/mcp-schema.json` (on the HTTP port + 1, e.g., if your server runs on 8080, the schema is on 8081)
- **Purpose:** Allows clients and AI assistants to discover all available MCP tools and their parameters automatically.

You can access the schema at:
```
http://localhost:8081/.well-known/mcp-schema.json
```

### Example Schema Response

```json
{
  "tools": [
    {
      "name": "list_tasks",
      "description": "List all scheduled tasks.",
      "endpoint": "list_tasks",
      "method": "POST",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": false
      }
    },
    {
      "name": "add_command_task",
      "description": "Add a new shell command task.",
      "endpoint": "add_command_task",
      "method": "POST",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "schedule": {"type": "string"},
          "command": {"type": "string"},
          "description": {"type": "string"},
          "enabled": {"type": "boolean"},
          "do_only_once": {"type": "boolean"}
        },
        "required": ["name", "schedule", "command"],
        "additionalProperties": false
      }
    }
    // ... more tools ...
  ]
}
```

This schema is generated automatically from the registered MCP tools and always reflects the current server capabilities.

## Development

If you want to contribute or develop the MCP Scheduler further, here are some additional commands:

```bash
# Install the MCP SDK for development
uv pip install "mcp[cli]>=1.4.0"

# Or for FastMCP (alternative implementation)
uv pip install fastmcp

# Testing your MCP server
# With the MCP Inspector tool
mcp inspect --stdio -- uv run main.py

# Or with a simple MCP client
python -m mcp.client.stdio uv run main.py

# Running tests
uv run -m pytest

# Linting
uv pip install flake8
flake8 mcp_scheduler/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

