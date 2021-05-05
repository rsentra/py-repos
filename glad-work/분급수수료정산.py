import pandas as pd
import mypkgs.GladUtil as glad

data=pd.read_excel('정산파일.xlsx',header=1)
for seq, row in data.iterrows():
    if row['구분']=='분급파일':
        inFile1 = row['파일폴더'] + row['파일명']
        company = row['회사명']
    elif row['구분']=='선급파일':
        inFile2 = row['파일폴더'] + row['파일명']
    elif row['구분']=='출력파일':
        outFile = row['파일폴더'] + row['파일명']
    else: print('error')

print('입력1 = ', inFile1)
print('입력2 = ', inFile1)
print('출력 = ', outFile)
print(company, '-- 작업을 시작합니다')

#분급원장-2019.12월 이후 실시

df=pd.read_excel(inFile1, header=0)
df=df[df.본부=='MPKJ']
df['계약일자']=df.계약일자.map(lambda x: str(x)[:8])
df=df[~((df.사원명=='문홍주') & (df.계약일자 < '20180601'))]  #문홍주 예정건 삭제
#지점 공란은 메트로로 / 메트로중 지사건 분리
df=glad.BrhConv(df,'지점그룹')

#선급 원장: 기존 방식의 계산값(글로벌 -> MP)
df2=pd.read_excel(inFile2, header=0, sheet_name='전체')  
df2=df2[(df2.보험사==company)&(df2.계약종류=='장기')]


#concat를 하기 위해 index순번을 재부여
df=df.sort_values(by=['증권번호','납입회차','상태','수수료']).reset_index()
df2=df2.sort_values(by=['증권번호','납입회차','상태','수수료계']).reset_index()
df=pd.concat([df, df2.수수료계], axis=1)  #차례대로 합침
df.rename(columns={'수수료계':'선급수수료','수수료':'분급수수료'}, inplace=True)
df['차액(선급-분급)']=df.선급수수료 - df.분급수수료

#요약시트 생성
dfT=pd.DataFrame(df.groupby('지점')['선급수수료','분급수수료','차액(선급-분급)'].agg('sum'))
직영=['엠피레전드','엠피여주','엠피의정부','제이엔제이','씨티엠지점']
dfT.loc[dfT.index.isin(직영),'%']=100 
dfT.loc[~dfT.index.isin(직영),'%']=70
dfT['kj']=dfT['%'] * dfT['차액(선급-분급)'] / 100  #귀속분 산출
s1=dfT.sum()    #요약값 산출
s1['%']=0       
dfT.loc['합계']=s1        #마지막 row에 합계추가
dfT['이자']= (dfT['kj'] * 0.03 / 12).astype(int)  #마지막 column열에 이자 3% 적용

with pd.ExcelWriter(outFile) as writer:  
    dfT.to_excel(writer, sheet_name='요약',index=True)
    df.to_excel(writer, sheet_name='목록',index=False) 

if  (df.선급수수료.sum() - df2.수수료계.sum()) != 0:
     print('오류발생xxxxxxxxxxxxxxxxxxxxxxxxxx')
else: print('정상종료-------------------------')

print('선급수수료-matched = {:,.0f}'.format(df.선급수수료.sum()) )
print('선급수수료-원장 = {:,.0f}'.format(df2.수수료계.sum() ))
print('분급수수료-원장 = {:,.0f}'.format(df.분급수수료.sum() ) )
print('분급수수료-원장 = {:,.0f}'.format(df['차액(선급-분급)'].sum() ) )