# -*- coding:utf-8 -*-
import pandas
import os,tqdm
import Tool,numpy
pd=pandas.read_excel("C:\Users\lenovo\Desktop\yuce/20170630.xlsx")
array=[]
array.append(u'date')
for c in pd.columns:
    array.append(c.split("\r\n")[0])
walk=os.walk("C:\Users\lenovo\Desktop\yuce")
for x,y,z in walk:
    print z
o=0
for code in pd[u'证券代码'][3000:]:
    print 3000
    print code
    o=o+1
    print str(o)+"/"+str(len(pd[u'证券代码']))
    pd5=pandas.DataFrame(columns=array)
    #pd5.set_index('date')
    for file in tqdm.tqdm(z):
        pd1 = pandas.read_excel("C:\Users\lenovo\Desktop\yuce/"+str(file))
        array1 = [u'证券代码',u'证券名称',u'一致预测归属母公司净利润(FY1)',u'一致预测归属母公司净利润(FY2)',u'一致预测归属母公司净利润(FY3)',u'一致预测归属母公司净利润(未来12个月)',u'一致预测归属母公司净利润同比',u'一致预测归属母公司净利润2年复合增长率',u'一致预测归属母公司净利润1周变化率',u'一致预测归属母公司净利润4周变化率',u'一致预测归属母公司净利润13周变化率',u'一致预测归属母公司净利润26周变化率',u'一致预测每股收益(FY1)',u'一致预测每股收益(FY2)',u'一致预测每股收益(FY3)',u'一致预测每股收益(未来12个月)',u'一致预测ROE(FY1)',u'一致预测ROE(FY2)',u'一致预测ROE(FY3)',u'一致预测ROE(未来12个月)',u'一致预测ROE(同比)',u'一致预测总营业收入(FY1)',u'一致预测总营业收入(FY2)',u'一致预测总营业收入(FY3)',u'一致预测总营业收入(未来12个月)',u'一致预测总营业收入(同比)',u'一致预测总营业收入2年复合增长率',u'一致预测每股现金流(FY1)',u'一致预测每股股利(FY3)',u'一致预测每股现金流(FY3)',u'一致预测每股现金流(未来12个月)',u'一致预测每股股利(FY1)',u'一致预测每股股利(FY2)',u'一致预测每股股利(未来12个月)',u'一致预测每股净资产(FY1)',u'一致预测每股净资产(FY2)',u'一致预测每股净资产(FY3)',u'一致预测每股净资产(未来12个月)',u'一致预测息税前利润(FY1)',u'一致预测息税前利润(FY2)',u'一致预测息税前利润(FY3)',u'一致预测息税前利润(未来12个月)',u'一致预测息税折旧摊销前利润(FY1)',u'一致预测息税折旧摊销前利润(FY2)',u'一致预测息税折旧摊销前利润(FY3)',u'一致预测息税折旧摊销前利润(未来12个月)',u'一致预测营业利润(FY1)',u'一致预测营业利润(FY2)',u'一致预测营业利润(FY3)',u'一致预测营业利润(未来12个月)',u'一致预测营业利润同比',u'一致预测营业利润2年复合增长率']
        pd1.columns = array1
        num=0
        for y in pd1[u'证券代码']:
            num=num+1
            if y[:6] == code[:6]:
                pd2=pd1.loc[[num-1]]
                pd2.insert(0,"date",file)
                frames = [pd2, pd5]
                pd5 = pandas.concat(frames)
                break
    pd5 = pd5.replace(u"——", numpy.NaN)
    pd5.to_csv("C:\Users\lenovo\Desktop/11/" + code + ".csv", encoding='gbk')
    Tool.UpLoadToSQL(pd5, str(code[:6]), "_choice", 'fxsycsjdata')

