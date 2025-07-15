#!/usr/bin/env python3
"""
MCP Scheduler API客户端示例

此脚本展示如何通过编程方式与MCP Scheduler交互，
包括连接到服务器、创建任务、运行任务和处理错误。
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# 确保MCP客户端库已安装
try:
    from mcp.client import StdioClient, SseClient
    from mcp.errors import McpError
except ImportError:
    print("错误: 未找到MCP客户端库。请安装: uv pip install 'mcp[client]>=1.4.0'")
    sys.exit(1)

# 获取MCP Scheduler路径
SCHEDULER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MAIN_SCRIPT = os.path.join(SCHEDULER_PATH, "main.py")

async def scheduler_demo():
    """演示与MCP Scheduler的交互"""
    print(f"[{datetime.now()}] 启动MCP Scheduler客户端演示...")
    
    # 启动MCP Scheduler作为子进程
    process_args = ["python", MAIN_SCRIPT]
    print(f"[{datetime.now()}] 连接到MCP Scheduler: {' '.join(process_args)}")
    
    try:
        async with StdioClient.create_subprocess(process_args) as client:
            # 获取服务器信息
            server_info = await client.call("get_server_info")
            print(f"[{datetime.now()}] 连接到 {server_info['name']} 版本 {server_info['version']}")
            
            # 列出所有任务
            tasks = await client.call("list_tasks")
            print(f"[{datetime.now()}] 当前有 {len(tasks)} 个任务")
            
            # 添加一个命令任务
            print(f"[{datetime.now()}] 创建命令任务...")
            cmd_task = await client.call(
                "add_command_task", 
                {
                    "name": "示例命令任务",
                    "schedule": "*/5 * * * *",  # 每5分钟
                    "command": "echo 'MCP Scheduler测试 - $(date)' >> /tmp/mcp_scheduler_test.log",
                    "description": "通过API创建的测试任务",
                    "do_only_once": False
                }
            )
            print(f"[{datetime.now()}] 创建命令任务成功: {cmd_task['id']}")
            
            # 立即运行任务
            print(f"[{datetime.now()}] 立即运行任务...")
            run_result = await client.call(
                "run_task_now", 
                {"task_id": cmd_task['id']}
            )
            print(f"[{datetime.now()}] 任务执行结果: {run_result['execution']['status']}")
            
            # 获取任务执行历史
            print(f"[{datetime.now()}] 获取任务执行历史...")
            executions = await client.call(
                "get_task_executions", 
                {"task_id": cmd_task['id']}
            )
            print(f"[{datetime.now()}] 任务执行历史: {json.dumps(executions, indent=2)}")
            
            # 更新任务
            print(f"[{datetime.now()}] 更新任务...")
            updated_task = await client.call(
                "update_task", 
                {
                    "task_id": cmd_task['id'],
                    "description": "已更新的测试任务描述"
                }
            )
            print(f"[{datetime.now()}] 更新任务成功: {updated_task['id']}")
            
            # 禁用任务
            print(f"[{datetime.now()}] 禁用任务...")
            disabled_task = await client.call(
                "disable_task", 
                {"task_id": cmd_task['id']}
            )
            print(f"[{datetime.now()}] 禁用任务成功: {disabled_task['id']}")
            
            # 启用任务
            print(f"[{datetime.now()}] 启用任务...")
            enabled_task = await client.call(
                "enable_task", 
                {"task_id": cmd_task['id']}
            )
            print(f"[{datetime.now()}] 启用任务成功: {enabled_task['id']}")
            
            # 删除任务
            print(f"[{datetime.now()}] 删除任务...")
            await client.call(
                "remove_task", 
                {"task_id": cmd_task['id']}
            )
            print(f"[{datetime.now()}] 删除任务成功")
            
            print(f"[{datetime.now()}] 演示完成!")
    
    except McpError as e:
        print(f"[{datetime.now()}] MCP API错误: {e}")
        return 1
    except ConnectionError:
        print(f"[{datetime.now()}] 无法连接到MCP Scheduler")
        return 1
    except Exception as e:
        print(f"[{datetime.now()}] 未预期的错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(scheduler_demo())
    sys.exit(exit_code)
