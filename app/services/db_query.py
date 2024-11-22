import pymysql
from logger import logger  # 导入共享的 logger

def connect_to_database(mysql_url: str):
    """
    根据 MySQL URL 连接到数据库。
    """
    try:
        # 从 MySQL URL 解析连接参数
        connection_params = parse_mysql_url(mysql_url)
        connection = pymysql.connect(
            host=connection_params["host"],
            user=connection_params["user"],
            password=connection_params["password"],
            database=connection_params["database"],
            port=connection_params["port"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        logger.info("数据库连接成功！")
        return connection
    except pymysql.Error as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return None


def parse_mysql_url(mysql_url: str) -> dict:
    """
    解析 MySQL URL 并返回连接参数。
    """
    from urllib.parse import urlparse
    url = urlparse(mysql_url)
    return {
        "host": url.hostname,
        "port": url.port or 3306,
        "user": url.username,
        "password": url.password,
        "database": url.path.lstrip("/")
    }


def execute_query(connection, sql: str):
    """
    执行 SQL 查询并返回结果。
    """
    try:
        with connection.cursor() as cursor:
            # 确保 SQL 是字符串并清理多余空白字符
            if not isinstance(sql, str):
                raise ValueError("SQL 查询必须是字符串")
            sql = sql.strip()  # 去掉首尾空白字符
            logger.info(f"执行 SQL 查询: {sql}")

            # 执行 SQL
            cursor.execute(sql)

            # 如果是 SELECT 查询，返回结果
            if sql.lower().startswith("select"):
                result = cursor.fetchall()
                logger.debug(f"查询结果: {result}")
                return result

            # 对于非 SELECT 查询，提交事务
            connection.commit()
            return "Query executed successfully."
    except pymysql.Error as e:
        logger.error(f"查询执行失败: {str(e)}")
        return f"Query execution error: {str(e)}"
    except Exception as e:
        logger.error(f"发生未处理的错误: {str(e)}")
        return f"Unexpected error: {str(e)}"


def load_schema(connection) -> str:
    """
    加载数据库的 schema 信息。
    """
    try:
        schema = []
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            for table in tables:
                table_name = list(table.values())[0]  # 获取表名
                schema.append(f"Table: {table_name}")
                cursor.execute(f"DESCRIBE {table_name};")
                columns = cursor.fetchall()
                for column in columns:
                    schema.append(f"  - {column['Field']} ({column['Type']})")
        logger.info(f"成功加载 schema 信息：{schema}")
        return "\n".join(schema)
    except pymysql.Error as e:
        logger.error(f"加载 schema 信息失败: {str(e)}")
        return ""


def load_schema_with_data_preview(connection) -> str:
    """
    加载数据库的 schema 信息，并附加每个表的前 3 条数据预览。
    :param connection: 数据库连接对象
    :return: 包含 schema 和数据预览的字符串表示
    """
    try:
        schema_with_preview = []
        with connection.cursor() as cursor:
            logger.info("开始加载数据库 schema 信息...")

            # 获取所有表名
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            logger.info(f"发现 {len(tables)} 个表。")

            for table in tables:
                table_name = list(table.values())[0]  # 获取表名
                logger.info(f"加载表结构: {table_name}")
                schema_with_preview.append(f"Table: {table_name}")

                # 获取表结构
                try:
                    cursor.execute(f"DESCRIBE {table_name};")
                    columns = cursor.fetchall()
                    for column in columns:
                        schema_with_preview.append(f"  - {column['Field']} ({column['Type']})")
                    logger.info(f"成功加载表 {table_name} 的结构。")
                except pymysql.Error as e:
                    logger.error(f"加载表 {table_name} 的结构失败: {str(e)}")
                    schema_with_preview.append(f"  Error loading table structure: {str(e)}")
                    continue

                # 获取前 3 条数据
                try:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                    rows = cursor.fetchall()
                    if rows:
                        schema_with_preview.append("  Sample Data:")
                        for row in rows:
                            schema_with_preview.append(f"    - {row}")
                            logger.info(f"表 {table_name} 的数据: {row}")  # 在日志中记录具体行数据
                        logger.info(f"成功加载表 {table_name} 的前 3 条数据。")
                    else:
                        schema_with_preview.append("  No data available in this table.")
                        logger.info(f"表 {table_name} 中没有数据。")
                except pymysql.Error as e:
                    logger.error(f"加载表 {table_name} 的数据失败: {str(e)}")
                    schema_with_preview.append(f"  Error loading data: {str(e)}")
                    continue

        logger.info("成功加载所有表的 schema 信息和数据预览。")
        return "\n".join(schema_with_preview)
    except pymysql.Error as e:
        logger.error(f"加载 schema 信息失败: {str(e)}")
        return ""