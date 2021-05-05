import pyautogui
import time
import webbrowser
import pandas as pd
import numpy as np
import logging

conf=0.9
pyautogui.PAUSE=0.3

#이미지읽기 - 반복
def f_readImage(imgStr,waitCnt):  
    retry_counter = 0
    while retry_counter < waitCnt:
        try:
            result = pyautogui.locateCenterOnScreen(imgStr,confidence=conf)
            if result:
                time.sleep(1)
                print('successful read = ',retry_counter, '- ', imgStr)
                retry_counter = 10  # to break the loop
                pyautogui.click(result)
                return result
            else:
                retry_counter += 1
        except:
            time.sleep(1)  # retry after some time, i.e. 1 sec
            retry_counter += 1
    print('fail to read image ', retry_counter, '- ', imgStr)
    return None

#이미지읽기 - no repeat   
def img_click(imgStr,actn='click'):
    q=pyautogui.locateCenterOnScreen(imgStr,confidence=conf)
    if q==None:
        print('fail to click image ', imgStr)
    else:
        if actn=='dbl':
            pyautogui.doubleClick(q)    
        else: pyautogui.click(q)
    return q
   
#동작에 따른 처리    
def proc_action(row,browser): 
    res=None
    action=row['Action']
    val = str(row['Value'])
    if np.isnan(row['Repeat']):
        cnt=0
    else: cnt= int(row['Repeat'])
    if np.isnan(row['Time sleep']):
        seconds=0
    else: seconds=int(row['Time sleep'])
    if action=='keyPress':    
        key = row['Keyboard'] 
    else:
        key=''
    breaks=row['ErrorBreak']
        
    if action=='url':
        webbrowser.get(browser).open(val)
    elif action=='keyPress':
        if  cnt == 0:
            pyautogui.typewrite([key])   
        else: 
            pyautogui.press(key,presses=cnt)                  
    elif action=='imageClick':
        if  cnt > 0:
            q=f_readImage(val,cnt)
            if (q==None) & (breaks=='yes'):
                res= val + '이미지 오류'  
        else:
             img_click(val)
    elif action=='valueInput':        
         pyautogui.typewrite(val)
    elif action=='screenShot':        
         pyautogui.screenshot(val)
            
    if seconds > 0: 
        time.sleep(seconds)
    
    return res

try:
    loops=True
    while loops==True:
        logging.basicConfig(filename='myrpa.log', level=logging.DEBUG)
        logging.info('Started : %s'%time.strftime("%Y%m%d %H:%M:%S",time.localtime()))

        control=pd.read_excel('../rpa.xlsx',sheet_name='control',header=0)
        browser= str(control['BrowserPath'][0])
    #     print(browser, jobs,control['작업명'])

        if len(control['ActionChoice']) ==1:
             jobs=str(control['ActionChoice'][0])
        else:   jobs = pyautogui.confirm(text='어느 화면으로?',title='선택',buttons=control['ActionChoice'])

        if jobs==None:
            result='실행 취소합니다'
            loops=False
            raise Exception(result) 

        seq= list(control['ActionChoice']).index(jobs) #선택한 작업의 index
        browser= str(control['BrowserPath'][seq]) if control['BrowserPath'].fillna(0)[seq]!=0 else str(control['BrowserPath'][0])     #선택한 작업의 browser

        data=pd.read_excel('../rpa.xlsx',sheet_name=jobs,header=0)
        for seq, row in data.iterrows():
            if row['Action']=='Stop':
                pyautogui.alert('작업을 종료합니다')
                break
            result = proc_action(row, browser)
            if result!=None:
                raise Exception(result) 

        logging.info('Finished : %s'%time.strftime("%Y%m%d %H:%M:%S",time.localtime()))

        if str(control['MenuRepeat'][0])!='yes': #메뉴반복이 아니면 종료
            loops=False
        time.sleep(3)
        pass
    
except  Exception as e: 
        print(f'error occured..{str(e)}')
        logging.info('%s ← error occured at..%s' %(str(e),time.strftime("%Y%m%d %H:%M:%S",time.localtime())))
#         pyautogui.alert(str(e))
        pass