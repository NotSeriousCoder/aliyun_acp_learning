import os, sys
from pathlib import Path
from openai import OpenAI
_client = None        # 先放个空位，真正用时再创建（懒加载）

DEFAULT_SYSTEM_PROMPT = "你负责教育内容开发公司的答疑，你的名字叫公司小蜜，你要回答同事们的问题。"
DEFAULT_MODEL = "qwen3.5-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.8

def _get_client():
    global _client
    if _client is None:
        if not os.getenv("DASHSCOPE_API_KEY"):   # 没设置 Key 就自动兜底
            init_api_key()
        _client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                         base_url="https://llm-edn13vvg67wwlb8j.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
    return _client



def chat(prompt, system_prompt=DEFAULT_SYSTEM_PROMPT, model=DEFAULT_MODEL):
    client = _get_client()
    response = client.chat.completions.create(model=model, messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ])
    return response.choices[0].message.content




def init_api_key():
    print(os.getcwd())
    # 从当前目录(course_core/utils)向上逐级找，直到找到含 config/load_key.py 的 course_core
    current = Path.cwd()
    current.absolute = "/mnt/workspace/acp_learning_myself/aliyun_acp_learning/大模型ACP认证教程/course_core"
    while not (current / "config" / "load_key.py").exists():
        if current == current.parent:
            raise FileNotFoundError("向上找不到 course_core（缺少 config/load_key.py）")
        current = current.parent


    os.chdir(current)
    sys.path.insert(0, str(current))
    print(f"已切换到课程公共模块目录：{current}")

    from config.load_key import load_key
    load_key()
    print(f'''你配置的 API Key 是：{os.environ["DASHSCOPE_API_KEY"][:5]+"*"*5}''')