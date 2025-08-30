from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
import urllib3
from datetime import datetime
import threading
import time

app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

CORS(app)

# 抢购平台API配置
PLATFORM_API_BASE = "https://nncx-api.shujiejiyuan.com"

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置requests会话
session = requests.Session()
session.verify = False  # 禁用SSL验证
session.timeout = 30    # 增加超时时间

# 清除可能的代理设置
session.proxies.clear()

# 授权用户列表（可以配置在环境变量或配置文件中）
AUTHORIZED_USERS = [
    "15192025411",
    "13553232959"
]

# 托管任务存储（实际应用中应该使用数据库）
TASKS = {}
TASK_COUNTER = 1
TASK_SCHEDULER_RUNNING = False

# 验证用户是否授权
def is_user_authorized(phone):
    return True

def execute_purchase_task(task):
    """执行抢购任务 - 多线程优化版本"""
    try:
        logger.info(f"开始执行抢购任务: {task['id']}")
        
        # 获取任务参数
        product_id = task['product_id']
        password = task['password']
        sign = task['sign']
        max_retries = task['max_retries']
        retry_interval = task['retry_interval']
        user_token = task['user_token']
        
        # 添加日志
        task['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'message': f'开始多线程抢购商品ID: {product_id}',
            'type': 'info'
        })
        
        success = False
        threads = []
        results = []
        
        # 创建多个线程同时抢购
        for attempt in range(1, max_retries + 1):
            task['current_attempt'] = attempt
            
            task['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'message': f'启动第{attempt}个抢购线程',
                'type': 'info'
            })
            
            # 创建抢购线程
            thread = threading.Thread(
                target=execute_single_purchase,
                args=(task, attempt, product_id, password, sign, user_token, results)
            )
            thread.daemon = True
            threads.append(thread)
            thread.start()
            
            # 快速启动下一个线程，不等待响应
            if attempt < max_retries:
                time.sleep(0.2)  # 200毫秒间隔启动线程
        
        # 等待所有线程完成
        for thread in threads:
            thread.join(timeout=30)  # 最多等待30秒
        
        # 检查是否有成功的抢购
        success = any(results)
        
        if success:
            task['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'message': f'多线程抢购成功',
                'type': 'success'
            })
        else:
            task['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'message': f'所有{max_retries}个抢购线程均失败',
                'type': 'error'
            })
        
        logger.info(f"多线程抢购任务执行完成: {task['id']}, 结果: {'成功' if success else '失败'}")
        return success
        
    except Exception as e:
        logger.error(f"执行抢购任务异常: {str(e)}")
        task['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'message': f'执行抢购任务异常: {str(e)}',
            'type': 'error'
        })
        return False

def execute_single_purchase(task, attempt, product_id, password, sign, user_token, results):
    """单个抢购线程的执行函数"""
    try:
        # 准备抢购数据
        timer = int(datetime.now().timestamp() * 1000)
        purchase_data = {
            'id': f'[{product_id}]',
            'password': password,
            'timer': timer,
            'sign': sign
        }
        
        task['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'message': f'线程{attempt}发送抢购请求',
            'type': 'info'
        })
        
        # 创建独立的session，避免线程冲突
        thread_session = requests.Session()
        thread_session.verify = False
        thread_session.timeout = 5  # 5秒超时
        
        # 发送抢购请求（不等待响应）
        try:
            # 使用异步方式发送请求，不阻塞
            response = thread_session.post(
                f"{PLATFORM_API_BASE}/sellMarket/smart",
                headers={
                    'Token': user_token,
                    'Content-Type': 'application/json',
                },
                json=purchase_data,
                timeout=5  # 5秒超时
            )
            
            if response.status_code == 200:
                response_data = response.json()
                
                task['logs'].append({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'message': f'线程{attempt}收到响应: {response_data.get("code", "未知")}',
                    'type': 'info'
                })
                
                if response_data.get('code') == 200:
                    task['logs'].append({
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'message': f'线程{attempt}抢购成功！',
                        'type': 'success'
                    })
                    results.append(True)
                    return
                else:
                    task['logs'].append({
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'message': f'线程{attempt}抢购失败: {response_data.get("message", "未知错误")}',
                        'type': 'error'
                    })
            else:
                task['logs'].append({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'message': f'线程{attempt}请求失败: HTTP {response.status_code}',
                    'type': 'error'
                })
                
        except requests.exceptions.Timeout:
            task['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'message': f'线程{attempt}请求超时',
                'type': 'warning'
            })
        except requests.exceptions.ConnectionError:
            task['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'message': f'线程{attempt}连接错误',
                'type': 'warning'
            })
        except Exception as e:
            task['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'message': f'线程{attempt}异常: {str(e)}',
                'type': 'error'
            })
        
        results.append(False)
        
    except Exception as e:
        logger.error(f"线程{attempt}执行异常: {str(e)}")
        results.append(False)

def task_scheduler():
    """任务调度器，检查并执行到期的托管任务"""
    global TASKS, TASK_SCHEDULER_RUNNING
    
    logger.info("任务调度器启动")
    
    while TASK_SCHEDULER_RUNNING:
        try:
            current_time = datetime.now()
            
            # 检查所有等待中的任务
            for task_id, task in TASKS.items():
                if task['status'] == 'waiting':
                    try:
                        target_time = datetime.strptime(task['target_time'], '%Y-%m-%d %H:%M:%S')
                        
                        # 如果到达目标时间，执行任务
                        if current_time >= target_time:
                            logger.info(f"任务 {task_id} 到达执行时间，开始执行")
                            
                            # 更新任务状态
                            task['status'] = 'running'
                            task['current_attempt'] = 0
                            
                            # 添加日志
                            task['logs'].append({
                                'time': current_time.strftime('%H:%M:%S'),
                                'message': '到达目标时间，开始执行抢购',
                                'type': 'info'
                            })
                            
                            # 在新线程中执行抢购，避免阻塞调度器
                            def execute_task_async(task_id, task):
                                try:
                                    success = execute_purchase_task(task)
                                    
                                    if success:
                                        task['status'] = 'success'
                                        task['logs'].append({
                                            'time': datetime.now().strftime('%H:%M:%S'),
                                            'message': '抢购成功',
                                            'type': 'success'
                                        })
                                    else:
                                        task['status'] = 'failed'
                                        task['logs'].append({
                                            'time': datetime.now().strftime('%H:%M:%S'),
                                            'message': '抢购失败',
                                            'type': 'error'
                                        })
                                    
                                    logger.info(f"异步任务执行完成: {task_id}, 结果: {'成功' if success else '失败'}")
                                    
                                except Exception as e:
                                    logger.error(f"异步任务执行异常: {task_id}, {str(e)}")
                                    task['status'] = 'failed'
                                    task['logs'].append({
                                        'time': datetime.now().strftime('%H:%M:%S'),
                                        'message': f'执行异常: {str(e)}',
                                        'type': 'error'
                                    })
                            
                            # 启动异步执行线程
                            thread = threading.Thread(target=execute_task_async, args=(task_id, task))
                            thread.daemon = True
                            thread.start()
                            
                    except Exception as e:
                        logger.error(f"检查任务 {task_id} 时出错: {str(e)}")
            
            # 每1秒检查一次
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"任务调度器异常: {str(e)}")
            time.sleep(5)  # 出错时等待5秒再继续
    
    logger.info("任务调度器停止")

def start_task_scheduler():
    """启动任务调度器"""
    global TASK_SCHEDULER_RUNNING
    
    if not TASK_SCHEDULER_RUNNING:
        TASK_SCHEDULER_RUNNING = True
        scheduler_thread = threading.Thread(target=task_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        logger.info("任务调度器已启动")



def proxy_to_platform(endpoint, method='POST', require_auth=True):
    """
    通用代理函数，转发请求到抢购平台
    
    Args:
        endpoint: 抢购平台接口路径
        method: HTTP方法
        require_auth: 是否需要验证用户授权
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            logger.info(f"收到代理请求 - 接口: {endpoint}, 方法: {method}")
            
            # 验证用户授权 - 通过抢购平台token获取用户信息
            if require_auth:
                token = request.headers.get('Token')
                if not token:
                    logger.warning(f"未提供Token - 接口: {endpoint}")
                    return jsonify({'error': '未授权访问'}), 401
                
                logger.info(f"验证Token - 接口: {endpoint}")
                
                # 通过抢购平台的GetUserInfo接口验证token和获取用户信息
                try:
                    user_response = session.post(
                        f"{PLATFORM_API_BASE}/GetUserInfo",
                        headers={
                            'Token': token,
                            'Content-Type': 'application/json',
                        },
                        json={}
                    )
                    
                    logger.info(f"GetUserInfo响应状态码: {user_response.status_code}")
                    logger.info(f"GetUserInfo响应内容: {user_response.text}")
                    
                    if user_response.status_code != 200:
                        logger.warning(f"GetUserInfo请求失败 - 状态码: {user_response.status_code}")
                        return jsonify({'error': '无效token'}), 401
                    
                    user_data = user_response.json()
                    if user_data.get('code') != 200:
                        logger.warning(f"GetUserInfo返回错误 - code: {user_data.get('code')}")
                        return jsonify({'error': '无效token'}), 401
                    
                    mobile = user_data.get('data', {}).get('mobile')
                    logger.info(f"获取到用户手机号: {mobile}")
                    
                    if not mobile or not is_user_authorized(mobile):
                        logger.warning(f"用户未授权 - 手机号: {mobile}")
                        return jsonify({'error': '用户未授权'}), 403
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"验证Token失败: {str(e)}")
                    return jsonify({'error': '验证token失败'}), 401
            
            try:
                # 转发请求到抢购平台
                platform_url = f"{PLATFORM_API_BASE}/{endpoint}"
                logger.info(f"转发请求到抢购平台: {platform_url}")
                logger.info(f"请求方法: {method}")
                logger.info(f"请求头: {dict(request.headers)}")
                logger.info(f"请求数据: {request.get_json() or {}}")
                
                response = session.request(
                    method,
                    platform_url,
                    headers={
                        'Token': request.headers.get('Token', ''),
                        'Content-Type': 'application/json',
                        'User-Agent': request.headers.get('User-Agent', ''),
                    },
                    json=request.get_json() or {}
                )
                
                logger.info(f"抢购平台响应状态码: {response.status_code}")
                logger.info(f"抢购平台响应内容: {response.text}")
                
                # 直接返回抢购平台的响应
                return jsonify(response.json()), response.status_code
                
            except requests.exceptions.ConnectTimeout as e:
                logger.error(f"连接超时: {str(e)}")
                return jsonify({'error': f'连接超时，请检查网络连接'}), 500
            except requests.exceptions.ConnectionError as e:
                logger.error(f"连接错误: {str(e)}")
                return jsonify({'error': f'连接错误，请检查网络或代理设置'}), 500
            except requests.exceptions.RequestException as e:
                logger.error(f"请求抢购平台失败: {str(e)}")
                return jsonify({'error': f'请求抢购平台失败: {str(e)}'}), 500
        
        wrapper.__name__ = f'proxy_{endpoint.lower()}'
        return wrapper
    return decorator

# 登录接口 - 转发到抢购平台
@app.route('/api/login_password', methods=['POST'])
def login_with_password():
    data = request.get_json()
    mobile = data.get('mobile')
    password = data.get('password')
    
    logger.info(f"收到登录请求 - 手机号: {mobile}")
    
    if not mobile or not password:
        logger.warning(f"登录参数缺失 - 手机号: {mobile}, 密码: {'有' if password else '无'}")
        return jsonify({'error': '手机号和密码不能为空'}), 400
    
    # 检查用户是否为我们平台的授权用户
    if not is_user_authorized(mobile):
        logger.warning(f"用户未授权 - 手机号: {mobile}")
        return jsonify({'error': '您尚未获得系统授权，请联系管理员'}), 403
    
    logger.info(f"用户已授权，转发登录请求到抢购平台 - 手机号: {mobile}")
    
    try:
        # 转发登录请求到抢购平台
        platform_url = f"{PLATFORM_API_BASE}/login_password"
        logger.info(f"请求抢购平台: {platform_url}")
        logger.info(f"请求数据: {data}")
        
        response = session.post(
            platform_url,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': request.headers.get('User-Agent', ''),
            },
            json=data
        )
        
        logger.info(f"抢购平台响应状态码: {response.status_code}")
        logger.info(f"抢购平台响应内容: {response.text}")
        
        # 直接返回抢购平台的响应
        return jsonify(response.json()), response.status_code
            
    except requests.exceptions.ConnectTimeout as e:
        logger.error(f"连接超时: {str(e)}")
        return jsonify({'error': f'连接超时，请检查网络连接'}), 500
    except requests.exceptions.ConnectionError as e:
        logger.error(f"连接错误: {str(e)}")
        return jsonify({'error': f'连接错误，请检查网络或代理设置'}), 500
    except requests.exceptions.RequestException as e:
        logger.error(f"请求抢购平台失败: {str(e)}")
        return jsonify({'error': f'请求抢购平台失败: {str(e)}'}), 500

# 用户信息接口
@app.route('/api/GetUserInfo', methods=['POST'])
@proxy_to_platform('GetUserInfo', 'POST', require_auth=True)
def get_user_info():
    pass

# 托管任务管理接口
@app.route('/api/proxy/tasks', methods=['GET'])
def get_tasks():
    """获取用户的托管任务列表"""
    global TASKS
    
    token = request.headers.get('Token')
    if not token:
        return jsonify({'error': '未授权访问'}), 401
    
    try:
        # 验证用户
        user_response = session.post(
            f"{PLATFORM_API_BASE}/GetUserInfo",
            headers={'Token': token, 'Content-Type': 'application/json'},
            json={}
        )
        
        if user_response.status_code != 200:
            return jsonify({'error': '无效token'}), 401
        
        user_data = user_response.json()
        if user_data.get('code') != 200:
            return jsonify({'error': '无效token'}), 401
        
        mobile = user_data.get('data', {}).get('mobile')
        if not mobile or not is_user_authorized(mobile):
            return jsonify({'error': '用户未授权'}), 403
        
        # 返回用户的任务列表
        user_tasks = [task for task in TASKS.values() if task.get('user_mobile') == mobile]
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': user_tasks
        })
        
    except Exception as e:
        logger.error(f"获取任务列表失败: {str(e)}")
        return jsonify({'error': '获取任务列表失败'}), 500

@app.route('/api/proxy/tasks', methods=['POST'])
def create_task():
    """创建托管任务"""
    global TASKS, TASK_COUNTER
    
    token = request.headers.get('Token')
    if not token:
        return jsonify({'error': '未授权访问'}), 401
    
    data = request.get_json()
    
    try:
        # 验证用户
        user_response = session.post(
            f"{PLATFORM_API_BASE}/GetUserInfo",
            headers={'Token': token, 'Content-Type': 'application/json'},
            json={}
        )
        
        if user_response.status_code != 200:
            return jsonify({'error': '无效token'}), 401
        
        user_data = user_response.json()
        if user_data.get('code') != 200:
            return jsonify({'error': '无效token'}), 401
        
        mobile = user_data.get('data', {}).get('mobile')
        if not mobile or not is_user_authorized(mobile):
            return jsonify({'error': '用户未授权'}), 403
        
        # 创建新任务
        task_id = TASK_COUNTER
        TASK_COUNTER += 1
        
        task = {
            'id': task_id,
            'user_mobile': mobile,
            'user_token': token,
            'product_id': data.get('product_id'),
            'product_name': data.get('product_name', '未知商品'),
            'target_time': data.get('target_time'),
            'password': data.get('password'),
            'sign': data.get('sign'),
            'max_retries': data.get('max_retries', 3),
            'retry_interval': data.get('retry_interval', 1000),
            'status': 'waiting',
            'current_attempt': 0,
            'logs': [],
            'created_at': datetime.now().isoformat()
        }
        
        TASKS[task_id] = task
        
        logger.info(f"创建托管任务: {task_id}, 用户: {mobile}")
        
        return jsonify({
            'code': 200,
            'message': '任务创建成功',
            'data': task
        })
        
    except Exception as e:
        logger.error(f"创建任务失败: {str(e)}")
        return jsonify({'error': '创建任务失败'}), 500

# 多线程抢购接口
@app.route('/api/proxy/multi_purchase', methods=['POST'])
def multi_purchase():
    """多线程并发抢购接口"""
    token = request.headers.get('Token')
    if not token:
        return jsonify({'error': '未授权访问'}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')
    password = data.get('password')
    sign = data.get('sign')
    thread_count = data.get('thread_count', 5)  # 默认5个线程
    
    try:
        # 验证用户
        user_response = session.post(
            f"{PLATFORM_API_BASE}/GetUserInfo",
            headers={'Token': token, 'Content-Type': 'application/json'},
            json={}
        )
        
        if user_response.status_code != 200:
            return jsonify({'error': '无效token'}), 401
        
        user_data = user_response.json()
        if user_data.get('code') != 200:
            return jsonify({'error': '无效token'}), 401
        
        mobile = user_data.get('data', {}).get('mobile')
        if not mobile or not is_user_authorized(mobile):
            return jsonify({'error': '用户未授权'}), 403
        
        # 创建多线程抢购任务
        threads = []
        results = []
        
        logger.info(f"开始多线程抢购: 商品ID={product_id}, 线程数={thread_count}")
        
        # 启动多个抢购线程
        for i in range(thread_count):
            thread = threading.Thread(
                target=execute_single_purchase_optimized,
                args=(product_id, password, sign, token, i+1, results)
            )
            thread.daemon = True
            threads.append(thread)
            thread.start()
            
            # 快速启动，不等待
            time.sleep(0.2)  # 200毫秒间隔
        
        # 等待所有线程完成
        for thread in threads:
            thread.join(timeout=15)  # 15秒超时
        
        # 检查结果
        success = any(results)
        
        logger.info(f"多线程抢购完成: 成功={success}, 结果={results}")
        
        return jsonify({
            'code': 200,
            'message': '多线程抢购完成',
            'data': {
                'success': success,
                'results': results,
                'thread_count': thread_count
            }
        })
        
    except Exception as e:
        logger.error(f"多线程抢购异常: {str(e)}")
        return jsonify({'error': f'多线程抢购异常: {str(e)}'}), 500

def execute_single_purchase_optimized(product_id, password, sign, user_token, thread_id, results):
    """优化的单个抢购线程"""
    try:
        # 准备抢购数据
        timer = int(datetime.now().timestamp() * 1000)
        purchase_data = {
            'id': f'[{product_id}]',
            'password': password,
            'timer': timer,
            'sign': sign
        }
        
        logger.info(f"线程{thread_id}发送抢购请求")
        
        # 创建独立的session
        thread_session = requests.Session()
        thread_session.verify = False
        thread_session.timeout = 3  # 3秒超时，更快响应
        
        # 发送抢购请求
        response = thread_session.post(
            f"{PLATFORM_API_BASE}/sellMarket/smart",
            headers={
                'Token': user_token,
                'Content-Type': 'application/json',
            },
            json=purchase_data,
            timeout=3
        )
        
        if response.status_code == 200:
            response_data = response.json()
            
            if response_data.get('code') == 200:
                logger.info(f"线程{thread_id}抢购成功！")
                results.append(True)
                return
            else:
                logger.info(f"线程{thread_id}抢购失败: {response_data.get('message')}")
        else:
            logger.info(f"线程{thread_id}请求失败: HTTP {response.status_code}")
            
    except requests.exceptions.Timeout:
        logger.info(f"线程{thread_id}请求超时")
    except requests.exceptions.ConnectionError:
        logger.info(f"线程{thread_id}连接错误")
    except Exception as e:
        logger.error(f"线程{thread_id}异常: {str(e)}")
    
    results.append(False)

@app.route('/api/proxy/tasks/<int:task_id>/start', methods=['POST'])
def start_task(task_id):
    """立即执行托管任务"""
    global TASKS
    
    token = request.headers.get('Token')
    if not token:
        return jsonify({'error': '未授权访问'}), 401
    
    if task_id not in TASKS:
        return jsonify({'error': '任务不存在'}), 404
    
    task = TASKS[task_id]
    
    try:
        # 验证用户权限
        if task['user_token'] != token:
            return jsonify({'error': '无权限操作此任务'}), 403
        
        # 更新任务状态
        task['status'] = 'running'
        task['current_attempt'] = 0
        
        # 添加日志
        task['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'message': '任务开始执行',
            'type': 'info'
        })
        
        # 执行抢购逻辑
        success = execute_purchase_task(task)
        
        if success:
            task['status'] = 'success'
            task['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'message': '抢购成功',
                'type': 'success'
            })
        else:
            task['status'] = 'failed'
            task['logs'].append({
                'time': datetime.now().strftime('%H:%M:%S'),
                'message': '抢购失败',
                'type': 'error'
            })
        
        logger.info(f"任务执行完成: {task_id}, 结果: {'成功' if success else '失败'}")
        
        return jsonify({
            'code': 200,
            'message': '任务执行完成',
            'data': task
        })
        
    except Exception as e:
        logger.error(f"执行任务失败: {str(e)}")
        task['status'] = 'failed'
        task['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'message': f'执行异常: {str(e)}',
            'type': 'error'
        })
        return jsonify({'error': '执行任务失败'}), 500

@app.route('/api/proxy/tasks/<int:task_id>/cancel', methods=['POST'])
def cancel_task(task_id):
    """取消托管任务"""
    global TASKS
    
    token = request.headers.get('Token')
    if not token:
        return jsonify({'error': '未授权访问'}), 401
    
    if task_id not in TASKS:
        return jsonify({'error': '任务不存在'}), 404
    
    task = TASKS[task_id]
    
    try:
        # 验证用户权限
        if task['user_token'] != token:
            return jsonify({'error': '无权限操作此任务'}), 403
        
        # 更新任务状态
        task['status'] = 'cancelled'
        
        # 添加日志
        task['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'message': '任务已取消',
            'type': 'warning'
        })
        
        logger.info(f"取消任务: {task_id}")
        
        return jsonify({
            'code': 200,
            'message': '任务已取消',
            'data': task
        })
        
    except Exception as e:
        logger.error(f"取消任务失败: {str(e)}")
        return jsonify({'error': '取消任务失败'}), 500

@app.route('/api/proxy/tasks/<int:task_id>/logs', methods=['GET'])
def get_task_logs(task_id):
    """获取任务执行日志"""
    global TASKS
    
    token = request.headers.get('Token')
    if not token:
        return jsonify({'error': '未授权访问'}), 401
    
    if task_id not in TASKS:
        return jsonify({'error': '任务不存在'}), 404
    
    task = TASKS[task_id]
    
    try:
        # 验证用户权限
        if task['user_token'] != token:
            return jsonify({'error': '无权限查看此任务'}), 403
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': task.get('logs', [])
        })
        
    except Exception as e:
        logger.error(f"获取任务日志失败: {str(e)}")
        return jsonify({'error': '获取任务日志失败'}), 500

# 网络连接测试接口
@app.route('/api/test_connection', methods=['GET'])
def test_connection():
    """测试与抢购平台的网络连接"""
    try:
        logger.info("开始测试网络连接...")
        
        # 测试基本连接
        response = session.get(f"{PLATFORM_API_BASE}/", timeout=5)
        logger.info(f"连接测试成功，状态码: {response.status_code}")
        
        return jsonify({
            'success': True,
            'message': '网络连接正常',
            'status_code': response.status_code
        })
        
    except requests.exceptions.ConnectTimeout:
        logger.error("连接超时")
        return jsonify({
            'success': False,
            'message': '连接超时，请检查网络'
        }), 500
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"连接错误: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'连接错误: {str(e)}'
        }), 500
        
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'未知错误: {str(e)}'
        }), 500

# 通用代理接口 - 可以处理任何抢购平台接口
@app.route('/api/proxy/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_any_endpoint(endpoint):
    """
    通用代理接口，可以转发任何请求到抢购平台
    
    使用方式：
    POST /api/proxy/GetUserInfo
    POST /api/proxy/GetMarketList
    POST /api/proxy/CreateOrder
    等等...
    """
    logger.info(f"收到通用代理请求 - 接口: {endpoint}, 方法: {request.method}")
    
    # 验证用户授权 - 通过抢购平台token获取用户信息
    token = request.headers.get('Token')
    if not token:
        logger.warning(f"未提供Token - 通用代理接口: {endpoint}")
        return jsonify({'error': '未授权访问'}), 401
    
    # 通过抢购平台的GetUserInfo接口验证token和获取用户信息
    try:
        logger.info(f"验证Token - 通用代理接口: {endpoint}")
        user_response = session.post(
            f"{PLATFORM_API_BASE}/GetUserInfo",
            headers={
                'Token': token,
                'Content-Type': 'application/json',
            },
            json={}
        )
        
        logger.info(f"GetUserInfo响应状态码: {user_response.status_code}")
        logger.info(f"GetUserInfo响应内容: {user_response.text}")
        
        if user_response.status_code != 200:
            logger.warning(f"GetUserInfo请求失败 - 状态码: {user_response.status_code}")
            return jsonify({'error': '无效token'}), 401
        
        user_data = user_response.json()
        if user_data.get('code') != 200:
            logger.warning(f"GetUserInfo返回错误 - code: {user_data.get('code')}")
            return jsonify({'error': '无效token'}), 401
        
        mobile = user_data.get('data', {}).get('mobile')
        logger.info(f"获取到用户手机号: {mobile}")
        
        if not mobile or not is_user_authorized(mobile):
            logger.warning(f"用户未授权 - 手机号: {mobile}")
            return jsonify({'error': '用户未授权'}), 403
            
    except requests.exceptions.RequestException as e:
        logger.error(f"验证Token失败: {str(e)}")
        return jsonify({'error': '验证token失败'}), 401
    
    try:
        # 转发请求到抢购平台
        platform_url = f"{PLATFORM_API_BASE}/{endpoint}"
        logger.info(f"转发请求到抢购平台: {platform_url}")
        logger.info(f"请求方法: {request.method}")
        logger.info(f"请求头: {dict(request.headers)}")
        logger.info(f"请求数据: {request.get_json() or {}}")
        
        response = session.request(
            request.method,
            platform_url,
            headers={
                'Token': token,
                'Content-Type': 'application/json',
                'User-Agent': request.headers.get('User-Agent', ''),
            },
            json=request.get_json() or {}
        )
        
        logger.info(f"抢购平台响应状态码: {response.status_code}")
        logger.info(f"抢购平台响应内容: {response.text}")
        
        # 直接返回抢购平台的响应
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.RequestException as e:
        logger.error(f"请求抢购平台失败: {str(e)}")
        return jsonify({'error': f'请求抢购平台失败: {str(e)}'}), 500

if __name__ == '__main__':
    # 启动任务调度器
    start_task_scheduler()
    
    app.run(debug=True, host='0.0.0.0', port=5001)