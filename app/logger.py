import logging

def setup_logger():
    """
    配置日志记录
    """
    logger = logging.getLogger("MySQLChat")
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别为 DEBUG

    # 创建日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 控制台日志级别为 INFO
    console_handler.setFormatter(formatter)

    # 文件日志处理器
    file_handler = logging.FileHandler("mysql_chat.log")
    file_handler.setLevel(logging.DEBUG)  # 文件日志级别为 DEBUG
    file_handler.setFormatter(formatter)

    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# 创建并暴露日志实例
logger = setup_logger()
