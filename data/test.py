import pandas as pd
from DrissionPage import ChromiumPage
import time
import random

# 可选：自定义User-Agent池
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
]

csv_path = 'jobs_new.csv'
df = pd.read_csv(csv_path)
sample_df = df.copy()
recruit_nums = []

for url in sample_df['links']:
    retry = 3
    while retry > 0:
        try:
            # 随机User-Agent
            ua = random.choice(USER_AGENTS)
            page = ChromiumPage()
            # 设置User-Agent
            page.set.headers({'User-Agent': ua})
            page.get(url)
            # 随机延迟2-5秒
            time.sleep(random.uniform(2, 3))
            recruit_li = page.ele('xpath://ul[@class="summary-plane__info"]/li[contains(text(), "招")]')
            recruit_info = recruit_li.text.strip() if recruit_li else ''
            recruit_nums.append(recruit_info)
            page.quit()
            break
        except Exception as e:
            retry -= 1
            if retry == 0:
                recruit_nums.append('')
            try:
                page.quit()
            except:
                pass
            # 失败时随机延迟再重试
            time.sleep(random.uniform(1, 3))

sample_df['numbers'] = recruit_nums
sample_df.to_csv('jobs_new_sample.csv', mode="a",index=True, encoding='utf-8-sig')
print('招聘人数已补全并写入jobs_new_sample.csv')

