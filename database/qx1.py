import pymysql
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'zhaopin'
}

# 创建统计表（如果不存在）
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS job_statistics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total_positions INT,
    covered_cities INT,
    highest_salary DOUBLE,
    lowest_salary DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def main():
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 创建统计表
        cursor.execute(CREATE_TABLE_SQL)
        
        # 执行统计查询
        stats_query = """
        SELECT 
            COUNT(*) AS total_positions,
            COUNT(DISTINCT city) AS covered_cities,
            MAX(max_salary) AS highest_salary,
            MIN(min_salary) AS lowest_salary
        FROM jobs_new;
        """
        cursor.execute(stats_query)
        result = cursor.fetchone()
        
        # 解析结果
        total_positions, covered_cities, highest_salary, lowest_salary = result
        
        # 插入统计结果
        insert_query = """
        INSERT INTO job_statistics 
            (total_positions, covered_cities, highest_salary, lowest_salary)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (total_positions, covered_cities, highest_salary, lowest_salary))
        
        connection.commit()
        print("统计结果已成功保存到数据库")
        
    except Exception as e:
        print(f"操作失败: {str(e)}")
        connection.rollback()
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()