```c
#include "stdio.h" 
#include <stdlib.h> 
#include <conio.h> 
#define getpch(type) (type*)malloc(sizeof(type)) 
#define NULL 0 
struct pcb { /* 定义进程控制块PCB */ 
char name[10]; 
char state; 
int super; 
int ntime; 
int rtime; 
struct pcb* link; 
}*ready=NULL,*p; 
typedef struct pcb PCB; 
void sort() /* 建立对进程进行优先级排列函数*/ 
{
PCB *first, *second; 
int insert=0; 
if((ready==NULL)||((p->super)>(ready->super))) /*优先级最大者,插入队首*/ 
{ 
p->link=ready; 
ready=p; 
} 
else /* 进程比较优先级,插入适当的位置中*/ 
{ 
first=ready; 
second=first->link; 
while(second!=NULL) 
{ 
if((p->super)>(second->super)) /*若插入进程比当前进程优先数大,*/ 
{ /*插入到当前进程前面*/ 
p->link=second; 
first->link=p; 
second=NULL;
insert=1; 
} 
else /* 插入进程优先数最低,则插入到队尾*/ 
{ 
first=first->link; 
second=second->link; 
} 
} 
if(insert==0) first->link=p; 
} 
}
Void input() /* 建立进程控制块函数*/ 
{ 
int i,num; 
system("CLS"); /*清屏*/ 
printf("\n 请输入进程个数："); 
scanf("%d",&num);
for(i=0;i<num;i++) 
{ 
printf("\n 进程号No.%d:\n",i); 
p=getpch(PCB); 
printf("\n 输入进程名:"); 
scanf("%s",p->name); 
printf("\n 输入进程优先数:"); 
scanf("%d",&p->super); 
printf("\n 输入进程运行时间:"); 
scanf("%d",&p->ntime); 
printf("\n"); 
p->rtime=0;p->state='w'; 
p->link=NULL; 
sort(); /* 调用sort函数*/ 
} 
} 
int space() 
{ 
int l=0; PCB* pr=ready;
while(pr!=NULL) 
{ 
l++; 
pr=pr->link; 
} 
return(l); 
} 
Void disp(PCB * pr) /*建立进程显示函数,用于显示当前进程*/ 
{ 
printf("\n qname \t state \t super \t ndtime \t runtime \n"); 
printf("|%s\t",pr->name); 
printf("|%c\t",pr->state); 
printf("|%d\t",pr->super); 
printf("|%d\t",pr->ntime); 
printf("|%d\t",pr->rtime); 
printf("\n"); 
}
Void check() /* 建立进程查看函数 */ 
{ 
PCB* pr; 
printf("\n **** 当前正在运行的进程是:%s",p->name); /*显示当前运行进程*/ 
disp(p); 
pr=ready; 
printf("\n ****当前就绪队列状态为:\n"); /*显示就绪队列状态*/ 
while(pr!=NULL) 
{ 
disp(pr); 
pr=pr->link; 
} 
} 
Void destroy() /*建立进程撤消函数(进程运行结束,撤消进程)*/ 
{ 
printf("\n 进程 [%s] 已完成.\n",p->name); 
free(p); 
} 
Void running() /* 建立进程就绪函数(进程运行时间到,置就绪状态*/
{(p->rtime)++; 
if(p->rtime==p->ntime) 
destroy(); /* 调用destroy函数*/ 
else 
{ 
(p->super)--; 
p->state='w'; 
sort(); /*调用sort函数*/ 
} 
} 
Void main() /*主函数*/ 
{ 
int len,h=0; 
char ch; 
input(); 
len=space(); 
while((len!=0)&&(ready!=NULL)) 
{ 
ch=getchar(); 
h++; 
printf("\n The execute number:%d \n",h); 
p=ready; 
ready=p->link; 
p->link=NULL; 
p->state='R'; 
check(); 
running(); 
printf("\n 按任一键继续......"); 
ch=getchar(); 
} 
printf("\n\n 进程已经完成.\n"); 
ch=getchar(); 

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
