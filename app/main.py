import os
import json
from services.db_query import connect_to_database, load_schema_with_data_preview, execute_query
from services.sql_generator import generate_sql
from logger import logger  # 导入共享的 logger

# 加载配置文件
def load_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        logger.info(f"加载配置文件: {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"配置文件未找到: {config_path}")
        raise
    except Exception as e:
        logger.error(f"加载配置文件时出错: {e}")
        raise

def main():
    logger.info("欢迎使用 MySQL Chat！")

    # 加载配置
    config_path = os.path.join(os.getcwd(), "../config.json")
    config = load_config(config_path)
    mysql_url = config.get("mysql_url")
    prompt_path = config.get("prompt_path")

    # 连接数据库
    connection = connect_to_database(mysql_url)
    if not connection:
        logger.error("无法连接到数据库，请检查配置文件中的 mysql_url 设置。")
        return

    # 加载 schema 信息（包括数据预览）
    schema_info = load_schema_with_data_preview(connection)
    if not schema_info:
        logger.error("无法加载 schema 信息，请检查数据库连接或表结构。")
        return

    logger.info("数据库连接成功！已加载 schema 信息。")
    logger.debug(f"Schema 信息: {schema_info}")

    while True:
        print("\n请选择操作：")
        print("1. 输入自然语言查询描述，生成 SQL 并查询数据")
        print("2. 生成数据可视化图表")
        print("3. 退出")
        choice = input("请输入操作编号: ")

        if choice == "1":
            query = input("请输入自然语言查询描述: ")
            logger.info(f"用户输入的查询描述: {query}")
            sql = generate_sql(query, schema_info, prompt_path)
            logger.info(f"生成的 SQL 查询: {sql}")

            # 执行 SQL 查询
            result = execute_query(connection, sql)
            logger.debug(f"查询结果: {result}")
            print("\n查询结果:")
            print(result)

        elif choice == "2":
            print("生成数据可视化图表功能待开发。")
        elif choice == "3":
            logger.info("感谢使用 MySQL Chat，再见！")
            break
        else:
            logger.warning("无效的操作编号，请重新输入。")

if __name__ == "__main__":
    main()
