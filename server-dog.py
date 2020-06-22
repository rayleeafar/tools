import requests
import psutil
import time
import datetime
import os

server_jiang = [""]
server_jiang = ["SCU100404Tb017d76ebfaacc5d97803ac75b33bd5f5ed767e7d3d4e","SCU96080Tb69efe255f6f9986dca2a225cba739675eaa48af1a168"]
def push_server_jiang(title, content):
    for skey in server_jiang:
        api = "https://sc.ftqq.com/{server_jiang}.send".format(server_jiang=skey) 
        data = {
            "text": title,
            "desp": content
        }
        requests.post(api, data=data)
 
"""
获取系统基本信息
"""
 
EXPAND = 1024 * 1024 * 1024
 
def mems():
    ''' 获取系统内存使用情况 '''
    mem = psutil.virtual_memory()
    mem_str = " 内存状态如下:\n\n"
    mem_str += "   系统的内存使用率: " + '%0.3f'%((mem.used / mem.total)*100) + "%\n\n"
    mem_str += "   系统的内存容量为: " + '%0.3f'%(mem.total / EXPAND) + " GB\n\n"
    mem_str += "   系统的内存已使用容量为: " + '%0.3f'%(mem.used / EXPAND) + " GB\n\n"
    mem_str += "   系统可用的内存容量为: " + '%0.3f'%(mem.total / EXPAND - mem.used / EXPAND) + " GB\n\n"
    # mem_str += "   内存的buffer容量为: " + str(mem.buffers / EXPAND) + " MB\n"
    # mem_str += "   内存的cache容量为:" + str(mem.cached / EXPAND) + " MB\n"
    return mem_str,float(mem.used / mem.total)>0.5
 
 
def cpus():
    ''' 获取cpu的相关信息 '''
    cpu_str = " CPU状态如下:\n\n"
    cpu_status = psutil.cpu_times()
    cpu_str += "   user = " + str(cpu_status.user) + "\n\n"
    # cpu_str += "   nice = " + str(cpu_status.nice) + "\n\n"
    cpu_str += "   system = " + str(cpu_status.system) + "\n\n"
    cpu_str += "   idle = " + str(cpu_status.idle) + "\n\n"
    cpu_str += "   iowait = " + str(cpu_status.iowait) + "\n\n"
    # cpu_str += "   irq = " + str(cpu_status.irq) + "\n\n"
    # cpu_str += "   softirq = " + str(cpu_status.softirq) + "\n"
    # cpu_str += "   steal = " + str(cpu_status.steal) + "\n"
    # cpu_str += "   guest = " + str(cpu_status.guest) + "\n"
    search_command = 'netstat -nat|wc -l'
    num_connects = os.popen(search_command).read()
    cpu_str += "   tcp_connected_num = " + str(num_connects) + "\n"
    return cpu_str,int(num_connects) > 7000
 
def docker_info():
    '''get docker stats info'''
    dcmd = 'docker stats --no-stream'
    docker_info = os.popen(dcmd).read()
    cpu_str = "docker Infos:" + str(docker_info) + "\n"
    return cpu_str,False

def open_files():
    '''open files monitor'''
    cmd1 = "ps -aux | awk -F' [ ]*' '{print $2}'"
    cmd1_ret = os.popen(cmd1)
#    print(cmd1_ret)
    cmd21 = "ps -aux |grep "
    cmd22 = " | grep -v grep| awk -F' [ ]*' '{ for(i=1; i<=10; i++){ $i=\"\" }; print $0 }'" 
    cmd23 = "lsof -p "
    cmd24 = " | wc -l"
    sum_open_files = 0
    ret_info = "sys_open_files_info: Total[{TOTAL}]\n\n"
    for sl in cmd1_ret.readlines():
        pid = sl.strip()
        if pid.find("PID")>-1:
            continue
        file_num = os.popen(cmd23+pid+cmd24).read()
        sum_open_files += int(file_num)
        if int(file_num)>100:
            ret_info += file_num + " <==> "+ pid + " <==> "
            cmd2_ret = os.popen(cmd21+pid+cmd22).read()
            ret_info += cmd2_ret + "\n"
            if int(file_num)>10000:
                docker_name = ""
                docker_name_arr = cmd2_ret.split(' ')
                for dns in docker_name_arr:
                    if dns.startswith("-owner="):
                       docker_name = dns.split("=")[1]
                       break
                docker_restrat_cmd = "docker restart proxy_node_"+docker_name
                os.popen(docker_restrat_cmd)
    return ret_info.format(TOTAL=sum_open_files),sum_open_files > 30000
    
 
def disks():
    ''' 查看硬盘基本信息 '''
    ''' psutil.disk_partitions()    获取磁盘的完整信息
        psutil.disk_usage('/')      获得分区的使用情况,这边以根分区为例
        psutil.disk_io_counters()   获取磁盘总的io个数
        perdisk 默认为False
        psutil.disk_io_counters(perdisk=True)   perdisk为True 返回单个分区的io个数
    '''
    disk_str = " 硬盘信息如下:\n\n"
    disk = psutil.disk_usage('/')
    disk_str += "磁盘使用率为: " + '%0.3f'%((disk.used/disk.total)*100) + "%\n\n"
    disk_str += "磁盘容量为: " + '%0.3f'%(disk.total / EXPAND) + " GB\n\n"
    disk_str += "磁盘已使用容量为: " + '%0.3f'%(disk.used / EXPAND) + " GB\n\n"
    disk_str += "磁盘可用的内存容量为: " + '%0.3f'%(disk.free / EXPAND) + " GB\n\n"

    # disk_status = psutil.disk_partitions()
    # for item in disk_status:
    #     disk_str += str(item) + "\n"
    #     p = item.device
    #     disk = psutil.disk_usage(p)
    #     disk_str += p+"盘容量为: " + str(disk.total / EXPAND) + " MB\n"
    #     disk_str += p+"盘已使用容量为: " + str(disk.used / EXPAND) + " MB\n"
    #     disk_str += p+"盘可用的内存容量为: " + str(disk.free / EXPAND) + " MB\n"
    return disk_str,float(disk.used/disk.total) > 0.6
 
 
def users():
    ''' 查看当前登录的用户信息 '''
    user_str = " 登录用户信息如下:\n "
    user_status = psutil.users()
    for item in user_status:
        user_str += str(item) + "\n"
    return user_str
 
def process():
    ''' 查看进程信息 '''
    pids = psutil.pids()
    proces = []
    for pid in pids:
        p = psutil.Process(pid)
        jctime = str(datetime.datetime.fromtimestamp(p.create_time()))[:19]
        p_info = [
            p.name(),       # 进程的名字
            #p.exe(),        # 进程bin文件位置
            #p.cwd(),        # 进程的工作目录的绝对路径
            p.status(),     # 进程的状态
            jctime,         # 进程的创建时间
            #p.uids(),       # 进程的uid信息
            #p.gids(),       # 进程的gid信息
            p.cpu_times(),  # cup时间信息
            p.memory_info(),# 进程内存的利用率
            p.io_counters() # 进程的io读写信息
        ]
        proces.append(p_info)
    return proces

def check_loop(exIP,cf_list):
    push_info = ""
    push_it = False
    for cf in cf_list:
        ret = cf()
        if(ret[1]):
            push_it = True
        push_info+=ret[0]+"\n"
    print(push_info)
    if(push_it):
        push_server_jiang(exIP+"#barking!",push_info)

if __name__ == '__main__':
    exIP = "server_dog#"
    try:
        exIP += ':'+os.popen('curl ipconfig.io').read()
    except:
        pass
    while True:
        cf_list = [mems,cpus,disks,open_files,docker_info]
        check_loop(exIP,cf_list)
        time.sleep(120)
    #push_info,it = open_files()
    #push_server_jiang(exIP+"#barking!",push_info)
    # print(mems()[0])   # 内存
    # print(cpus()[0])   # CPU
    # print(disks()[0])  # 硬盘
    #print(docker_info())  # 登录用户
    # proces = process()
