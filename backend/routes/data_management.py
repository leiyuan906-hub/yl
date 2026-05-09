from flask import Blueprint, jsonify
from models import *
from sqlalchemy import func


bp = Blueprint('data_management', __name__)

@bp.route('/api/data_status')
def get_data_status():
    """获取数据状态信息
    
    返回数据库中的记录总数、最新更新ID和数据状态
    数据状态分为'normal'(有数据)和'empty'(无数据)两种
    
    Returns:
        JSON: 包含数据状态信息的对象
    """
    # 获取总记录数
    total = db.session.query(Job).count()
    
    # 获取最新ID（如果无数据则返回0）
    latest_id = db.session.query(func.max(Job.id)).scalar() or 0
    
    # 确定数据状态
    status = 'normal' if total > 0 else 'empty'
    
    return jsonify({
        'total_records': total,
        'latest_id': latest_id,
        'status': status
    })

@bp.route('/api/statistics')
def get_statistics():
    """获取数据统计概览
    
    返回数据库中的职位总数、平均薪资、城市数量和行业数量等统计信息
    
    Returns:
        JSON: 包含统计数据的对象，格式示例：
        {
            "total_jobs": 100,
            "avg_salary": 25000.5,
            "unique_cities": 15,
            "unique_industries": 8
        }
    """
    try:
        total_jobs = db.session.query(func.count(Job.id)).scalar() or 0
        avg_salary = db.session.query(func.avg(Job.avg_salary)).scalar() or 0
        unique_cities = db.session.query(func.count(func.distinct(Job.city))).scalar() or 0
        unique_industries = db.session.query(func.count(func.distinct(Job.industry))).scalar() or 0
        
        return jsonify({
            "total_jobs": total_jobs,
            "avg_salary": round(float(avg_salary), 2),
            "unique_cities": unique_cities,
            "unique_industries": unique_industries
        })
    except Exception as e:
        app.logger.error(f"Failed to get statistics: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
        
@bp.route('/industry_distribution')
def get_industry_distribution():
    # 示例SQL: SELECT industry, COUNT(*) FROM jobs_new GROUP BY industry
    data = db.session.query(Job.industry, func.count(Job.id)).group_by(Job.industry).all()
    return jsonify({item[0]: item[1] for item in data})

@bp.route('/api/export_jobs')
def export_jobs():
    try:
        import io
        import csv
        jobs = Job.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
             'position', 'city', 'company', 'salary', 'experience', 'education', 'industry', 'skills', 'benefits', 'search_keyword', 'min_salary', 'max_salary', 'avg_salary'
        ])
        for job in jobs:
            writer.writerow([
                 job.position, job.city, job.company, job.salary, job.experience, job.education, job.industry, job.skills, job.benefits, job.search_keyword, job.min_salary, job.max_salary, job.avg_salary
            ])
        output.seek(0)
        from flask import Response
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=jobs_export.csv'
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500