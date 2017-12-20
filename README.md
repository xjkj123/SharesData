```c

#include<windows.h>
#include<iostream.h>
// 定义两个线程函数Write()和Read()
// Read()、Write()函数分别使用VC++的P、V操作WaitForSingleObject()和ReleaseSemaphore()
DWORD WINAPI Write(LPVOID lpParameter);
DWORD WINAPI Read(LPVOID lpParameter);
// 缓冲区资源
unsigned char buffer;
// 两个信号量，分别使用缓冲区buffer的两个资源：满和空
// semaphore1 表示缓冲区buffer满，初始值为0，最大值为1
// semaphore2 表示缓冲区buffer空，初始值为1，最大值为1
HANDLE semaphore1;
HANDLE semaphore2;
//线程句柄
 HANDLE hThread1;
 HANDLE hThread2;
void main()
{  
	// buffer清空
	buffer=' ';
	// 创建信号量
	semaphore1=CreateSemaphore(NULL,0,1,NULL);
    semaphore2=CreateSemaphore(NULL,1,1,NULL);
	// 创建线程
    hThread1=CreateThread(NULL,0,Write,NULL,0,NULL);
    hThread2=CreateThread(NULL,0,Read,NULL,0,NULL);
	// 在子线程执行完前主线程不能退出，否则显示结果异常
	Sleep(10000);
	// 关闭句柄
    CloseHandle(Write);
    CloseHandle(Read);
	// 释放信号量
	CloseHandle(semaphore1);
	CloseHandle(semaphore2);
}
// 线程1对应的p函数实体：缓冲区buffer写操作
DWORD WINAPI Write(LPVOID lpParameter)
{
	unsigned char str[6]="Hello";
	int i=0;
    for (i=0;i<5;i++)
	{
		// 等待缓冲区空
		WaitForSingleObject( semaphore2, INFINITE );
		// 缓冲区空时，向缓冲区写入数据
		buffer=str[i];
		// 通知缓冲区满
		ReleaseSemaphore( semaphore1, 1, NULL );
	}
    return 0;
}
// 线程2对应的V函数实体：缓冲区buffer读操作
DWORD WINAPI Read(LPVOID lpParameter)
{
	int i=1;
	unsigned char c;
	for (i=1;i<=5;i++)
	{
		// 等待缓冲区满
		WaitForSingleObject( semaphore1, INFINITE);
		// 从缓存buffer获取数据
		c=buffer;
		// 输出从缓冲区buffer取出的数据
		cout<<c;
    	// 通知缓冲区空
		ReleaseSemaphore( semaphore2, 1, NULL );
	}
	// 回车换行
    cout<<endl;
    return 0;  
}


```



# SharesData
版本1.0.0
### 基于A股市场的数据获取拓展包
##### 量化公众号分享量化工具
![](https://github.com/xjkj123/SharesData/blob/master/qrcode.jpeg)
#### 引入包

```python
from ShareData import *
```

#### 获取个股开盘以来所有数据
```python
ShareClass().GetDayData(code='600000',start='1980-01-01',end="",zs=False)#股票代码#起始日期#结束日期#是否为指数代码
#获取股票代码600000的所有日线数据
#返回类型dataframe 
#date     日期               open       开盘价        close  收盘价           high  最高价      low  最低价
#QFQ_open 前复权开盘价        QFQ_close  前复权收盘价  QFQ_high 前复权最高价    QFQ_low  前复权最低价
#HFQ_open  后复权开盘价       HFQ_close  后复权收盘价  HFQ_high 后复权最高价    HFQ_low 后复权最低价 
#traded_market_value 流通市值 market_value  总市值    change 复杂收益率        volume 交易量 
```
#### 获取指数所有数据
```python
ShareClass().GetDayData(code='000001',start='1980-01-01',end="",zs=True)#指数代码#起始日期#结束日期#是否为指数代码
#获取指数代码000001的所有日线数据
#返回类型dataframe 
#date     日期      open       开盘价        close  收盘价           high  最高价      low  最低价
#volume 交易量      change 复杂收益率
```

#### 获取个股财务摘要

```python
ShareClass().GetCwzy("600000")#参数code为股票代码，两市上市股
#返回值为dataframe，从开市以来的所有财务摘要
#截止日期     #资产总计        #每股现金含量    #主营业务收入      #长期负债合计      #每股净资产
#净利润       #固定资产合计    #财务费用        #每股资本公积金    #流动资产合计      #每股收益

```


#### 获取个股资产负债数据

```python
ShareClass().GetZcfzb("600000")#参数code为股票代码，两市上市股
#返回值为dataframe，从开市以来的所有财务摘要
# 报表日期                          # 资产总计                     # 其他权益工具
# 资产                              # 负债                         # 其中：优先股
# 现金及存放中央银行款项            # 向中央银行借款               # 资本公积
# 存放同业款项                      # 同业存入及拆入               # 减:库藏股
# 拆出资金                          # 其中:同业存放款项             # 其他综合收益
# 贵金属                            # 拆入资金                     # 盈余公积
# 交易性金融资产                    # 衍生金融工具负债             # 未分配利润
# 衍生金融工具资产                  # 交易性金融负债               # 一般风险准备
# 买入返售金融资产                  # 卖出回购金融资产款           # 外币报表折算差额
# 应收利息                          # 客户存款(吸收存款)            # 其他储备
# 发放贷款及垫款                    # 应付职工薪酬                 # 归属于母公司股东的权益
# 代理业务资产                      # 应交税费                     # 少数股东权益
# 可供出售金融资产                  # 应付利息                     # 股东权益合计
# 持有至到期投资                    # 应付账款                     # 负债及股东权益总计
# 长期股权投资                      # 代理业务负债      
# 应收投资款项                      # 应付债券    
# 固定资产合计                      # 递延所得税负债     
# 无形资产                          # 预计负债    
# 商誉                              # 其他负债    
# 递延税款借项                      # 负债合计    
# 投资性房地产                      # 所有者权益       
# 其他资产                          # 股本      
```




#### 获取利润表

```python
ShareClass().GetLrb("600000")#参数code为股票代码，两市上市股
#返回值为dataframe，从开市以来的所有财务摘要

# 报表日期                   # 其中:对联营公司的投资收益            # 减:营业外支出  
# 一、营业收入               # 公允价值变动净收益                  # 四、利润总额   
# 利息净收入                 # 其他业务收入                        # 减:所得税    
# 其中：利息收入             # 二、营业支出                        # 五、净利润    
# 减：利息支出               # 营业税金及附加                      # 归属于母公司的净利润   
# 手续费及佣金净收入         # 业务及管理费用                      # 少数股东权益   
# 其中:手续费及佣金收入       # 资产减值损失                        # 六、每股收益   
# 减：手续费及佣金支出       # 其他业务支出                        # 基本每股收益(元 / 股)    
# 汇兑收益                   # 三、营业利润                        # 稀释每股收益(元 / 股)    
# 投资净收益                 # 加:营业外收入                        # 七、其他综合收益 
# 八、综合收益总额           # 归属于母公司所有者的综合收益总额    # 归属于少数股东的综合收益总额   

```

# 未完待续
