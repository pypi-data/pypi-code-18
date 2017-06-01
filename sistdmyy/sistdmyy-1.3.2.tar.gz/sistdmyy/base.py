from sistdmyy import db
import pandas as pd 

m=db()


def waizi_count_peryear(year):
    startdate="%d-01-01"%year
    enddate="%d-01-01"%(year+1)
    sql="""
    select count(distinct ztsfdm ) from basedb.dbo.t_zzjgjz
    where clrq>='%s' and clrq<'%s'
    and jglxdm in ('1','2') and qylxdm like '[567w]%%'
    """%(startdate,enddate)
    df=m.frommssql(sql)
    count_the_year=df.iat[0,0]
    return count_the_year

def waizi_zczj_peryear(year):
    startdate="%d-01-01"%year
    enddate="%d-01-01"%(year+1)
    sql="""
    select sum(zczj_rmb ) as zczj from basedb.dbo.t_zzjgjz
    where clrq>='%s' and clrq<'%s'
    and jglxdm in ('1','2') and qylxdm like '[567w]%%'
    """%(startdate,enddate)
    df=m.frommssql(sql)
    count_the_year=df.iat[0,0]
    return count_the_year

def waizi_count_mutiyear(beginyear,endyear):
    data=[(year,waizi_count_peryear(year),waizi_zczj_peryear(year)) for year in range(beginyear,endyear+1)]
    df=pd.DataFrame(data,columns=['year','count','zczj_rmb'])
    df['countP']=df['count'].pct_change()
    df['zczjP']=df['zczj_rmb'].pct_change()
    return df





def gb_pct(year):
    startdate="%d-01-01"%year
    enddate="%d-01-01"%(year+1)
    sql_union="""
        with a as (
    select jgdm,t1.zczj_rmb,t2.gb from basedb.dbo.t_zzjgjz as t1 left join basedb.dbo.dict_gb as t2
    on t1.gbdm=t2.gbdm 
    where  t1.gbdm is not null and t1.gbdm not in('156') and qylxdm like '[567w]%%' and clrq>'%s' and clrq<'%s')

    , g1 as (select gb,zczj_rmb,a.jgdm from basedb.dbo.t_zzjgjz as a,test_dmyy.dbo.sist_waizi as b

    where a.jgdm=b.jgdm and clrq>='%s' and qylxdm like '[567w]%%' and clrq<'%s' )

    ,g2 as (select jgdm,zczj_rmb,gb from (select jgdm,zczj_rmb,gb ,row_number() over(partition by jgdm order by gb) as rn
    from g1 where gb!='中国' ) as _t where rn<=3)
    ,g3 as (
    select * from a

    union 
    select * from g2)
        

    select gb,sum(zczj_rmb) as zczj_rmb,count(*) as count from g3

     group by gb 
     order by count(*) desc
    """%(startdate,enddate,startdate,enddate)
    df3=m.frommssql(sql_union)

    d3=df3.to_dict(orient='records')
    count=waizi_count_peryear(year)
    zczj=waizi_zczj_peryear(year)
    df3['count_p']=df3['count']/count
    df3['zczj_rmb_p']=df3['zczj_rmb']/zczj
    df3['zczj_rmb_p']=df3[['zczj_rmb_p']].applymap(lambda x:'%.6f'%x)
    return df3

def gb_pct20(year):
    df=gb_pct(year)
    
    df1=df[:21]
    return df1








def neizi_count_peryear(year):
    startdate="%d-01-01"%year
    enddate="%d-01-01"%(year+1)
    sql="""
    with a as (select ztsfdm from basedb.dbo.t_zzjgjz
        where clrq>='%s' and clrq<'%s'
        and jglxdm in ('1','2') and qylxdm like '[^567w]%%')
    ,b as (
    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode=0
    and len(shname)>3

    union

    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode<0
    and len(shname)>3)

    select  count(distinct ztsfdm)  as count from basedb.dbo.t_zzjgjz where ztsfdm in(select entid from b)
    """%(startdate,enddate)
    df=m.frommssql(sql)
    count_the_year=df.iat[0,0]
    return count_the_year

def neizi_zczj_peryear(year):
    startdate="%d-01-01"%year
    enddate="%d-01-01"%(year+1)
    sql="""
    with a as (select ztsfdm from basedb.dbo.t_zzjgjz
        where clrq>='%s' and clrq<'%s'
        and jglxdm in ('1','2') and qylxdm like '[^567w]%%')
    ,b as (
    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode=0
    and len(shname)>3

    union

    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode<0
    and len(shname)>3)

    select  sum(zczj_rmb)  as zczj from basedb.dbo.t_zzjgjz where ztsfdm in(select entid from b) 
    """%(startdate,enddate)
    df=m.frommssql(sql)
    zczj_the_year=df.iat[0,0]
    return zczj_the_year

def neizi_countANDzczj_mutiyear(beginyear,endyear):
    data=[(year,neizi_count_peryear(year),neizi_zczj_peryear(year)) for year in range(beginyear,endyear+1)]
    df=pd.DataFrame(data,columns=['year','count','zczj'])
    df['count_pct_change']=df['count'].pct_change()
    df['zczj_pct_change']=df['zczj'].pct_change()
    return df



#--------------------------------------------------------预留 分国内城市----------------------------------------

#----------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------各区----------------------------------------------------



def waizi_qh0_peryear(year,xzqh):
    startdate="%d-01-01"%year
    enddate="%d-01-01"%(year+1)
    sql="""
    select count(distinct ztsfdm ) as count,sum(zczj_rmb) as zczj from basedb.dbo.t_zzjgjz
    where clrq>='%s' and clrq<'%s' and xzqh='%s'
    and jglxdm in ('1','2') and qylxdm like '[567w]%%'
    """%(startdate,enddate,xzqh)
    df=m.frommssql(sql)
    arr=xzqh,year,df.iat[0,0],df.iat[0,1]
    return arr



def waizi_qh_mutiyear(beginyear,endyear):
    xzqhs=['福田区','南山区','罗湖区','盐田区','龙岗区','宝安区','光明新区','龙华新区','大鹏新区','坪山新区']
    df=pd.DataFrame()
    for xzqh in xzqhs:
        data=[waizi_qh0_peryear(year,xzqh)  for year in range(beginyear,endyear+1) ]
        dftmp=pd.DataFrame(data,columns=['xzqh','year','count','zczj'])
        dftmp['countP']=dftmp['count'].pct_change()
        dftmp['zczjP']=dftmp['zczj'].pct_change()
        df=df.append(dftmp,ignore_index=True)
    return df


def neizi_qh0_peryear(year,xzqh):
    startdate="%d-01-01"%year
    enddate="%d-01-01"%(year+1)
    sql="""
    with a as (select ztsfdm from basedb.dbo.t_zzjgjz
        where clrq>='%s' and clrq<'%s'
        and jglxdm in ('1','2') and qylxdm like '[^567w]%%')
    ,b as (
    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode=0
    and len(shname)>3

    union

    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode<0
    and len(shname)>3)

    select  count(distinct ztsfdm) count,sum(zczj_rmb)  as zczj from basedb.dbo.t_zzjgjz where ztsfdm in(select entid from b) and xzqh='%s'
    """%(startdate,enddate,xzqh)
    df=m.frommssql(sql)
    arr=xzqh,year,df.iat[0,0],df.iat[0,1]
    return arr

def neizi_qh_mutiyear(beginyear,endyear):
    xzqhs=['福田区','南山区','罗湖区','盐田区','龙岗区','宝安区','光明新区','龙华新区','大鹏新区','坪山新区']
    df=pd.DataFrame()
    for xzqh in xzqhs:
        data=[neizi_qh0_peryear(year,xzqh)  for year in range(beginyear,endyear+1) ]
        dftmp=pd.DataFrame(data,columns=['xzqh','year','count','zczj'])
        dftmp['countP']=dftmp['count'].pct_change()
        dftmp['zczjP']=dftmp['zczj'].pct_change()
        df=df.append(dftmp,ignore_index=True)
    return df


#-------------------7.2016年各产业（行业）在深投资企业数量、注册资本金饼状图--------------------------
def hy_distribute1(year):
    startdate='%d-01-01'%year
    enddate='%d-01-01'%(year+1)
    sql="""
    with a as (select ztsfdm from basedb.dbo.t_zzjgjz
        where clrq>='%s' and clrq<'%s'
        and jglxdm in ('1','2') and qylxdm like '[^567w]%%')
    ,b as (
    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode=0
    and len(shname)>3

    union

    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode<0
    and len(shname)>3)
        ,c as (    select ztsfdm from basedb.dbo.t_zzjgjz
    where clrq>='%s' and clrq<'%s'
    and jglxdm in ('1','2') and qylxdm like '[567w]%%')

    ,d as (select distinct entid as ztsfdm from b
        )
    , e as (
    select substring(jjhydm,1,1) jjhydm,count(distinct ztsfdm) as count,sum(zczj_rmb) as zczj from basedb.dbo.t_zzjgjz where ztsfdm in(select ztsfdm from d)

    group by substring(jjhydm,1,1))

    select e.*,_t.jjhy from e left join basedb.dbo.dict_jjhy as _t on e.jjhydm=_t.jjhydm order by count desc
    """%(startdate,enddate,startdate,enddate)
    df=m.frommssql(sql)
    return df

def hy_distribute2(year):
    startdate='%d-01-01'%year
    enddate='%d-01-01'%(year+1)
    sql="""
    with a as (select ztsfdm from basedb.dbo.t_zzjgjz
        where clrq>='%s' and clrq<'%s'
        and jglxdm in ('1','2') and qylxdm like '[^567w]%%')
    ,b as (
    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode=0
    and len(shname)>3

    union

    select entid,shname from regdb.dbo.tdsh where entid in (select ztsfdm from a) and shatt=2 and entstatuscode<0
    and len(shname)>3)
        ,c as (    select ztsfdm from basedb.dbo.t_zzjgjz
    where clrq>='%s' and clrq<'%s'
    and jglxdm in ('1','2') and qylxdm like '[567w]%%')

    ,d as (
        select ztsfdm from c)
    , e as (
    select substring(jjhydm,1,1) jjhydm,count(distinct ztsfdm) as count,sum(zczj_rmb) as zczj from basedb.dbo.t_zzjgjz where ztsfdm in(select ztsfdm from d)

    group by substring(jjhydm,1,1))

    select e.*,_t.jjhy from e left join basedb.dbo.dict_jjhy as _t on e.jjhydm=_t.jjhydm order by count desc
    """%(startdate,enddate,startdate,enddate)
    df=m.frommssql(sql)
    return df


def task1():
    df1=waizi_count_mutiyear(2011,2016)
    df2=gb_pct20(2016)
    df3=neizi_countANDzczj_mutiyear(2011,2016)


    df4_1=waizi_qh_mutiyear(2015,2016)
    df4_2=neizi_qh_mutiyear(2015,2016)

    df5_1=hy_distribute1(2016)
    df5_2=hy_distribute2(2016)

    sheets=['外资','国别','内资','分区内外资','行业内外资']
    outdfss([[df1],[df2],[df3],[df4_1,df4_2],[df5_1,df5_2]],sheets)



