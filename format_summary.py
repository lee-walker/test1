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
        # 1. 尝试直接解析
        data = None
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            # 2. 如果直接解析失败，寻找 JSON 数组 [...]
            match = re.search(r'\[\s*\{.*\}\s*\]', json_data, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
            else:
                # 3. 寻找 Markdown 代码块内的 JSON
                match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', json_data, re.DOTALL)
                if match:
                    data = json.loads(match.group(1))
        
        if not data:
            return "未能从 Gemini 返回的内容中提取有效的 JSON 数据。"

        output = []
        # 按类别分组
        categories = {}
        for item in data:
            cat = clean_text(item.get('category', '精选新闻'))
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
            
        for cat, items in categories.items():
            output.append(f"【{cat}】") 
            for item in items:
                title = clean_text(item.get('title', '无题'))
                link_url = item.get('link', '').strip()
                summary = item.get('summary', '').strip()
                
                if link_url and link_url.startswith('http'):
                    formatted_title = f"[{title}]({link_url})"
                else:
                    formatted_title = title
                
                line = formatted_title
                if summary:
                    line += f"：{summary}"
                output.append(f"· {line}") 
            output.append("") # 类别间空行
            
        return "\n".join(output).strip()
    except Exception as e:
        return f"格式化失败: {str(e)}\n原始输出片段: {json_data[:150]}"

if __name__ == "__main__":
    content = ""
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"读取文件失败: {str(e)}")
            sys.exit(1)
    else:
        content = sys.stdin.read()
    
    if content:
        result = format_summary(content)
        if result:
            print(result)
        else:
            print("错误: 格式化结果为空")
    else:
        print("错误: 没有接收到输入内容")
        sys.exit(1)
