from openai import OpenAI
from logger import logger  # 导入共享的 logger

client = OpenAI()

def load_prompt_template(filepath: str) -> str:
    """
    从文件加载 prompt 模板。
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            logger.info(f"加载了 prompt 模板文件: {filepath}")
            return f.read()
    except FileNotFoundError:
        logger.error(f"Prompt 文件未找到: {filepath}")
        raise
    except Exception as e:
        logger.error(f"加载 Prompt 文件时出错: {e}")
        raise


def generate_sql(query: str, schema_info: str, prompt_path: str) -> str:
    """
    根据自然语言和 schema 信息生成 SQL 查询语句。
    """
    logger.info(f"生成 SQL 查询: 用户输入: {query}")
    prompt_template = load_prompt_template(prompt_path)
    if not prompt_template:
        logger.error("Prompt 模板加载失败")
        return "Error: Prompt 模板加载失败。"

    # 用 schema 和用户的 query 替换占位符
    formatted_prompt = prompt_template.replace("{schema_placeholder}", schema_info).replace("{query_placeholder}", query)
    logger.info(f"生成prompt：{formatted_prompt}")
    try:
        # 调用 OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": formatted_prompt}],
            temperature=0.0
        )

        sql_message = response.choices[0].message
        sql = sql_message.content.strip()  # 获取 content 属性并去掉多余空格
        logger.info(f"生成的 SQL 查询: {sql}")
        return sql
    except Exception as e:
        logger.error(f"生成 SQL 时出错: {e}")
        return f"Error generating SQL: {str(e)}"
