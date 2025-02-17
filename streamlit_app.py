"""  
@author: VL
@time: 2025/2/17 19:01  
@file: streamlit_app.py  
@project: VL_deepseek_r1  
@description: 这里是文件的描述信息  
"""

from openai import OpenAI
import streamlit as st
import toml
# 读取 config.toml 文件
with open("config.toml", "r") as f:
    config = toml.load(f)

# 从 config 中获取 API_KEY 和 BASE_URL
key = config["openai"]["api_key"]
url = config["openai"]["base_url"]


client = OpenAI(
    api_key=key,
    base_url=url
)


def get_response(prompt):
    response = client.chat.completions.create(
        model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )
    return response.choices[0].message.content


def get_re_history(messages):
    response = client.chat.completions.create(
        model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=messages
    )
    return response


def main():
    st.set_page_config(
        page_title="DeepSeek对话平台",
        page_icon="🚀",
    )
    st.title("DeepSeek-R1-671B")
    # 在title下边小标题，写上版本 0.01
    st.sidebar.markdown("###  小bug待解决：第一次对话的思考内容无法获取,第二轮及以后正常   ###")
    # st.sidebar.header("API 配置")
    # api_key = st.sidebar.text_input("API Key", type="password")
    model_name = st.sidebar.selectbox("模型选择", ["deepseek-R1"])
    # openai.api_key = api_key
    # openai.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    # 用于跟踪对话历史
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    messagesout = st.container(height=500)
    history = []
    if prompt := st.chat_input("请输入你的问题"):
        # 将用户输入添加到对话历史中
        st.session_state.messages.append({"role": "user", "content": prompt})

        # print(st.session_state.messages)

        # 调用 respond 函数获取回答
        answer = get_re_history(st.session_state.messages)

        # 检查回答是否为 None
        if answer is not None:
            answer_content = answer.choices[0].message.content
            reasoning_content = answer.choices[0].message.reasoning_content
            print(answer_content)
            print(reasoning_content)

            # 将LLM的回答添加到对话历史中
            st.session_state.messages.append({"role": "assistant", "content": answer_content})

        messagesout.empty()
        with messagesout:
            # 遍历对话历史，将每个消息显示在聊天窗口中,将对话中的
            for message in st.session_state.messages[:-2]:
                if message["role"] == "user":
                    st.chat_message("user").write(message["content"])
                elif message["role"] == "assistant":
                    st.chat_message("assistant").write(message["content"])
            st.chat_message("user").write(st.session_state.messages[-2]["content"])
            st.write("\n" + "=" * 30 + "思考过程" + "=" * 30 + "\n")
            st.chat_message("assistant").write(reasoning_content)
            st.write("\n" + "=" * 30 + "最终答案" + "=" * 30 + "\n")
            st.chat_message("assistant").write(answer_content)

        print(len(st.session_state.messages))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"发生错误：{e}")
