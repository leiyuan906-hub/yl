import time
from DrissionPage import SessionPage, ChromiumPage
import re
import csv

class Zhilian(object):
    def __init__(self, keyword, city='全国'):
        self.keyword = keyword
        self.city = city
        self.url = 'https://www.zhaopin.com/sou/?jl=489&kw=python&p=2'

    def _get_city_code(self):
        """获取城市编码"""
        page = SessionPage()
        page.get('https://fe-api.zhaopin.com/c/i/search/base/data')
        json_data = page.json['data']['allCity']
        for dit in json_data:
            if dit['name'] == self.city:
                return str(dit['code'])
            for city_json in dit['sublist']:
                if city_json['name'] == self.city:
                    return str(city_json['code'])
        return '489'  # 默认值为全国

    def _get_url(self):
        """根据关键词和城市编码生成正确的URL"""
        self.url = re.sub(r'(?<=jl=)[^&]+', self._get_city_code(), self.url)
        self.url = re.sub(r'(?<=kw=)[^&]+', self.keyword, self.url)
        print(self.url)
        return self.url

    def run(self, csv_path):
        """爬取数据并直接写入CSV文件"""
        page = None
        headers = ["position","city","company","salary","experience","education","industry","skills","benefits","search_keyword","links"]
        all_rows = []
        try:
            page = ChromiumPage()
            page.listen.start('/search/positions')
            page.get(self._get_url())
            time.sleep(2)
            for _ in range(1000):  # 翻页处理
                response = page.listen.wait()
                json_data = response.response.body
                jobList = json_data['data']['list']
                for job in jobList:
                    row = [
                        job['name'],
                        job['workCity'],
                        job['companyName'],
                        job['salary60'],
                        job['workingExp'],
                        job['education'],
                        job['industryName'],
                        ', '.join(skill['name'] for skill in job['jobSkillTags']),
                        ', '.join(job['jobKnowledgeWelfareFeatures']),
                        self.keyword,
                        job['positionURL']
                    ]
                    all_rows.append(row)
                next_page_btn = page.ele('css:.soupager a:last-of-type')
                if next_page_btn and 'soupager__btn--disable' in next_page_btn.attr('class'):
                    break
                elif next_page_btn:
                    next_page_btn.click()
                else:
                    print("无法找到下一页按钮，可能页面结构已更改。")
                    break
        except Exception as e:
            print(f"发生错误: {e}")
        finally:
            if page:
                page.quit()
            # 写入CSV
            import os
            file_exists = os.path.exists(csv_path)
            try:
                with open(csv_path, mode="a", encoding="utf-8-sig", newline="") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(headers)
                    writer.writerows(all_rows)
                print(f"数据已成功追加到 {csv_path}")
            except Exception as e:
                print(f"导出CSV时发生错误: {e}")

if __name__ == '__main__':
    city = input('请输入城市名：')
    keyword = input('请输入搜索关键词：')
    if keyword:
        Zhilian_spider = Zhilian(keyword, city=city)
        Zhilian_spider.run('jobs_new.csv')
    else:
        print("关键词和城市名不能为空！")