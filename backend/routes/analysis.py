from flask import Blueprint, jsonify, request
from sqlalchemy import create_engine, func, distinct, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import *

# 创建蓝图对象，用于组织相关的路由
bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/citi_job_count')  # 注意URL拼写与需求一致
def get_city_job_data():
    """获取城市职位统计数据
    
    Returns:
        JSON: 结构示例：
        [
            {"city": "北京", "job_count": 2543},
            {"city": "上海", "job_count": 1987}
        ]
    """
    try:
        # 使用SQLAlchemy查询数据库
        data = CityJobCount.query.order_by(CityJobCount.job_count.desc()).all()
        # 确保转换为数组格式
        result = [{"city": item.city, "job_count": item.job_count} for item in data]
        return jsonify(result)  # 直接返回数组
    except Exception as e:
        return jsonify({"error": str(e)}), 

@bp.route('/city_salary')  
def city_salary_data():
    """获取城市平均薪资数据
    
    Returns:
        JSON: 结构示例：
        [
            {"city": "北京", "avg_salary": 25000.5},
            {"city": "上海", "avg_salary": 23000.0}
        ]
    """
    try:
        # 查询全表数据并按薪资降序排序
        data = db.session.query(CitySalary).order_by(CitySalary.city.desc()).all()
        
        
        # 转换为字典列表
        result = [{"city": item.city, "avg_salary": item.avg_salary} for item in data]
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": "数据库查询失败",
            "details": str(e)
        }), 500

@bp.route('/education_salary')
def get_education_salary():
    """获取教育背景与薪资数据
    
    Returns:
        JSON: 结构示例：
        [
            {"education": "本科", "avg_salary": 15000.0},
            {"education": "硕士", "avg_salary": 25000.0}
        ]
    """
    try:
        # 查询全表数据并按薪资降序排序
        data = db.session.query(EducationSalary).order_by(EducationSalary.avg_salary.desc()).all()
        result = [item.to_dict() for item in data]
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": "数据库查询失败",
            "details": str(e)
        }), 500
        
@bp.route('/industry_salary')
def get_industry_salary():
    """获取行业平均薪资数据
    
    Returns:
        JSON: 结构示例：
        [
            {"industry": "互联网", "avg_salary": 25000.0},
            {"industry": "金融", "avg_salary": 23000.0}
        ]
    """
    try:
        # 查询全表数据并按薪资降序排序
        data = db.session.query(IndustrySalary).order_by(IndustrySalary.avg_salary.desc()).all()
        result = [item.to_dict() for item in data]
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": "数据库查询失败",
            "details": str(e)
        }), 500

@bp.route('/major_salary')
def get_major_salary():
    """获取专业/关键词平均薪资数据
    
    Returns:
        JSON: 结构示例：
        [
            {"search_keyword": "计算机科学", "avg_salary": 28000.0},
            {"search_keyword": "金融工程", "avg_salary": 26000.0}
        ]
    """
    try:
        # 查询全表数据并按薪资降序排序
        data = db.session.query(MajorSalary).order_by(MajorSalary.avg_salary.desc()).all()
        result = [item.to_dict() for item in data]
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": "数据库查询失败",
            "details": str(e)
        }), 500
@bp.route('/province_stats')
def get_province_stats():
    """获取省份统计数据
    
    Returns:
        JSON: 结构示例：
        [
            {"province": "广东", "count": 754, "avg_salary": 9745.01},
            {"province": "山东", "count": 715, "avg_salary": 9055.94}
        ]
    """
    try:
        data = db.session.query(ProvinceStats).all()
        result = [item.to_dict() for item in data]
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": "数据库查询失败",
            "details": str(e)
        }), 500

@bp.route('/jobs_new', methods=['GET'])
def search_jobs():
    """职位搜索接口
    
    Query Params:
        q (str): 搜索关键词
        page (int): 分页页码（默认1）
        per_page (int): 每页条数（默认20）
        
    Returns:
        JSON: 包含总数和结果列表
        {
            "total": 100,
            "results": [{...}, {...}]
        }
    """
    try:
        # 获取参数
        keyword = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 构建查询
        query = Job.query
        if keyword:
            search = f"%{keyword}%"
            query = query.filter(
                or_(
                    Job.position.ilike(search),
                    Job.company.ilike(search),
                    Job.skills.ilike(search),
                    Job.search_keyword.ilike(search)
                )
            )
        
        # 分页查询
        # 处理排序
        sort_field = request.args.get('sort_field', 'id')
        sort_order = request.args.get('sort_order', 'desc')
        
        # 字段映射
        sort_mapping = {
            'min_salary': Job.min_salary,
            'experience': Job.experience,
            'id': Job.id
        }
        
        order_field = sort_mapping.get(sort_field, Job.id)
        if sort_order.lower() == 'asc':
            query = query.order_by(order_field.asc())
        else:
            query = query.order_by(order_field.desc())
        
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            "total": pagination.total,
            "results": [job.to_dict() for job in pagination.items]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/datacount')
def get_data_count():
    """获取核心数据统计
    
    Returns:
        JSON: {
            "cities_count": 城市数量,
            "jobs_count": 职位总数, 
            "max_salary": 最高平均薪资,
            "min_salary": 最低平均薪资
        }
    """
    try:
        # 查询城市数量
        cities_count = db.session.query(func.count(distinct(Job.city))).scalar()

        # 查询职位总数
        jobs_count = db.session.query(func.count(Job.id)).scalar()

        # 查询最高平均薪资
        max_salary = db.session.query(func.max(Job.avg_salary)).scalar()
        # 查询最低平均薪资
        min_salary = db.session.query(func.min(Job.avg_salary)).scalar()
        return jsonify({
            "cities_count": cities_count,
            "jobs_count": jobs_count,
            "max_salary": max_salary,
            "min_salary": min_salary
        })

    except Exception as e:
        return jsonify({
            "error": "数据库查询失败",
            "details": str(e)
        }), 500

@bp.route('/jobs', methods=['GET'])
def get_jobs():
    # 获取参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    keyword = request.args.get('keyword', '').strip()

    # 基础查询
    query = Job.query

    # 关键字搜索（覆盖多个字段）
    if keyword:
        search_pattern = f'%{keyword}%'
        query = query.filter(
            or_(
                Job.position.ilike(search_pattern),
                Job.company.ilike(search_pattern),
                Job.city.ilike(search_pattern),
                Job.skills.ilike(search_pattern),
                Job.industry.ilike(search_pattern)
                # 其他需要搜索的字段...
            )
        )

    # 分页
    paginated_data = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 转换为字典列表
    jobs = [job.to_dict() for job in paginated_data.items]

    # 返回分页数据（包含元信息）
    return jsonify({
        'jobs': jobs,
        'total_pages': paginated_data.pages,
        'current_page': paginated_data.page,
        'total_items': paginated_data.total
    })


@bp.route('/recruit_ratio')
def get_recruit_ratio():
    """统计每个职位的招聘人数总和，返回格式：[{"position": "职位名称", "count": 招聘人数}]"""
    try:
        # 聚合每个职位的招聘人数，过滤numbers为空的数据
        data = db.session.query(
            Job.industry,
            func.sum(Job.numbers).label('count')
        ).filter(Job.numbers != None).group_by(Job.industry).order_by(func.sum(Job.numbers).desc()).all()
        result = [
            {"industry": item[0], "count": int(item[1]) if item[1] is not None else 0}
            for item in data if item[0]
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500