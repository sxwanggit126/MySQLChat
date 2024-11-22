# MySQL Chat

MySQL Chat 是一个基于自然语言生成 SQL 查询的 AI 工具，旨在帮助数据分析师通过简单的对话完成数据库操作。项目以 Python 开发，支持动态数据库 Schema 加载和数据查询。

---

## Features

- **自然语言转 SQL：** 输入自然语言查询描述，快速生成 SQL 查询。
- **动态 Schema 加载：** 自动读取并解析数据库结构，无需手动输入。
- **SQL 执行和结果返回：** 直接运行生成的 SQL 并返回结果。
- **模块化设计：** 独立的数据库连接、SQL 生成和日志模块，易于扩展。
- **日志功能：** 统一日志输出，支持调试和问题排查。

---

## Installation

### 克隆项目
```bash
git clone https://github.com/sxwanggit126/MySQLChat.git
cd MySQLChat
```
## 创建 Conda 虚拟环境并安装依赖
### 创建虚拟环境：

```bash
conda create -n mysql_chat python=3.9 -y 
```
### 激活虚拟环境：

``` bash
conda activate mysql_chat
```
### 安装依赖：

``` bash
pip install -r requirements.txt
```
## Configuration
### 配置文件路径
项目使用 config.json 进行配置，文件内容如下：

```json
{
  "mysql_url": "mysql://username:password@localhost:3306/database_name",
  "prompt_path": "path/to/prompt_template.txt"
}
``` 
### 配置说明
mysql_url： 目标数据库的连接 URL，支持 MySQL。
prompt_path： 存放 Prompt 模板的文件路径，用于自然语言转 SQL。

### 启动程序
```bash
python app/main.py
```
```bash
示例流程
输入自然语言查询描述：

复制代码
查询 dim_area 表中每个地区的城市数量。
生成 SQL 查询：

sql：
SELECT area AS area_alias, COUNT(DISTINCT city) AS city_count_alias
FROM dim_area
GROUP BY area;
执行查询并返回结果：
[
  { "area_alias": "北方地区", "city_count_alias": 15 }
]
```

### Project Structure
```bash
MySQLChat/
├── app/
│   ├── main.py              # 主程序入口
│   ├── services/            # 核心服务模块
│   │   ├── db_query.py      # 数据库连接与查询模块
│   │   ├── sql_generator.py # 自然语言转 SQL 模块
├── config.json              # 配置文件
├── logs/                    # 日志输出目录
├── prompt_template.txt      # Prompt 模板
├── requirements.txt         # 项目依赖
└── README.md                # 项目说明
```

## License
本项目基于 MIT 许可证发布，详情请参阅 LICENSE 文件。

## Contributing
欢迎提交 Issue 和 Pull Request 来改进本项目！如有任何问题，请联系项目作者。


