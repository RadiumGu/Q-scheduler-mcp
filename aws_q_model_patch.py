# aws_q_model_patch.py
# AWS Q 模型集成补丁

import os
import sys
import json
import asyncio
import subprocess
import tempfile
import logging
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置日志记录
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   filename='/home/ec2-user/scheduler-mcp/aws_q_patch.log')
logger = logging.getLogger(__name__)

try:
    # 导入原始的 Executor 类
    from mcp_scheduler.executor import Executor
    
    # 保存原始的 _execute_ai_task 方法
    original_execute_ai_task = Executor._execute_ai_task
    
    # 定义新的 _execute_ai_task 方法，使用 AWS Q CLI
    async def execute_ai_task_with_aws_q(self, prompt: str):
        """使用 AWS Q 模型处理 AI 任务"""
        if not prompt:
            return None, "No prompt specified"
        
        # 检查配置中是否启用了 AWS Q 模型
        config = getattr(self, 'config', {})
        if not isinstance(config, dict):
            config = {}
        
        ai_config = config.get('ai', {})
        use_aws_q = ai_config.get('use_aws_q_model', False)
        
        # 如果启用了 AWS Q 模型，则使用 AWS Q CLI
        if use_aws_q:
            logger.info("Using AWS Q model for AI task")
            
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
        else:
            # 如果未启用 AWS Q 模型，则使用原始的 OpenAI 处理
            return await original_execute_ai_task(self, prompt)
    
    # 替换 Executor 类的 _execute_ai_task 方法
    Executor._execute_ai_task = execute_ai_task_with_aws_q
    
    logger.info("AWS Q 模型补丁已应用 - 已修改 Executor 类以支持 AWS Q 模型")
    print("AWS Q 模型补丁已应用 - 已修改 Executor 类以支持 AWS Q 模型")

except ImportError as e:
    logger.error(f"导入错误: {str(e)}")
    print(f"导入错误: {str(e)}")
    print("请确保已安装所有依赖项: pip install -r requirements.txt")
except Exception as e:
    logger.exception("应用 AWS Q 模型补丁时出错")
    print(f"应用 AWS Q 模型补丁时出错: {str(e)}")
