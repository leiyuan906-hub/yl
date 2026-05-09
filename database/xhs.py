from DrissionPage import ChromiumPage
import pandas as pd

# 初始化浏览器对象
dp = ChromiumPage()
# 开始监听特定的API接口，用于获取笔记数据
dp.listen.start('web_api/sns/v5/creator/note')
# 访问小红书创作者中心的笔记管理页面
dp.get('https://creator.xiaohongshu.com/new/note-manager')

# 等待并获取监听到的响应数据
r = dp.listen.wait()
# 获取响应体的JSON数据
json_data  = r.response.body
# print(json_data)

# 从JSON结构中提取笔记列表数据
items = json_data['data']['notes']
# print(items)

notes_data = []

def parse_html(items):
    """
    解析笔记数据列表
    Args:
        items: 原始的笔记数据列表
    Returns:
        list: 包含提取关键信息后的笔记列表
    """
    notes_data = []
    for item in items:
        # 提取每个笔记的关键指标
        info = {
            "标题": item.get("display_title", ""),
            "发布时间": item.get("time", ""),
            "播放量": item.get("view_count", 0),
            "评论量": item.get("comments_count", 0),
            "点赞量": item.get("likes", 0),
            "收藏量": item.get("collected_count", 0),
            "转发量": item.get("shared_count", 0)
        }
        notes_data.append(info)
    return notes_data

def save_to_excel(data, file_path="小红书笔记数据.xlsx"):
    """
    将数据保存为Excel文件
    Args:
        data: 要保存的数据列表
        file_path: 目标Excel文件路径
    """
    if not data:
        print("没有数据可保存")
        return
    
    try:
        # 使用pandas将数据转换为DataFrame并导出为Excel
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, sheet_name="笔记数据")
        print(f"数据已成功保存到 {file_path}")
    except Exception as e:
        print(f"保存Excel文件时出错: {e}")

if __name__ == "__main__":
    # 解析获取到的笔记数据
    notes_data = parse_html(items)
    # 保存数据到Excel文件
    save_to_excel(notes_data)
    
    
