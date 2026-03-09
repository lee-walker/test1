import json
import sys
import re

def clean_text(text):
    """清理可能破坏 Markdown 链接语法的字符"""
    if not text:
        return ""
    # 去除方括号和圆括号，防止嵌套导致解析失败
    return re.sub(r'[\[\]\(\)]', '', str(text)).strip()

def format_summary(json_data):
    try:
        # 预处理：剔除可能存在的 Markdown 代码块标记
        json_data = json_data.strip()
        if json_data.startswith("```"):
            lines = json_data.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            json_data = "\n".join(lines).strip()
            
        # 解析 JSON
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            match = re.search(r'\[\s*\{.*\}\s*\]', json_data, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
            else:
                raise

        output = []
        # 按类别分组
        categories = {}
        for item in data:
            cat = clean_text(item.get('category', '精选新闻'))
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
            
        for cat, items in categories.items():
            output.append(f"【{cat}】") # 使用更稳定的中文书名号作为标题
            for item in items:
                title = clean_text(item.get('title', '无题'))
                link_url = item.get('link', '').strip()
                summary = item.get('summary', '').strip()
                
                # 严格执行参考格式: [{title}]({link_url})
                if link_url and link_url.startswith('http'):
                    formatted_title = f"[{title}]({link_url})"
                else:
                    formatted_title = title
                
                line = formatted_title
                if summary:
                    line += f"：{summary}"
                output.append(f"· {line}") # 使用简单的圆点作为列表符
            output.append("") # 类别间空行
            
        return "\n".join(output).strip()
    except Exception as e:
        return f"格式化失败: {str(e)}\n原始输出: {json_data[:100]}"

if __name__ == "__main__":
    content = sys.stdin.read()
    if content:
        print(format_summary(content))
