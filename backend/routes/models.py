from flask_sqlalchemy import SQLAlchemy

# 初始化SQLAlchemy对象，用于数据库操作
db = SQLAlchemy()

class CityJobCount(db.Model):
    __tablename__ = 'city_job_count'  # 严格对应表名
    
    city = db.Column(db.Text, primary_key=True)  # city作为主键
    job_count = db.Column(db.BigInteger, nullable=False)

class CitySalary(db.Model):
    __tablename__ = 'city_salary'  # 与表名严格对应
    
    city = db.Column(db.Text, primary_key=True)  # 城市作为主键
    avg_salary = db.Column(db.Float, nullable=False)  # 对应MySQL的double类型

    def to_dict(self):
        return {
            "city": self.city,
            "avg_salary": self.avg_salary
        }

class EducationSalary(db.Model):
    __tablename__ = 'education_salary'  # 与表名严格对应
    
    education = db.Column(db.Text, primary_key=True)  # 教育背景作为主键
    avg_salary = db.Column(db.Float, nullable=False)  # 对应MySQL的double类型

    def to_dict(self):
        return {
            "education": self.education,
            "avg_salary": self.avg_salary
        }

class IndustrySalary(db.Model):
    __tablename__ = 'industry_salary'  # 与表名严格对应
    
    industry = db.Column(db.Text, primary_key=True)  # 行业作为主键
    avg_salary = db.Column(db.Float, nullable=False)  # 对应MySQL的double类型

    def to_dict(self):
        return {
            "industry": self.industry,
            "avg_salary": self.avg_salary
        }

class Job(db.Model):
    __tablename__ = 'jobs_new'
    
    id = db.Column(db.BigInteger, primary_key=True)
    position = db.Column(db.Text,primary_key=True)
    city = db.Column(db.Text)
    company = db.Column(db.Text)
    salary = db.Column(db.Text)
    experience = db.Column(db.Text)
    education = db.Column(db.Text)
    industry = db.Column(db.Text)
    skills = db.Column(db.Text)
    benefits = db.Column(db.Text)
    search_keyword = db.Column(db.Text)
    min_salary = db.Column(db.Float)
    max_salary = db.Column(db.Float)
    avg_salary = db.Column(db.Float)
    numbers = db.Column(db.BigInteger)
    def to_dict(self):
        return {
            "id": self.id,
            "position": self.position,
            "city": self.city,
            "company": self.company,
            "salary": self.salary,
            "experience": self.experience,
            "education": self.education,
            "industry": self.industry,
            "skills": self.skills,
            "benefits": self.benefits,
            "search_keyword": self.search_keyword,
            "min_salary": self.min_salary,
            "max_salary": self.max_salary,
            "avg_salary": self.avg_salary,
        }

class ProvinceStats(db.Model):
    __tablename__ = 'province_stats'
    
    province = db.Column(db.Text, primary_key=True)  # 省份作为主键
    count = db.Column(db.BigInteger, nullable=False)
    avg_salary = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "province": self.province.replace("省", "").replace("市", "").replace("自治区", "").strip(),
            "count": self.count,
            "avg_salary": round(self.avg_salary, 2)
        }
class MajorSalary(db.Model):
    __tablename__ = 'major_salary'  # 与表名严格对应
    
    search_keyword = db.Column(db.Text, primary_key=True)  # 搜索关键词作为主键
    avg_salary = db.Column(db.Float, nullable=False)  # 对应MySQL的double类型

    def to_dict(self):
        return {
            "search_keyword": self.search_keyword,
            "avg_salary": self.avg_salary
        }