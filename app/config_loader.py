import json
import os

class ConfigLoader:
    """
    加载并管理配置文件。
    """
    CONFIG_PATH = "../config.json"

    @staticmethod
    def load_config():
        """
        加载 config.json 文件内容。
        """
        try:
            with open(ConfigLoader.CONFIG_PATH, "r") as f:
                config = json.load(f)

            # 验证必要字段
            if "mysql_url" not in config or "prompt_path" not in config:
                raise ValueError("配置文件中缺少必要字段 (mysql_url 或 prompt_path)。")

            # 验证 prompt 文件路径是否存在
            if not os.path.exists(config["prompt_path"]):
                raise FileNotFoundError(f"Prompt 文件路径无效: {config['prompt_path']}")

            return config
        except FileNotFoundError:
            print("配置文件 config.json 未找到，请检查或创建配置文件。")
            raise
        except json.JSONDecodeError:
            print("配置文件格式错误，请检查 config.json。")
            raise
        except Exception as e:
            print(f"加载配置文件时出错: {e}")
            raise
