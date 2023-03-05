import time
from getData import GetDataFromMysql
from datetime import datetime, timedelta
import playsound

class Shot:
    def __init__(self):
        self.Shaba = GetDataFromMysql('shaba')
        self.Manbetx = GetDataFromMysql('manbetx')
        self.num = 0

    def data_is_new(self, data):
        # 创建一个datetime对象
        dt = datetime.now()
        # 创建一个时间差对象，表示要减去5秒
        delta = timedelta(seconds=10)
        # 减去时间差
        new_dt = dt - delta

        if data['TIME'] > new_dt:
            #print('data time 是最新数据')
            return True
        else:
            # print('数据需要重新刷新！！！')
            return False

    def print_data_is_new(self, data_manbetx, data_shaba):
        try:
            if self.data_is_new(data_manbetx) and self.data_is_new(data_shaba):
                self.num += 1
                # print(self.num)
                if self.num % 500 == 0:
                    print(datetime.now(), 'ManBetX 数据获取正常，shaba 数据获取正常')
        except:
            print('print_data_is_new')

    def time_is_match(self, data_manbetx, data_shaba):
        # print(data_manbetx['GAMETIME'], data_shaba['GAMETIME'])
        # print(data_manbetx)
        # print(data_shaba)
        if data_manbetx['GAMETIME'] == None or data_shaba['GAMETIME'] == None:
            print(data_manbetx['GAMETIME'], data_shaba['GAMETIME'])
            return False
        time_list_manbetx = data_manbetx['GAMETIME'].split(':')
        time_list_shaba = data_shaba['GAMETIME'].split(':')
        if float(time_list_manbetx[0]) == 0 and float(time_list_manbetx[1]) == 0:
            return False
        if float(time_list_shaba[0]) == 0 and float(time_list_shaba[1]) == 0:
            return False
        if float(time_list_manbetx[0]) == float(time_list_shaba[0]):
            print(data_manbetx['GAMETIME'], data_shaba['GAMETIME'])
            return True

    def has_shot(self, data_manbetx, data_shaba):
        try:
            if self.time_is_match(data_manbetx, data_shaba):
                if data_manbetx['BIGSMALL'] >= data_shaba['BIGSMALL'] + 3 or data_manbetx['BIGSMALL'] <= data_shaba['BIGSMALL'] - 3:
                    playsound.playsound('Alarm01.wav')
                    print("机会出现！！！！")
                    print('双方主队名称为：', data_manbetx['HOST'], data_shaba['HOST'])
                    print("让球数分别是ManBetX：", data_manbetx['BIGSMALL'], "shaba：", data_shaba['BIGSMALL'])
                    print(data_manbetx)
                    print(data_shaba)
                    return True
                else:
                    return False
            else:
                return False
        except:
            print('has_shot出错')

    def run(self):
        try:
            data_manbetx = self.Manbetx.get_data()
            data_shaba = self.Shaba.get_data()
            #print(data_manbetx[0])
            #print(data_shaba[0])
            # 判断数据是否是最近五秒内的
            for manbetx in data_manbetx:
                if self.data_is_new(manbetx):
                    for shaba in data_shaba:
                        if self.data_is_new(shaba):
                            self.print_data_is_new(manbetx, shaba)
                            # 根据比分判断是否是同一场比赛
                            if manbetx['HOSTSCORE'] == shaba['HOSTSCORE'] and manbetx['GUESTSCORE'] == shaba['GUESTSCORE'] :
                                if manbetx['HOSTSCORE'] != 0 or manbetx['GUESTSCORE'] != 0:
                                    #print('双方主队名称为：', manbetx['HOST'], shaba['HOST'])
                                    # 判断是否存在套利机会
                                    self.has_shot(manbetx, shaba)
        except:
            print('--------------------')




if __name__ == '__main__':
    shot = Shot()
    while True:
        try:
            shot.run()
            time.sleep(3)
        except:
            print('出错')