import json

from flask import request, jsonify, Response

from app import db
from app.main import main
from app.models.models import Activity, Declare, User, Train


# 获取申报和参与申报的用户数、各月提交数、活动报名人数
@main.route('/manageall')
def manageall():
    activities = Activity.query.all()
    # 各月提交活动统计
    activity_month = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0,
                      '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0}
    for activity in activities:
        activity_month[str(activity.updatetime.month)] += 1

    return jsonify(activity_month)


# 列表显示用户申报信息
@main.route('/searchdeclareuser')
def searchdeclareuser():
    # 查询所有的申报任务与对应的申报用户
    result = []
    declare = Declare.query.all()
    # declare.udeclares返回UDeclare的列表
    # d:申报任务; ducu:用户申报记录; ud:用户申报;
    for dec in declare:
        for d in dec.udeclares:
            result.append({'name': User.query.filter_by(id=d.id).first().username, 'begintime': dec.begintime,
                           'endtime': dec.endtime, 'uptime': d.uptime})
    # print(result)
    return jsonify(result)


# 通过用户申报
@main.route('/tgdeclareuser', methods=['GET', 'POST'])
def tgdeclareuser():
    if request.method == 'GET':
        pass
    else:
        pass
    return Response(json.dumps({'status': True}), mimetype='application/json')


# 添加新的申报任务
@main.route('/adddeclare', methods=['GET', 'POST'])
def adddeclare():
    if request.method == 'GET':
        name = request.args.get('name')
        begintime = request.args.get('begintime')
        endtime = request.args.get('endtime')
        main = request.args.get('main')
    else:
        name = request.form.get('name')
        begintime = request.form.get('begintime')
        endtime = request.form.get('endtime')
        main = request.form.get('main')
    print(name)
    declare = Declare(name=name, begintime=begintime, endtime=endtime, main=main)
    db.session.add(declare)
    db.session.commit()
    return Response(json.dumps({'status': True}), mimetype='application/json')


# 列表显示用户申请培训信息
@main.route('/searchabilityuser')
def searchabilityuser():
    # 查询所有的能力提升培训与对应的申请的用户
    result = []
    train = Train.query.all()
    # d:申报任务; ducu:用户申报记录; ud:用户申报;
    for tra in train:
        for t in tra.utrains:
            result.append({'name': User.query.filter_by(id=t.id).first().username, 'begintime': tra.begintime,
                           'endtime': tra.endtime, 'uptime': t.uptime})
    # print(result)
    return jsonify(result)
