import gradio as gr
import os
import json
from PIL import Image
from evaluator.task_trace import DatasetHelper

DATASET_PATH = (
    "/data/yyh/mobile/leaderboard/LlamaTouch/dataset/llamatouch_dataset_0521/"
)
helper = DatasetHelper(
    epi_metadata_path="/data/yyh/mobile/leaderboard/LlamaTouch/dataset/llamatouch_dataset_0521/",
    gr_dataset_path="./",
)

def get_datasets():
    """获取可用数据集的名称"""
    return os.listdir(DATASET_PATH)


def get_traces(dataset_name):
    """获取指定数据集的子文件夹"""
    dataset_dir = os.path.join(DATASET_PATH, dataset_name)
    if os.path.exists(dataset_dir):
        traces = [f for f in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, f))]
        traces = sorted(traces, key=lambda x: int(x.split("_")[1]))
        return traces
    return []


def get_img_by_path(img_path):
    """根据路径加载图片"""
    if os.path.exists(img_path):
        return Image.open(img_path)
    return None


def load_element(trace_dir):
    """加载指定数据集和子文件夹的元素"""
    if not os.path.exists(trace_dir):
        return None, None, "trace not found"

    img_path = os.path.join(trace_dir, "agg_plot.png")

    # 加载图片
    if os.path.exists(img_path):
        img = Image.open(img_path) 
    else:
        # plot_any_agg(DATASET_PATH,dataset_name,trace_name,trace_dir)
        img = None

    return img


def update_trace_and_display(dataset_name,trace_name):
    """更新子文件夹下拉列表和显示内容"""
    traces = get_traces(dataset_name)

    if not traces:
        return gr.Dropdown(choices=[]), None

    # 默认选择第一个子文件夹并加载其内容
    first_trace = traces[0]
    trace_dir = os.path.join(DATASET_PATH, dataset_name, first_trace)
    img= load_element(trace_dir)

    return (
        gr.Dropdown(choices=traces, value=first_trace),
        img
    )


def display_element(dataset_name, trace_name):
    """根据选择的子文件夹显示元素内容"""
    if trace_name:
        trace_dir = os.path.join(DATASET_PATH, dataset_name, trace_name)
        img = load_element(trace_dir)
        trace = helper._load_groundtruth_trace_by_path(trace_dir)
        idx = list(range(len(trace)))
        return (
            img,
            gr.Dropdown(choices=idx),
            gr.Button(
                value="(Not implemented yet) Submit your feedback if you beileve this trace's essential states are mislabeled",
                visible=True,
            ),
        )
    return None, None, None


def get_state_details(dataset_name, trace_name, idx):
    trace_dir = os.path.join(DATASET_PATH, dataset_name, trace_name)
    trace = helper._load_groundtruth_trace_by_path(trace_dir)
    trace[int(idx)].vh_simp_ui_json_path
    with open (trace[int(idx)].vh_simp_ui_json_path) as f:
        all_info = json.load(f)
        
    
    return gr.Image(get_img_by_path(trace[int(idx)].screenshot_path.replace(".png","_drawed.png")),visible=True), gr.Dropdown(choices=list(range(len(all_info))),visible=True,value=0), gr.Textbox(json.dumps(all_info[0],indent=4),visible=True)


def get_elem_details(dataset_name, trace_name, idx, elem_idx):
    # TODO 机制没搞清楚于是在这复制代码，可以找个方式优化掉
    trace_dir = os.path.join(DATASET_PATH, dataset_name, trace_name)
    trace = helper._load_groundtruth_trace_by_path(trace_dir)
    trace[int(idx)].vh_simp_ui_json_path
    with open(trace[int(idx)].vh_simp_ui_json_path) as f:
        all_info = json.load(f)
    
    return gr.Textbox(json.dumps(all_info[int(elem_idx)],indent=4),visible=True)

# 定义Gradio的UI
dataset_list = get_datasets()

# with gr.Blocks() as demo:
#     dataset_dropdown = gr.Dropdown(label="Select Dataset", choices=dataset_list)
#     trace_dropdown = gr.Dropdown(label="Select Trace", allow_custom_value=True)
#     # sys_info = gr.Textbox(label="System Info")

#     # with gr.Row():  # 使用 Row 布局将图片和文字并排显示
#     #     output_image = gr.Image(label="Image Viewer")
#     #     output_text = gr.Textbox(label="Text Viewer")
#     output_image = gr.Image(label="Image Viewer")
#     submit = gr.Button(
#         value="(Not implemented yet) Submit your feedback if you beileve this trace's essential states are mislabeled",
#         visible=False
#     )
#     detailed_trace = gr.Dropdown(label="Select an UIState to view its details", allow_custom_value=True)

#     with gr.Row() :  # 使用 Row 布局将图片和文字并排显示
#         state_image = gr.Image(label="Image for this state", visible=False)
#         with gr.Column():
#             state_elem = gr.Dropdown(label="All the UI Elements", allow_custom_value=True, visible=False, value=0)
#             state_text = gr.Textbox(label="Details for the selected UI Element",visible=False)

#     # 当选择数据集时，更新子文件夹选项并显示默认的第一个子文件夹内容
#     dataset_dropdown.change(
#         fn=update_trace_and_display,
#         inputs=[dataset_dropdown, trace_dropdown],
#         outputs=[
#             trace_dropdown,  # 设置choices
#             output_image,
#             # output_text,
#             # sys_info,  # 输出错误消息
#         ],
#     )

#     # 当选择子文件夹时，显示对应的图片和文本
#     trace_dropdown.change(
#         fn=display_element,
#         inputs=[dataset_dropdown, trace_dropdown],
#         # outputs=[output_image, output_text, sys_info],
#         outputs=[output_image, detailed_trace, submit],
#     )

#     detailed_trace.change(
#         fn=get_state_details,
#         inputs=[dataset_dropdown, trace_dropdown, detailed_trace],
#         outputs=[state_image,state_elem, state_text],
#     )
#     state_elem.change(
#         fn=get_elem_details,
#         inputs=[dataset_dropdown, trace_dropdown, detailed_trace, state_elem],
#         outputs=[state_text],
#     )


# demo.launch()
