import matplotlib.pyplot as plt
import io
import base64
import json

def generate_chart(data: str, chart_type: str) -> str:
    """
    根据数据生成图表，并返回图表的 Base64 URL。
    """
    data = json.loads(data)
    x = [item["x"] for item in data]
    y = [item["y"] for item in data]
    
    plt.figure()
    if chart_type == "bar":
        plt.bar(x, y)
    elif chart_type == "line":
        plt.plot(x, y)
    else:
        return "不支持的图表类型"

    # 转换为 Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    return f"data:image/png;base64,{img_str}"
