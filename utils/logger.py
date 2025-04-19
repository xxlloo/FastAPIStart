import sys
from pathlib import Path

from loguru import logger


def setup_logger():
    BASE_DIR = Path(__file__).resolve().parent.parent  # 指向项目根目录
    log_path = BASE_DIR / "logs"
    log_path.mkdir(parents=True, exist_ok=True)

    # 移除默认配置
    logger.remove()

    # 控制台输出
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="<green>[{time:YYYY-MM-DD HH:mm:ss.SSS}]</green> "
        "<level>[{level}]</level> "
        "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
    )

    # 文件记录
    logger.add(
        log_path / "app.log",
        rotation="00:00",
        retention="7 days",
        compression="zip",
        encoding="utf-8",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )


_logger_initialized = False


def initialize_logger():
    global _logger_initialized
    if not _logger_initialized:
        try:
            logger.add(lambda msg: None, format="", level="TRACE")
            logger.remove()
            _logger_initialized = True
            setup_logger()
        except ValueError:
            _logger_initialized = True
            setup_logger()


initialize_logger()

__all__ = ["logger"]


if __name__ == "__main__":
    logger.debug("调试信息")
    logger.info("普通信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.success("成功信息")

    try:
        1 / 0
    except Exception as e:
        logger.exception(f"异常来了 {e}")
