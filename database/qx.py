import pandas as pd
import numpy as np
import re
from sqlalchemy import create_engine

# 正则表达式匹配核心结构
def parse_salary(salary_str):
    salary_str = salary_str.strip().replace(' ', '').replace('·', '')
    match = re.match(
        r"""
        ^
        ([\d.]+)                # 最小值
        \s*[~～至—-]\s*        # 支持多种分隔符
        ([\d.]+)                # 最大值
        \s*?
        (万|千|k|K|w|W|元|元/月)?\s*?
        (?:/\s*?(天|月|年)\s*?)?
        (?:·?\s*?(\d+)\s*薪)?
        $
        """,
        salary_str,
        re.VERBOSE
    )
    if not match:
        return None

    min_val, max_val, unit, period, bonus_months = match.groups()

    def convert_unit(value, unit):
        unit_map = {
            "万": 10000, "w": 10000, "W": 10000,
            "千": 1000, "k": 1000, "K": 1000,
            "元": 1
        }
        return float(value) * unit_map.get(unit, 1)

    try:
        min_salary = convert_unit(min_val, unit)
        max_salary = convert_unit(max_val, unit)
    except ValueError:
        return None

    if period == '天':
        min_salary *= 22
        max_salary *= 22
    elif period == '年':
        min_salary /= 12
        max_salary /= 12

    return {
        "min_salary": int(min_salary),
        "max_salary": int(max_salary),
    }

# 封装分组聚合函数
def group_and_aggregate(data, group_col):
    return data.groupby(group_col).agg(
        avg_salary=('avg_salary', 'mean'),
        count=(group_col, 'count')
    ).reset_index()

# 异常值检测函数
def detect_outliers(data, group_cols):
    data['is_outlier'] = False
    for group_col in group_cols:
        for group in data[group_col].unique():
            group_data = data[data[group_col] == group]
            if len(group_data) > 0:
                # 检测avg_salary异常
                q1_salary = group_data['avg_salary'].quantile(0.25)
                q3_salary = group_data['avg_salary'].quantile(0.75)
                iqr_salary = q3_salary - q1_salary
                lower_salary = q1_salary - 2.0 * iqr_salary
                upper_salary = q3_salary + 2.0 * iqr_salary

                # 检测numbers异常
                q1_num = group_data['numbers'].quantile(0.25)
                q3_num = group_data['numbers'].quantile(0.75)
                iqr_num = q3_num - q1_num
                lower_num = q1_num - 1.5 * iqr_num
                upper_num = q3_num + 1.5 * iqr_num

                mask = data[group_col] == group
                data.loc[mask, 'is_outlier'] |= (
                    (data.loc[mask, 'avg_salary'] < lower_salary) |
                    (data.loc[mask, 'avg_salary'] > upper_salary) |
                    (data.loc[mask, 'min_salary'] > data.loc[mask, 'max_salary']) |
                    (data.loc[mask, 'numbers'] < lower_num) |
                    (data.loc[mask, 'numbers'] > upper_num)
                )
    return data[~data['is_outlier']].drop('is_outlier', axis=1)

# 优化后的去重函数
def remove_duplicates(data, subset, keep='first', sort_columns=None):
    if sort_columns:
        data = data.sort_values(by=sort_columns)
    return data.drop_duplicates(subset=subset, keep=keep)

if __name__ == "__main__":
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/zhaopin?charset=utf8mb4')
    data = pd.read_csv('jobs_new_sample.csv', encoding='gbk')
    # 提取numbers列中的数字并转为整数
    if 'numbers' in data.columns:
        data['numbers'] = data['numbers'].astype(str).str.extract(r'(\d+)').astype(float).astype('Int64')
    data2 = data[(data['salary'] != '面议') & (data['numbers'].notna()) & (~data['salary'].str.contains('/天'))] 

    salary_data = data2['salary'].apply(lambda x: pd.Series(parse_salary(x)))
    data3 = pd.concat([
        data2.reset_index(drop=True),
        salary_data.reset_index(drop=True)
    ], axis=1)

    # 缺失值填充
    data3['min_salary'] = data3['min_salary'].fillna(data3.groupby(['city', 'education'])['min_salary'].transform('median'))
    data3['max_salary'] = data3['max_salary'].fillna(data3.groupby(['city', 'education'])['max_salary'].transform('median'))
    data3 = data3.dropna(subset=['min_salary', 'max_salary'])

    # 计算平均薪资
    data3['avg_salary'] = (data3['min_salary'] + data3['max_salary']) / 2

    # 异常值检测
    data3 = detect_outliers(data3, ['city', 'search_keyword', 'education'])
    # 使用数据库自增主键
    data3 = data3.reset_index(drop=True)

    # 数据去重
    data3 = remove_duplicates(data3, subset=['position', 'company', 'salary','city'], sort_columns=None)

    # 数据质量评估
    print('\n=== 数据质量评估报告 ===')
    original_count = len(data)
    cleaned_count = len(data3)
    missing_ratio = (original_count - cleaned_count) / original_count
    print(f'原始数据记录数: {original_count}')
    print(f'清洗后记录数: {cleaned_count}')
    print(f'因缺失值/无效值删除比例: {missing_ratio:.2%}')

    total_outliers = len(data2) - len(data3)
    num_outliers = len(data3[data3['numbers'] < 0])
    print(f'总异常值删除记录数: {total_outliers}')

    print('\n薪资分布统计:')
    print(data3[['min_salary', 'max_salary', 'avg_salary']].describe())

    print('\n城市分布统计:')
    print(data3['city'].value_counts().head(10))

    print('\n教育背景分布:')
    print(data3['education'].value_counts())

    # try:
    #     # 将数据写入MySQL数据库
    #     data3.to_sql('jobs_new', engine, if_exists='replace', index=False)
    #     print('数据已成功保存到MySQL数据库')

    #     # 保存统计数据到相应的表
    #     tables = {
    #         'education_salary': 'education',
    #         'city_salary': 'city',
    #         'industry_salary': 'industry',
    #         'major_salary': 'search_keyword'
    #     }

    #     for table_name, group_col in tables.items():
    #         stats = group_and_aggregate(data3, group_col)
    #         stats.to_sql(table_name, engine, if_exists='replace', index=False)

    #     # 各个区域的招聘岗位数量统计
    #     city_job_count = data3['city'].value_counts().reset_index()
    #     city_job_count.columns = ['city', 'job_count']
    #     city_job_count.to_sql('city_job_count', engine, if_exists='replace', index=False)

    #     print('所有统计数据已成功保存到MySQL数据库')
    # except Exception as e:
    #     print(f'保存数据到MySQL时出错：{str(e)}')
    # finally:
    #     engine.dispose()