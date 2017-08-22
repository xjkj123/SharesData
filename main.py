# -*- coding: utf-8 -*-
import threading
from tqdm import tqdm
from ShareData import *
def ChildThead(code):
    try:
        pd = desc(code).Rstr()
        if not pd.empty:
            pd.to_csv('C:\Users\lenovo\Desktop\SharesData/11/' + code + '.csv')
    except:
        c=open('error.txt','a')
        c.write(code+'beta\n')
        c.close()

    # try:
    #     pd = xx(code)
    #     pd.to_csv('C:\Users\lenovo\Desktop\SharesData/11/'+code+'.csv')
    # except:
    #     print 'error'+code
def UpDataShare():
    thread = []
    MaxThread = 3
    num=0
    code = Tools().GetShareCode()
    for x in code:
        y = threading.Thread(target=ChildThead, args=(x,))
        thread.append(y)
    try:
        for t in tqdm(thread):
            t.start()
            while True:
                time.sleep(0.05)
                if len(threading.enumerate()) < MaxThread:
                    if len(code) - num < 13:
                        t.join()
                    num = num + 1
                    break
    except:
        print "1223"
def xx(code):
    pd1 = desc(code, sql=True).Cmra()
    pd = desc(code, sql=True).Beta()
    pd1 = pandas.merge(pd1, pd, how='inner', on='date')
    print 1
    pd = desc(code, sql=True).Rstr()
    pd1 = pandas.merge(pd1, pd, how='inner', on='date')
    print 2
    pd = desc(code, sql=True).Incap()
    pd1 = pandas.merge(pd1, pd, how='inner', on='date')
    print 3
    pd = desc(code, sql=True).Eplbs()
    pd1 = pandas.merge(pd1, pd, how='inner', on='date')
    print 4
    pd = desc(code, sql=True).Cetop()
    pd1 = pandas.merge(pd1, pd, how='inner', on='date')
    print 5
    pd = desc(code, sql=True).Dastd()
    pd1 = pandas.merge(pd1, pd, how='inner', on='date')

    return pd1
if __name__ == '__main__':
    #print desc('600000',sql=True).Rstr()
    print desc('600000',sql=True).Beta()

    # pd=ShareClass().GetDayData('002088')
    # Tools().UpLoadToSQL(pd, '002088', "_tencent", "daydata")

    #
# UpDataShare()
    # for x in tqdm(ShareClass().GetZS()):
    #     pd= ShareClass().GetDayData(x, zs=True)
    #     Tools().UpLoadToSQL(pd,x,"_tencent",'zsdata',False)


    #pd = desc().Beta("600000","_tencent","000001")
    #pd.to_csv('betanowg.csv')
    #
    # PD=ShareClass().GetDayData("002088")
    # Tool.UpLoadToSQL(PD,"002088",'_tencent',"daydata")

        #re.findall(r'http://stock.jrj.com.cn/share(.+?)shtml',Tools().smartCode(ret.read()))



