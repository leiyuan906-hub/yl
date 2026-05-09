from backend.utils.data_processor import JobDataProcessor

def test_job_data_processor():
    # 创建JobDataProcessor实例
    processor = JobDataProcessor('jobs.csv')

    # 测试数据加载
    assert processor.load_data() == True

    # 测试数据清洗
    assert processor.clean_data() == True

    # 测试薪资范围分析
    salary_range = processor.get_salary_range()
    assert salary_range is not None
    print("\n薪资范围分析示例：")
    print(salary_range.head())

    # 测试城市分布
    city_dist = processor.get_city_stats()
    assert city_dist is not None
    print("\n城市分布TOP5：")
    print(dict(sorted(city_dist['count'].items(), key=lambda x: x[1], reverse=True)[:5]))

    # 测试技能需求分析
    skills = processor.get_skills_stats()
    assert skills is not None
    print("\n最受欢迎的技能TOP10：")
    print(dict(sorted(skills['count'].items(), key=lambda x: x[1], reverse=True)[:10]))

    # 测试学历要求分布
    education = processor.get_education_stats()
    assert education is not None
    print("\n学历要求分布：")
    print(education['count'])

    # 测试工作经验分布
    experience = processor.get_experience_stats()
    assert experience is not None
    print("\n工作经验要求分布：")
    print(experience['count'])

if __name__ == '__main__':
    test_job_data_processor()