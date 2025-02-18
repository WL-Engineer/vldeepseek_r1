# deepseek_r1
### deepseek_r1  api调用web版本





配置并部署在streamlit中

1. 将本仓库放置于streamlit的app仓库中，网址：https://share.streamlit.io/
2. 修改app入口为streamlit_app.py
3. 在配置文件中填写程序的deepseek_R1模型`url`和在相应平台上获取的deepseek_R1模型`api_key`
4. 配置文件格式如下
```shell
[openai]
api_key = "xxxxx"
base_url = "https:"
```
5. 运行即可；





### 构建自助知识库

（一）架构设计

1. 分层架构：
   - 数据预处理层
   - 向量服务层
   - 检索增强层
   - 大模型交互层
2. 核心组件交互流程： 文档 → 分块 → 向量化 → 向量存储 → 用户提问 → 向量检索 → 上下文构造 → R1生成
