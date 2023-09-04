import os
os.environ['no_proxy'] = '*' # 避免代理网络产生意外污染

def flip_text(x):
    # return("use flip text")
    return [["1",x[::-1]]]

if __name__ == "__main__":
    import gradio as gr
    # if gr.__version__ not in ['3.28.3']: 
    #     print(gr.__version__)
    #     assert False

    # 记录
    import logging, uuid
    os.makedirs("gpt_log", exist_ok=True)
    try:
        logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO, encoding="utf-8", format="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    except:
        logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO,  format="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    # Disable logging output from the 'httpx' logger
    logging.getLogger("httpx").setLevel(logging.WARNING)
    print("所有问询记录将自动保存在本地目录./gpt_log/chat_secrets.log, 请注意自我隐私保护哦！")

    from utils import get_current_version
    title_html = f"<h1 align=\"center\"> 财报助手 {get_current_version()}</h1>"

    # 配置
    LLM_MODEL = "gpt-3.5-turbo"

    # 做一些外观色彩上的调整
    set_theme = None
    advanced_css = None
    LAYOUT = "TOP-DOWN"
    CHATBOT_HEIGHT = 615

    ###
    gr_L1 = lambda: gr.Row().style()
    gr_L2 = lambda scale, elem_id: gr.Column(scale=scale, elem_id=elem_id)


    with gr.Blocks(title="财报助手", theme=set_theme, analytics_enabled=False, css=advanced_css) as demo:
        gr.HTML(title_html)

        with gr_L1():
            with gr_L2(scale=2, elem_id="gpt-chat"):
                chatbot = gr.Chatbot(label=f"当前模型：{LLM_MODEL}", elem_id="gpt-chatbot")
                # chatbot = gr.Textbox()
            with gr_L2(scale=1, elem_id="gpt-panel"):
                with gr.Accordion("输入区", open=True, elem_id="input-panel") as area_input_primary:
                    with gr.Row():
                        txt = gr.Textbox(show_label=False, placeholder="Input question here.").style(container=False)
                    with gr.Row():
                        submitBtn = gr.Button("提交", variant="primary")
                    with gr.Row():
                        status = gr.Markdown(f"Tip: 按Enter提交, 按Shift+Enter换行。当前模型: {LLM_MODEL} \n ", elem_id="state-panel")

        submitBtn.click(fn=flip_text, inputs=txt, outputs=chatbot)

    # demo.launch(server_port=5000, server_name='0.0.0.0', debug=True)
    demo.launch(server_port=5000, debug=True)
