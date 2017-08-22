# -*- coding: utf-8 -*-
import pandas,time,urllib,re,requests,numpy,math,chardet,config
from tushare import get_k_data
from pandas.compat import StringIO
from sqlalchemy import create_engine
from sklearn import linear_model
from bs4 import *
class Tools():
    def __init__(self):
        time.sleep(0)
    def smartCode(self,item):
        codedetect = chardet.detect(item)["encoding"]
        try:
            item = unicode(item, codedetect)
            return item.encode("utf-8")
        except:
            item = unicode(item, 'gbk')
            return item.encode("utf-8")
    def ReadSqlData(self,name, db):
        conn = create_engine(
            'mysql://' + config.user + ':' + config.password + '@' + config.ip + '/' + db + '?charset=utf8')

        x = 'select * from ' + name + ';'  # sql与语句
        return pandas.read_sql(x, con=conn)
    def GetShareCode(self):
        ret=urllib.urlopen('http://file.tushare.org/tsdata/all.csv')
        df=pandas.read_csv(StringIO(ret.read()),encoding='gbk',dtype={'code':'object'})
        return df['code']
    def IntOnly(self,str):
        int = filter(lambda ch: ch in '0123456789', str)
        return int
    def UpLoadToSQL(self,framework, code, postfix, db, firstfix=True):
        if firstfix:
            if int(code[0]) is 0 or 3:
                name = "sz" + code + postfix
            if int(code[0]) is 6:
                name = "sh" + code + postfix
        else:
            name = code + postfix

        framework.to_sql(name, create_engine(
            'mysql://' + config.user + ':' + config.password + '@' + config.ip + '/' + db + '?charset=utf8'),
                         index=False, if_exists='replace')
    def DownLoadDataToCsv(self,framework, path):
        framework.to_csv(path, encoding="gbk")
    def downloadrequests(self,url, token, path):
        head = {'Authorization': 'Bearer ' + token}
        ret = requests.get(url=url, headers=head)

        total_size = int(ret.headers['Content-Length'])
        with open(path, 'wb') as of:
            for chunk in ret.iter_content(chunk_size=102400):
                if chunk:
                    of.write(chunk)
class ShareClass():
    def __init__(self):
        time.sleep(0)
    def GetDayData(self,code,start='1980-01-01',end="",zs=False):#日线数据，带除权，带权
        if zs :
            Bfq = get_k_data(code, start=start, end=end, ktype="d", autype=None)
            change=[]
            for x in Bfq['close']:
                try:
                    change.append(math.log(float(x) / before, math.e))
                except:
                    change.append(numpy.NaN)
                before = x
            del Bfq['code']
            Bfq['change']=change
            return Bfq
        else:
            Qfq = get_k_data(code, start=start, end=end, ktype="d", autype="qfq")
            Bfq = get_k_data(code, start=start, end=end, ktype="d", autype=None)
            Hfq = get_k_data(code, start=start, end=end, ktype="d", autype='hfq')
            Bfq['QFQ_open'] = Qfq['open']
            Bfq['QFQ_close'] = Qfq['close']
            Bfq['QFQ_high'] = Qfq['high']
            Bfq['QFQ_low'] = Qfq['low']
            Bfq['HFQ_open'] = Hfq['open']
            Bfq['HFQ_close'] = Hfq['close']
            Bfq['HFQ_high'] = Hfq['high']
            Bfq['HFQ_low'] = Hfq['low']
            if not Qfq is None:
                del Bfq['code']
                dfgb = ShareClass().GetGuben(code)
                dfgb.sort_index()
                dfgp = Bfq
                dfgp.sort_index()
                guben = []
                liutongguben = []
                change = []
                n = 0
                nan = 0
                before = 0
                for x in dfgp['date']:
                    try:

                        guben.append(float(dfgb[dfgb.index <= x].iloc[-1, 12:13]) * dfgp.loc[n, 'close'])

                    except:
                        guben.append(numpy.NaN)
                    try:
                        liutongguben.append(float(dfgb[dfgb.index <= x].iloc[-1, 14:15]) * dfgp.loc[n, 'close'])
                    except:
                        liutongguben.append(numpy.NaN)
                        nan = nan + 1
                    n = n + 1
                for x in dfgp['HFQ_close']:
                    change.append(math.log(x / before, math.e))

                    before = x
                dfgp["traded_market_value"] = liutongguben
                dfgp["market_value"] = guben
                dfgp["change"] = change
                # print dfgp[nan:]
                return dfgp[nan + 1:]
    def GetCwzy(self,code):     #财务摘要表
        ret = urllib.urlopen("http://money.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/"+code+".phtml")
        soup = BeautifulSoup(Tools().smartCode(ret.read()), "html.parser")
        y = soup.find(id="FundHoldSharesTable")
        thestar = True
        dict = {}
        jzrq = ""
        mgjzc = ""
        mgsy = "1"
        mgxjhl = "1"
        mgzbgjj = "1"
        gdzchj = "1"
        ldzchj = "1"
        zczj = "1"
        cqfzhj = "1"
        zyywsr = "1"
        cwfy = "1"
        for w in y.find_all("tr"):
            if u"截止日期" in w.get_text() and thestar == True:
                data = w.get_text().split("\n")
                jzrq = data[2]
                thestar = False
            if u"每股净资产" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                mgjzc = data[2]
                mgjzc = mgjzc.split(u'元')[0]
            if u"每股收益" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                mgsy = data[2]
                mgsy = mgsy.split(u'元')[0]
            if u"每股现金含量" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                mgxjhl = data[2]
                mgxjhl = mgxjhl.split(u'元')[0]
            if u"每股资本公积金" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                mgzbgjj = data[2]
                mgzbgjj = mgzbgjj.split(u'元')[0]
            if u"固定资产合计" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                gdzchj = data[2]
                gdzchj = gdzchj.split(u'元')[0]
            if u"流动资产合计" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                ldzchj = data[2]
                ldzchj = ldzchj.split(u'元')[0]
            if u"资产总计" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                zczj = data[2]
                zczj = zczj.split(u'元')[0]
            if u"长期负债合计" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                cqfzhj = data[2]
                cqfzhj = cqfzhj.split(u'元')[0]
            if u"主营业务收入" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                zyywsr = data[2]
                zyywsr = zyywsr.split(u'元')[0]
            if u"财务费用" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                cwfy = data[2]
                cwfy = cwfy.split(u'元')[0]
            if u"净利润" in w.get_text() and thestar == False:
                data = w.get_text().split("\n")
                jlr = data[2]
                jlr = jlr.split(u'元')[0]
                dict.update({jzrq: {u"截止日期".encode('gbk', 'ignore').decode('gbk'):jzrq.encode('gbk', 'ignore').decode('gbk'),
                                    u"每股净资产".encode('gbk', 'ignore').decode('gbk'): mgjzc.encode('gbk', 'ignore').decode('gbk'),
                                    u"每股收益".encode('gbk', 'ignore').decode('gbk'): mgsy.encode('gbk', 'ignore').decode('gbk'),
                                    u"每股现金含量".encode('gbk', 'ignore').decode('gbk'): mgxjhl.encode('gbk', 'ignore').decode('gbk'),
                                    u"每股资本公积金".encode('gbk', 'ignore').decode('gbk'): mgzbgjj.encode('gbk', 'ignore').decode('gbk'),
                                    u"固定资产合计".encode('gbk', 'ignore').decode('gbk'): gdzchj.encode('gbk', 'ignore').decode('gbk'),
                                    u"流动资产合计".encode('gbk', 'ignore').decode('gbk'): ldzchj.encode('gbk', 'ignore').decode('gbk'),
                                    u"资产总计".encode('gbk', 'ignore').decode('gbk'): zczj.encode('gbk', 'ignore').decode('gbk'),
                                    u"长期负债合计".encode('gbk', 'ignore').decode('gbk'): cqfzhj.encode('gbk', 'ignore').decode('gbk'),
                                    u"主营业务收入".encode('gbk', 'ignore').decode('gbk'): zyywsr.encode('gbk', 'ignore').decode('gbk'),
                                    u"财务费用".encode('gbk', 'ignore').decode('gbk'): cwfy.encode('gbk', 'ignore').decode('gbk'),
                                    u"净利润".encode('gbk', 'ignore').decode('gbk'): jlr.encode('gbk', 'ignore').decode('gbk')
                                    }})
                thestar = True
        pd = pandas.DataFrame.from_dict(dict, orient="index")
        return pd
    def GetZcfzb(self,code):#资产负债表
        url="http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/"+code+"/ctrl/all.phtml"
        ret=urllib.urlopen(url)
        pd=pandas.read_table(StringIO(ret.read()),encoding="gb2312").set_index(u'报表日期').transpose()
        pd.insert(0,u"报表日期",pd.index)
        del pd[u"单位"]
        return pd
    def GetLrb(self,code):#利润表
        url="http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/"+code+"/ctrl/all.phtml"
        ret=urllib.urlopen(url)
        pd=pandas.read_table(StringIO(ret.read()),encoding="gb2312").set_index(u'报表日期').transpose()
        pd.insert(0,u"报表日期",pd.index)
        del pd[u"单位"]
        return pd
    def GetXjllb(self,code):#现金流量表
        try:
            url = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/" + code + "/ctrl/all.phtml"
            ret=urllib.urlopen(url)
            pd = pandas.read_table(StringIO(ret.read()), encoding="gb2312").set_index(u'报表日期').transpose()
            pd.insert(0, u"报表日期", pd.index)
            del pd[u"单位"]
            return pd
        except:
            return None
    def GetFh(self,code):#获取配股分红
        try:
            ret = urllib.urlopen("http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/" + code + ".phtml")
            soup = BeautifulSoup(Tools().smartCode(ret.read()), "html.parser")
            dict = {}
            for x in soup.find_all('tbody'):
                for e in str(x).split('_blank'):
                    if "type=1" in e:
                        td = re.findall(r'<td>(.+?)</td>', e)
                        dict.update({td[0]: {u"公告日期".encode('gbk', 'ignore').decode('gbk'): td[0],
                                               u"送股".encode('gbk', 'ignore').decode('gbk'): td[1],
                                               u"转增".encode('gbk', 'ignore').decode('gbk'): td[2],
                                               u"派息".encode('gbk', 'ignore').decode('gbk'): td[3],
                                               u"进度".encode('gbk', 'ignore').decode('gbk'): td[4],
                                               u"除权除息日".encode('gbk', 'ignore').decode('gbk'): td[5],
                                               u"股权登记日".encode('gbk', 'ignore').decode('gbk'): td[6],
                                               u"红股上市日".encode('gbk', 'ignore').decode('gbk'): td[7]
                                               }})
            return pandas.DataFrame.from_dict(dict, orient="index")
        except:
            return None
    def GetPg(self,code):#获取配股分红
        try:
            ret = urllib.urlopen("http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/" + code + ".phtml")
            soup = BeautifulSoup(Tools().smartCode(ret.read()), "html.parser")
            dict = {}
            for x in soup.find_all('tbody'):
                for e in str(x).split('_blank'):
                    if "type=2" in e:
                        td = re.findall(r'<td>(.+?)</td>', e)
                        dict.update({td[0]: {u"公告日期".encode('gbk', 'ignore').decode('gbk'): td[0],
                                               u"配股方案".encode('gbk', 'ignore').decode('gbk'): td[1],
                                               u"配股价格".encode('gbk', 'ignore').decode('gbk'): td[2],
                                               u"基准股本".encode('gbk', 'ignore').decode('gbk'): td[3],
                                               u"除权日".encode('gbk', 'ignore').decode('gbk'): td[4],
                                               u"股权登记日".encode('gbk', 'ignore').decode('gbk'): td[5],
                                               u"缴款起始日".encode('gbk', 'ignore').decode('gbk'): td[6],
                                               u"缴款终止日".encode('gbk', 'ignore').decode('gbk'): td[7],
                                               u"配股上市日".encode('gbk', 'ignore').decode('gbk'): td[8],
                                               }})
            return pandas.DataFrame.from_dict(dict, orient="index")
        except:
            return None
    def GetGudong(self, code):
        ret = urllib.urlopen(
            "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockHolder/stockid/" + code + ".phtml")
        soup = BeautifulSoup(Tools().smartCode(ret.read()), "html.parser")
        catch = soup.find('tbody')
        y = str(catch).split("begin")
        num = 0
        numq = 0
        dict = {}
        for xiangmu in y:
            if len(xiangmu) > 200:
                jzrq = re.findall(r'截至日期</strong></div></td>\n<td colspan="4">(.+?)</td>', xiangmu)
                ggrq = re.findall(r'公告日期</strong></div></td>\n<td colspan="4">(.+?)</td>', xiangmu)
                gdzs = re.findall(r'股东总数</strong></div></td>\n<td colspan="4">(.+?)<a href=', xiangmu)
                pjcgs = re.findall(r'\t\t\t\t\t(.+?)股', xiangmu)
                if len(gdzs) is 0:
                    gdzs.append(0)
                if len(pjcgs) is 0:
                    pjcgs.append(0)
                if len(ggrq) is 0:
                    ggrq.append(0)
                soup = BeautifulSoup(xiangmu, 'html.parser')
                e = soup.find_all('tr')
                num = num + 1
                if num == 1:
                    s = 6
                else:
                    s = 7
                for t in range(s, len(e)):
                    soup1 = BeautifulSoup(str(e[t]), 'html.parser')
                    gudong = []
                    for i in soup1.find_all("td"):
                        if i.string is None:
                            rew = re.findall(r'_blank">(.+?)</a>', str(i))
                            if len(rew) == 0:
                                rew = re.findall(r'"center">(.+?)<font style', str(i))
                            gudong.append(rew[0])
                        else:
                            gudong.append(i.string)
                    numq = numq + 1
                    dict.update({numq: {
                        u"截止日期".encode('gbk', 'ignore').decode('gbk'): jzrq[0],
                        u"公告日期".encode('gbk', 'ignore').decode('gbk'): ggrq[0],
                        u"股东总数".encode('gbk', 'ignore').decode('gbk'): gdzs[0],
                        u"平均持股数".encode('gbk', 'ignore').decode('gbk'): pjcgs[0],
                        u"股东名称".encode('gbk', 'ignore').decode('gbk'): gudong[1].encode('gbk', 'ignore').decode('gbk'),
                        u"持股数量".encode('gbk', 'ignore').decode('gbk'): gudong[2].encode('gbk', 'ignore').decode('gbk'),
                        u"持股比例".encode('gbk', 'ignore').decode('gbk'): gudong[3].encode('gbk', 'ignore').decode('gbk'),
                        u"股本性质".encode('gbk', 'ignore').decode('gbk'): gudong[4].encode('gbk', 'ignore').decode('gbk')
                    }})
        return pandas.DataFrame.from_dict(dict, orient="index")
    def GetGuben(self,code):
        url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/"+code+".phtml"
        ret = requests.get(url)
        ret.encoding = "GBK"
        x = BeautifulSoup(ret.text, "html.parser")
        dict = {}
        num=-1
        for y in x.find_all(id="con02-1"):
            array = []
            for z in y.find_all("tr"):
                data = z.find_all("td")
                if not len(data) is 0 :
                    if not data[0].string is None and u"股本结构图" in data[0].string:
                        time.sleep(0)
                    else:
                        array[num].append(data)

                else:
                    array.append([])
                    num=num+1
        for x in array:
            h=len(x[0])

            for y in range(1,h):
                h=len(x[y])
                if x[2][y].string is None:

                    ltg=numpy.NaN
                else:
                    ltg=x[2][y].string.encode('gbk', 'ignore').decode('gbk')

                zgb=float(x[3][y].string.split(" ")[0])*10000
                try:
                    ltag=float(x[5][y].string.split(" ")[0])*10000
                except:
                    ltag=numpy.NaN

                dict.update({x[0][y].string:{
                    u'变动日期'.encode('gbk', 'ignore').decode('gbk'): x[0][y].string,
                    u'公告日期'.encode('gbk', 'ignore').decode('gbk'): x[1][y].string,
                    u'变动原因'.encode('gbk', 'ignore').decode('gbk'): ltg,
                    u'总股本'.encode('gbk', 'ignore').decode('gbk'): zgb,
                    u'流通股'.encode('gbk', 'ignore').decode('gbk'): x[4][y].string,
                    u'流通A股'.encode('gbk', 'ignore').decode('gbk'): ltag,
                    u'高管股'.encode('gbk', 'ignore').decode('gbk'): x[6][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'限售A股'.encode('gbk', 'ignore').decode('gbk'): x[7][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'流通B股'.encode('gbk', 'ignore').decode('gbk'): x[8][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'限售B股'.encode('gbk', 'ignore').decode('gbk'): x[9][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'流通H股'.encode('gbk', 'ignore').decode('gbk'): x[10][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'国家股'.encode('gbk', 'ignore').decode('gbk'): x[11][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'国有法人股'.encode('gbk', 'ignore').decode('gbk'): x[12][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'境内法人股'.encode('gbk', 'ignore').decode('gbk'): x[13][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'境内发起人股'.encode('gbk', 'ignore').decode('gbk'): x[14][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'募集法人股'.encode('gbk', 'ignore').decode('gbk'): x[15][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'一般法人股'.encode('gbk', 'ignore').decode('gbk'): x[16][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'战略投资者持股'.encode('gbk', 'ignore').decode('gbk'): x[17][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'基金持股'.encode('gbk', 'ignore').decode('gbk'): x[18][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'转配股'.encode('gbk', 'ignore').decode('gbk'): x[19][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'内部职工股'.encode('gbk', 'ignore').decode('gbk'): x[20][y].string.encode('gbk', 'ignore').decode('gbk'),
                    u'优先股'.encode('gbk', 'ignore').decode('gbk'): x[21][y].string.encode('gbk', 'ignore').decode('gbk')
                }})

        df= pandas.DataFrame.from_dict(dict).transpose()
        return df
    def GetZS(self):
        dict = {}
        for x in range(1, 13):
            ret = urllib.urlopen('http://q.jrjimg.cn/?q=cn|i&c=m&n=hqa&o=code,d&p=' + str(x) + '050&_dc=1502180002469')
            import json
            json1 = Tools().smartCode(ret.read())
            for x in json1[8:len(json1) - 2].split('[\n[')[1].split("],\n["):
                dict.update({x.split(""",""")[0][1:-1]: x.split(""",""")[2][1:-1]})
        return dict
class desc():
    def __init__(self,code,sql=False):
        if int(code[0]) is 0 or 3:
            name = "sz" + code
        if int(code[0]) is 6:
            name = "sh" + code

        if sql:
            self.sharedf=ShareClass().GetDayData(code)
        else:
            conn = create_engine(
                'mysql://' + config.user + ':' + config.password + '@' + config.ip + '/daydata?charset=utf8')

            x = 'select * from ' + name + '_tencent;'  # sql与语句
            self.sharedf = pandas.read_sql(x, con=conn)


        self.name=name
    def Beta(self):
        prixe = math.log(0.03637 / float(365) + 1)
        df1 = self.sharedf
        df1['change']=df1['change']-prixe
        df2 = ShareClass().GetDayData(code='000001',zs=True)
        print 11111111111
        coef = []
        intercept = []
        residues=[]
        ret= pandas.merge(df1,df2,how='inner',on='date')
        array2 = []
        if len(ret) > 252:
            for z in range(0, 252):
                array2.append(math.pow(math.pow(float(1) / 2, float(1 / float(63))), (252 - z - 1)))
            for z in range(0, 251):
                coef.append(numpy.NaN)
                intercept.append(numpy.NaN)
                residues.append(numpy.NaN)
            for c in range(252, len(ret)+1):
                array=[]
                for x in ret[c - 252:c]['change_x']:
                    array.append([x])
                clf = linear_model.LinearRegression()
                clf.fit(X=array, y=ret[c - 252:c]["change_y"], sample_weight=array2)
                coef.append(float(clf.coef_))
                residues.append(clf._residues)
                intercept.append(float(clf.intercept_))
            ret['beta'] = coef
            ret['alpha'] = intercept
            ret['residues'] = residues
            return ret[['date','beta','alpha','residues']]
    def Rstr(self):
        array2=[]
        prixe = math.log(0.03637 / float(252) + 1)
        ret = self.sharedf
        ret['change']=ret['change']-prixe
        rstr = []
        print 1
        if len(ret) > 525:
            for z in range(0, 504):
                array2.append(math.pow(math.pow(float(1) / 2, float(1 / float(126))), (503 - z)))

            for h in  range(0,525):
                rstr.append(numpy.NaN)

            for c in range(525, len(ret)):
                rett=0
                for f in range(0,len(duan)-21):
                    rett=rett+duan.iloc[f, 16]*array2[f]
                rstr.append(rett)

            print rstr
            ret['rstr'] = rstr
            return ret[['date','rstr']]
    def Incap(self):
        df1 = self.sharedf
        incap=[]
        for x in df1['market_value']:
            incap.append(math.log(x,math.e))
        df1['incap'] = incap
        return df1[['date','incap']]
    def Eplbs(self):
        dffxs= Tools().ReadSqlData(self.name+"_choice","fxsycsjdata")
        dffxs=dffxs.replace(0,numpy.NaN)
        eplbs=[]
        dfgg= self.sharedf
        for x in range(0,len(dffxs)):
            dffxs.loc[x,'date']=int(str(dffxs.loc[x,'date'])[0:8])
        for y in range(0,len(dfgg)):
            try:
                eplbss = float(dffxs.loc[dffxs['date'] < int(str(dfgg.loc[y, 'date']).replace("-", ""))].iloc[1, 6:7])/float(dfgg.loc[y, 'traded_market_value'])
                eplbs.append(eplbss)
            except:
                eplbs.append(numpy.NaN)
        dfgg['eplbs']=eplbs
        return dfgg[['date','eplbs']]
    def Etop(self):
        dict={}
        dict2={}
        dflrb = Tools().ReadSqlData(self.name + "_sina", "lrbdata")
        dfgg = self.sharedf
        dfgg=dfgg.sort_index(ascending=True)
        print dfgg
        etop=[]
        for x in range(0,len(dflrb[u'报表日期'])):
            try:
                jlr=dflrb.loc[x, u'归属于母公司的净利润']
            except:
                jlr=dflrb.loc[x, u'归属于母公司所有者的净利润']
            if dflrb.loc[x,u'报表日期'][:4] in dict:
                dict[dflrb.loc[x,u'报表日期'][:4]].update({
                    dflrb.loc[x, u'报表日期'][4:]:jlr
                })
            else:
                dict.update({dflrb.loc[x,u'报表日期'][:4]:{
                    dflrb.loc[x, u'报表日期'][4:]: jlr
                }})
        for x in sorted(dict.keys()):
            quankong=False
            try:
                yijidu = float(dict[x]['0331'])
                erjidu = float(dict[x]['0630']) - float(dict[x]['0331'])

                sijidu = float(dict[x]['1231']) - float(dict[x]['0930'])
            except:
                try:
                    yijidu = float(dict[x]['1231']) / 4
                    erjidu = float(dict[x]['1231']) / 4
                    sanjidu = float(dict[x]['1231']) / 4
                    sijidu = float(dict[x]['1231']) / 4
                except:
                    try:
                        yijidu = float(dict[x]['0331'])
                        erjidu = float(dict[x]['0630']) - float(dict[x]['0331'])
                        sanjidu = numpy.NaN
                        sijidu = numpy.NaN
                    except:
                        try:
                            yijidu = float(dict[x]['0331'])
                            erjidu = float(dict[x]['0630']) - float(dict[x]['0331'])
                            sanjidu = float(dict[x]['0930']) - float(dict[x]['0630'])
                            sijidu = numpy.NaN
                        except:
                            try:
                                yijidu = float(dict[x]['0331'])
                                erjidu = numpy.NaN
                                sanjidu = numpy.NaN
                                sijidu = numpy.NaN
                            except:
                                quankong = True
                                yijidu = numpy.NaN
                                erjidu = numpy.NaN
                                sanjidu = numpy.NaN
                                sijidu = numpy.NaN
            if not quankong:
                if x in dict2:
                    dict2[x].update({"s1": yijidu,
                                     "s2": erjidu,
                                     "s3": sanjidu,
                                     "s4": sijidu
                                     })
                else:
                    dict2.update({x: {
                        "s1": yijidu,
                        "s2": erjidu,
                        "s3": sanjidu,
                        "s4": sijidu
                    }})
            quankong = False
        num=1
        print etop

        for x in dfgg['date']:
            if int(x[5:7]+x[8:10])<430:
                etop.append((float(dict2[str(int(x[0:4])-1)]["s1"])+float(dict2[str(int(x[0:4])-1)]["s2"])+float(dict2[str(int(x[0:4])-1)]["s3"])+float(dict2[str(int(x[0:4])-2)]["s4"]))/dfgg.loc[num,u'traded_market_value'])
            if int(x[5:7]+x[8:10])>=430 and int(x[5:7]+x[8:10])<830:
                etop.append((float(dict2[str(int(x[0:4]) - 1)]["s2"])+float(dict2[str(int(x[0:4]) - 1)]["s3"])+float(dict2[str(int(x[0:4]) - 1)]["s4"])+float(dict2[str(int(x[0:4]))]["s1"]))/dfgg.loc[num,u'traded_market_value'])
            if int(x[5:7]+x[8:10])>=830 and int(x[5:7]+x[8:10])<1031:
                etop.append((float(dict2[str(int(x[0:4]) - 1)]["s3"]) + float(dict2[str(int(x[0:4]) - 1)]["s4"]) + float(dict2[str(int(x[0:4]))]["s1"]) + float(dict2[str(int(x[0:4]))]["s2"]))/dfgg.loc[num,u'traded_market_value'])
            if int(x[5:7]+x[8:10])>=1031:
                etop.append((float(dict2[str(int(x[0:4]) - 1)]["s4"]) + float(dict2[str(int(x[0:4]))]["s1"]) + float(dict2[str(int(x[0:4]))]["s2"])+ float(dict2[str(int(x[0:4]))]["s3"]))/dfgg.loc[num,u'traded_market_value'])
            num=num+1
        dfgg['etop']=etop                                                                                        #
        return dfgg[['date','etop']]
    def Cetop(self):
        tdate=[]
        Cetop=[]
        dfxjllb = Tools().ReadSqlData(self.name+"_sina", "xjllbdata")
        dfgg = self.sharedf
        for x in range(0,len(dfxjllb.index)):
            if dfxjllb.loc[x,u'报表日期'][4:] == "0331":
                tdate.append(int(dfxjllb.loc[x, u'报表日期'][:4]+"0430"))
            else:
                if dfxjllb.loc[x, u'报表日期'][4:] == "0630":
                    tdate.append(int(dfxjllb.loc[x, u'报表日期'][:4] + "0831"))
                else:
                    if dfxjllb.loc[x, u'报表日期'][4:] == "0930":
                        tdate.append(int(dfxjllb.loc[x, u'报表日期'][:4] + "1031"))
                    else:
                        if dfxjllb.loc[x, u'报表日期'][4:] == "1231":
                            tdate.append(int(str(int(dfxjllb.loc[x, u'报表日期'][:4]) + 1) + "0430"))
                        else:
                            tdate.append(numpy.NaN)
        dfxjllb['tdate']=tdate
        for x in range(1,len(dfgg.index)+1):
            Cetop.append(float(dfxjllb[dfxjllb[u'tdate']<int(str(dfgg.loc[x,u'date']).replace('-',''))].iloc[0,15:16])/dfgg.loc[x,u'traded_market_value'])
        dfgg['Cetop']=Cetop                                                                                        #
        return dfgg[['date','Cetop']]
    def Dastd(self):
        dastd=[]
        for x in range(0,251):
            dastd.append(numpy.NaN)
        dfgg = self.sharedf
        weight=[]
        all=0
        num=0
        for x in range(0,252):
            weight.append(math.pow(math.pow(float(1) / 2, float(1 / float(63))), (252 - x - 1)))
            all=all+math.pow(math.pow(float(1) / 2, float(1 / float(63))), (252 - x - 1))
        for x in range(252,len(dfgg['change'])+1):
            dd=0
            mean=dfgg['change'][x-252:x].mean()
            for y in dfgg['change'][x-252:x]:
                dd= dd+math.sqrt(math.pow((y-mean),2)*weight[num]/all)
                num=num+1
            dastd.append(dd)
            num=0
        dfgg['dastd'] = dastd
        return dfgg[['date','dastd']]
    def Cmra(self):
        df=self.sharedf
        cc=[]
        cmra=[]
        prixe=math.log(0.03637/float(12)+1)
        df=df.set_index('date')
        df1=df['change']
        for x in range(20,len(df1.index)+1):
            cc.append(df1[x-20:x].sum()-prixe)
        dd=[]
        for x in range(12,len(cc)+1):
            dd.append(sum(cc[x-12:x]))
        for x in range(252,len(dd)+1):
            cmra.append(max(cc[x-252:x])-min(cc[x-252:x]))
        df=df[281:]
        df['cmra']=cmra
        df['date']=df.index
        df=pandas.DataFrame(df.reset_index(drop=True))
        return df[['date','cmra']]




