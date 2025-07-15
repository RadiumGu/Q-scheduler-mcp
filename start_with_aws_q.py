#!/usr/bin/env python3
# 简化版的 start_with_aws_q.py
# 使用 AWS Q 模型的启动脚本

import os
import sys
import json
import logging

# 设置环境变量
os.environ["MCP_SCHEDULER_TRANSPORT"] = "stdio"
os.environ["MCP_SCHEDULER_LOG_LEVEL"] = "DEBUG"
os.environ["MCP_SCHEDULER_LOG_FILE"] = "/home/ec2-user/scheduler-mcp/mcp_scheduler.log"
os.environ["MCP_SCHEDULER_DB_PATH"] = "/home/ec2-user/scheduler-mcp/scheduler.db"

# 设置日志记录
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   filename='/home/ec2-user/scheduler-mcp/start_with_aws_q.log')
logger = logging.getLogger(__name__)

# 导入原始的 main 模块
import main

# 导入 Executor 类
from mcp_scheduler.executor import Executor

# 保存原始的 _execute_ai_task 方法
original_execute_ai_task = Executor._execute_ai_task

# 定义新的 _execute_ai_task 方法，使用 AWS Q CLI
async def execute_ai_task_with_aws_q(self, prompt: str):
    """使用 AWS Q 模型处理 AI 任务"""
    import asyncio
    import tempfile
    
    if not prompt:
        return None, "No prompt specified"
    
    logger.info("Using AWS Q model for AI task")
    print("Using AWS Q model for AI task", file=sys.stderr)
    
    # 创建临时文件存储提示词
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as f:
        prompt_file = f.name
        f.write(prompt)
    
    try:
        # 调用 AWS Q CLI 生成回答
        process = await asyncio.create_subprocess_exec(
            "q", "generate", "-f", prompt_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        # 清理临时文件
        os.unlink(prompt_file)
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            logger.error(f"AWS Q CLI error: {error_msg}")
            return None, f"AWS Q CLI error: {error_msg}"
        
        return stdout.decode().strip(), None
        
    except Exception as e:
        # 清理临时文件
        if os.path.exists(prompt_file):
            os.unlink(prompt_file)
            
        logger.exception("Error using AWS Q model")
        return None, f"AWS Q model error: {str(e)}"

# 替换 Executor 类的 _execute_ai_task 方法
Executor._execute_ai_task = execute_ai_task_with_aws_q

# 打印确认信息
print("AWS Q 模型补丁已应用 - 已修改 Executor 类以支持 AWS Q 模型", file=sys.stderr)

# 运行原始的 main 函数
if __name__ == "__main__":
    print("启动 MCP Scheduler (使用 AWS Q 模型)...", file=sys.stderr)
    main.main()
