#!/usr/bin/env python
# coding: utf-8

# # －實作程式輔助判斷藥物造成SJS/TEN之可能性
# ## 本程式整合Naranjo score及ALDEN score，藉由輸入藥物資訊、病人資料及相關問題
# ## 經由分析後，即可比較各藥物間之懷疑程度，同時輸出藥物使用表格

# ### 讀取藥物資料(存於csv檔中)：
# * acetaminophen, 500 mg 1# QID, 2020/6/8-2020/6/10
# * prednisolone, 5 mg 2# QID, 2020/6/12-2020/6/24
# * prednisolone, 5 mg 1# QID, 2020/6/30-2020/7/4
# * TMP-SMX, 2# BID, 2020/6/12-2020/6/24

# In[1]:


input('歡迎使用Naranjo與ALDEN量表輔助工具\n')
Drug_list = []  # ['acetaminophen', 'prednisolone', 'TMP-SMX']
Drug_info_list = [] # [['500 mg 1# QID'], ['5 mg 2# QID', '5 mg 1# QID'], ['2# BID']]
Drug_date_list = [] # [['2020/6/8-2020/6/10'], ['2020/6/12-2020/6/24', '2020/6/30-2020/7/4'], ['2020/6/12-2020/6/24']]
Drug_score_list = []

print('讀取import.csv...\n')
with open('./import.csv', encoding='utf-8') as f:
    lines = f.readlines()
    for l in lines:
        l = l.replace('\n','')
        name = l.split(',')[0]
        info = l.split(',')[1]
        date = l.split(',')[2]
        
        print('讀取藥物: %s, 劑量: %s, 服用期間: %s' % (name, info, date))
        
        if name in Drug_list:  # 若該藥物已出現過
            drug_index = Drug_list.index(name)
            Drug_info_list[drug_index].append(info)
            Drug_date_list[drug_index].append(date)
        else:
            Drug_list.append(name)
            Drug_info_list.append([info])
            Drug_date_list.append([date])
print('\n')


# ### 輸入不良反應發生日期及症狀緩解日

# In[2]:


Index_day = input('請輸入不良反應發生日期(index day): ')
Resolution_day = input('請輸入症狀緩解日: ')


# ### ALDEN score & naranjo score

# In[3]:


import datetime
from dateutil.relativedelta import relativedelta

def transform_time(date):
    return datetime.datetime.strptime(date, '%Y/%m/%d')

def difference_day(date1, date2):
    try: diff = int(str(date1 - date2).split(' ')[0])
    except: diff = 0
    return diff

def ask_YN(question):
    ans = input(question).upper()
    if ans == 'Y' or ans == 'N':
        pass
    else: 
        print('輸入錯誤，請再試一次')
        ans = ask_YN(question)
    return ans

def ask_YNU(question):
    ans = input(question).upper()
    if ans == 'Y' or ans == 'N' or ans == 'U':
        pass
    else: 
        print('輸入錯誤，請再試一次')
        ans = ask_YNU(question)
    return ans

def ask_number(question):
    ans = input(question)
    try: ans = float(ans)
    except: 
        print('輸入錯誤，請再試一次')
        ans = ask_number(question)

    return ans

def ask_SaSiO(question):
    ans = input(question).upper()
    if ans == 'SA' or ans == 'SI' or ans == 'O':
        pass
    else: 
        print('輸入錯誤，請再試一次')
        ans = ask_SaSiO(question)
    return ans

PLACEBO = ask_YN('是否有任何一個藥物給予安慰劑，以測試不良反應是否有發生? (Y/N) ')  # Q6
TDM = ask_YN('是否有任何一個藥物監測濃度，以測試是否超出治療區間? (Y/N) ')  # Q7
OBJ = ask_YNU('此項不良反應是否有客觀的證據證明是藥品引起的？("Y"es/ "N"o/ "U"nknown) ')  #Q10
 

def analysis(drug, date_lst):
    Alden_score = []
    Naranjo_score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    
    start_day = transform_time(date_lst[0].split('-')[0])
    end_day = transform_time(date_lst[0].split('-')[1])
    rechallenge = len(date_lst)
    if rechallenge > 1:
        restart_day = transform_time(date_lst[1].split('-')[0])
        reend_day = transform_time(date_lst[1].split('-')[1])
    index_day = transform_time(Index_day)
    resolution_day = transform_time(Resolution_day)
    s_to_idx_day = difference_day(index_day, start_day) # index day - start_day的天數
    e_to_res_day = difference_day(resolution_day, end_day)
    idx_to_e_day = difference_day(end_day, index_day)
    
    print('----------------------')
    print('目前評分藥物: %s, 使用日期: %s, 不良反應發生日期: %s, 症狀緩解日期: %s' % (drug, ', '.join(date_lst), Index_day, Resolution_day))
    
#     先評估Naranjo score

#     Nq1在C5

#     Nq2在C1
    if rechallenge == 1:
        if e_to_res_day > 0: Naranjo_score[2] = (1, 'Y')
        else: 
            Nq3 = ask_YNU('　當停藥或服用此藥之解藥，不良反應是否減輕？("Y"es/ "N"o/ "U"nknown) ')
            if Nq3 == 'Y': Naranjo_score[2] = (1, 'Y')
            elif Nq3 == 'N': Naranjo_score[2] = (0, 'N')
            elif Nq3 == 'U': Naranjo_score[2] = (0, 'U')
    else: 
        Nq3 = ask_YNU('　當停藥或服用此藥之解藥，不良反應是否減輕？("Y"es/ "N"o/ "U"nknown) ')
        if Nq3 == 'Y': Naranjo_score[2] = (1, 'Y')
        elif Nq3 == 'N': Naranjo_score[2] = (0, 'N')
        elif Nq3 == 'U': Naranjo_score[2] = (0, 'U')
    
    if rechallenge == 1: Naranjo_score[3] = (0, 'U')  
    else: 
        Nq4 = ask_YNU('　停藥一段時間再重新服用此藥，同樣的不良反應是否再度發生？ ("Y"es/ "N"o/ "U"nknown) ')
        if Nq4 == 'Y': Naranjo_score[3] = (2, 'Y')
        elif Nq4 == 'N': Naranjo_score[3] = (-1, 'N')
        elif Nq4 == 'U': Naranjo_score[3] = (0, 'U')  

#     Nq5後面再評分

    if PLACEBO == 'Y':
        Nq6 = ask_YNU('　當給予安慰劑時，此項不良反應是否會再度發生？ ("Y"es/ "N"o/ "U"nknown) ')
        if Nq6 == 'Y': Naranjo_score[5] = (-1, 'Y')
        elif Nq6 == 'N': Naranjo_score[5] = (1, 'N')
        elif Nq6 == 'U': Naranjo_score[5] = (0, 'U')
    elif PLACEBO == 'N':
        Naranjo_score[5] = (0, 'U')
        
    if TDM == 'Y':
        Nq7 = ask_YNU('　此藥物的血中濃度是否達到中毒劑量？ ("Y"es/ "N"o/ "U"nknown) ')
        if Nq7 == 'Y': Naranjo_score[6] = (1, 'Y')
        elif Nq7 == 'N': Naranjo_score[6] = (0, 'N')
        elif Nq7 == 'U': Naranjo_score[6] = (0, 'U')
    elif TDM == 'N':
        Naranjo_score[6] = (0, 'U')
    
    if rechallenge == 1:
        Naranjo_score[7] = (0, 'U')
    else:
        Nq8 = ask_YNU('　對此病人而言，藥物劑量與不良反應的程度是否成正向關係？("Y"es/ "N"o/ "U"nknown) ')
        if Nq8 == 'Y': Naranjo_score[7] = (1, 'Y')
        elif Nq8 == 'N': Naranjo_score[7] = (0, 'N')
        elif Nq8 == 'U': Naranjo_score[7] = (0, 'U')
            
#   Nq9在C3

    if OBJ == 'Y': Naranjo_score[9] = (1, 'Y')
    elif OBJ == 'N': Naranjo_score[9] = (0, 'N')
    elif OBJ == 'U': Naranjo_score[9] = (0, 'U')

        
#   Criterion 1: Delay from initial drug component intake to onset of reaction (index day)

    if s_to_idx_day <= 28 and s_to_idx_day >= 5:
#       * Suggestive +3 (From 5 to 28 days)
        Alden_score.append(3)
        Naranjo_score[1] = (2, 'Y')
        
    elif s_to_idx_day <= 56 and s_to_idx_day >= 29:
#       * Compatible +2 (From 29 to 56 days)
        Alden_score.append(2)
        Naranjo_score[1] = (2, 'Y')
        
    elif s_to_idx_day <= 4 and s_to_idx_day >= 1:
#       * Likely +1 (From 1 to 4 days)
        Alden_score.append(1)
        Naranjo_score[1] = (2, 'Y')
        
    elif s_to_idx_day > 56:
#       * Unlikely −1 (>56 Days)
        Alden_score.append(-1)
        Naranjo_score[1] = (2, 'Y')
        
    else:
#       * Excluded −3 (Drug started on or after the index day)
        Alden_score.append(-3)
        Naranjo_score[1] = (-1, 'N')
    
        
        
        
#   Criterion 2: Drug present in the body on index day
    On_index_day = False
    if end_day == index_day or idx_to_e_day >= 0:
#       Index day 仍然服用藥物
        On_index_day = True
            
    if On_index_day == False:
        halflife = ask_number('　Index day 時無服用藥物, 請輸入藥物半衰期(hr): ')
        x5_halflife = halflife * 5 / 24
        End_day_plus_halflife = (end_day + datetime.timedelta(days=x5_halflife)).strftime("%Y/%m/%d")
        print('　%s 經過5倍半衰期後: %s ' % (end_day.strftime("%Y/%m/%d"), End_day_plus_halflife))
        end_day_plus_halflife = transform_time(End_day_plus_halflife)
        
        if end_day_plus_halflife == index_day or difference_day(end_day_plus_halflife, index_day) > 0:
            print('　Index day 時體內仍有藥物殘量 ')
            On_index_day = True
            
        else: 
            function = ask_YN('　請輸入病人肝腎功能是否異常、或是懷疑有交互作用，導致index day時仍有藥物累積在體內(Y/N): ')
            if function == 'Y':
#              體內懷疑有藥物殘留
#              * Doubtful −1 (Drug stopped at a time point prior to the index day by more than five times the elimination half-life but liver or kidney function alterations or suspected drug interactions are present)')
                Alden_score.append(-1)
            elif function == "N":
#              體內應無藥物殘留，且代謝功能正常
#              * Excluded −3 (Drug stopped at a time point prior to the index day by more than five times the elimination half-life, without liver or kidney function alterations or suspected drug interactions)')
                Alden_score.append(-3)
    if On_index_day == True: 
#       * Definite 0 (Drug stopped at a time point prior to the index day by more than five times the elimination half-life but liver or kidney function alterations or suspected drug interactions are present')
        Alden_score.append(0)
    
    
    
#   Criterion 3: Prechallenge/ rechallenge
    used = ask_YNU('　過去是否有服用過該藥物 ("Y"es/ "N"o/ "U"nknown) ')
    if used == 'U' or used == 'N':
#       Other reaction after use of similar drug: 0 (No known previous exposure to this drug)
        Alden_score.append(0)
    
    elif used == 'Y':
        his = ask_YN('　過去服用類似藥物時是否有造成傷害 (Y/N) ')
        
        if his == 'N':
#           * Negative −2 (Exposure to this drug without any reaction (before or after reaction)
            Alden_score.append(-2)
            Naranjo_score[8] = (0, 'N')
        
        elif his == 'Y':
            challenge = ask_SaSiO('　是否有因服用同樣藥物／類似藥物產生SJS/TEN，或是產生了其他副作用 ("Sa"me, "Si"miliar, "O"ther) ')
            if challenge == "Sa":
#               * Positive specific for disease and drug: 4 (SJS/TEN after use of same drug)
                Alden_score.append(4)
                Naranjo_score[8] = (1, 'Y')
            elif challenge == "Si":
#               * Positive specific for disease or drug: 2 (SJS/TEN after use of similar drug or other reaction with same drug)
                Alden_score.append(2)
                Naranjo_score[8] = (1, 'Y')
            elif challenge == 'O':
#               * Positive unspecific: 1　(Other reaction after use of similar drug)
                Alden_score.append(1)
                Naranjo_score[8] = (1, 'Y')
    if Naranjo_score[8] == 0: Naranjo_score[8] = (0, 'U')
    
        

    
    
    
#   Criterion 4: Dechallenge'
    if rechallenge == 1:
        if resolution_day == end_day or e_to_res_day < 0 : Alden_score.append(-2)
#       * Negative -2 (Drug continued without harm)
        else: Alden_score.append(0)
#       * Neutral 0 (Drug stopped (or unknown))       
    else:
        if resolution_day == reend_day or resolution_day == end_day or difference_day(resolution_day, reend_day) < 0 :
    #       緩解後仍然服用藥物
    #       * Negative -2 (Drug continued without harm)')
            Alden_score.append(-2)
        else:
    #       * Neutral 0 (Drug stopped (or unknown))
            Alden_score.append(0)




#    Criterion 5: Type of drug (notoriety)
    strongly_associated = ['TMP-SMX', 'allopurinol', 'lamotrigine', 'sulfamethoxazole','carbamazepine','phenytoin','nevirapine','sulfasalazine','sulfonamides','piroxicam','tenoxicam','phenobarbital','etoricoxib']
    associated = ['diclofenac','doxycycline','amoxicillin','ampicillin','ciprofloxacin','levofloxacin','amifostine','oxcarbazepine','rifampin','rifampicin']
    suspected = ['pantoprazole','glucocorticoids','omeprazole','tetrazepam','dipyrone','metamizole','terbinafine','levetiracetam']
    if drug in strongly_associated:
#       Strongly associated +3 (Drug of the “high-risk” list according to previous case–control studies)
        Naranjo_score[0] = (1, 'Y')
        Alden_score.append(3)
    elif drug in associated:
#       Associated +2 (Drug with definite but lower risk according to previous case–control studies)
        Naranjo_score[0] = (1, 'Y')
        Alden_score.append(2)
    elif drug in suspected:
#       Suspected +1 (Several previous reports, ambiguous epidemiology results (drug under surveillance))
        Naranjo_score[0] = (1, 'Y')
        Alden_score.append(1)
        
    else:
        ask = ask_YNU('　過去是否有文獻指出%s會造成SJS/TEN? ("Y"es/ "N"o/ "U"nknown) ' % drug)
        if ask == 'Y':
#           Suspected +1 (Several previous reports, ambiguous epidemiology results (drug under surveillance))
            Naranjo_score[0] = (1, 'Y')
            Alden_score.append(1)
        if ask == 'U':
#           Unknown 0 (All other drugs including newly released ones))
            Naranjo_score[0] = (0, 'U')
            Alden_score.append(0)
        elif ask == 'N':
#           Not suspected −1 (No evidence of association from previous epidemiology studyd with sufficient number of exposed controlsc)
            Naranjo_score[0] = (0, 'N')
            Alden_score.append(-1)
            
                    
    return [Alden_score, Naranjo_score]


for drug_idx in range(len(Drug_list)):
    Drug_score_list.append(analysis(Drug_list[drug_idx], Drug_date_list[drug_idx]))
print('輸入完畢\n')


# In[4]:


# 計算每一個的temp score

Sum_scores_ALDEN =[]
for ALD,NAR in Drug_score_list:
    temp_sum = 0
    for score in ALD:
        temp_sum += score
    Sum_scores_ALDEN.append(temp_sum)


idx = 0
for s in Sum_scores_ALDEN:
    temp_Sum_scores = []
    temp_Sum_scores.extend(Sum_scores_ALDEN)
    del temp_Sum_scores[idx]
    POSSIBLE_DRUG = False
    for ts in temp_Sum_scores:
        if ts > 3: POSSIBLE_DRUG = True
    if POSSIBLE_DRUG == True:
        Drug_score_list[idx][0].append(-1)
        Drug_score_list[idx][1][4] = (-1,'Y')
    else:
        Drug_score_list[idx][0].append(0)
        Drug_score_list[idx][1][4] = (2, 'N')
    idx += 1
input('預估分數...\n')


# In[8]:


def read_score(input_score, drug, date_lst):
    Alden_score = input_score[0]
    Naranjo_score = input_score[1]
    Start_day = date_lst[0].split('-')[0]
    start_day = transform_time(date_lst[0].split('-')[0])
    end_day = transform_time(date_lst[0].split('-')[1])
    rechallenge = len(date_lst)
    if rechallenge > 1:
        restart_day = transform_time(date_lst[1].split('-')[0])
        reend_day = transform_time(date_lst[1].split('-')[1])
    index_day = transform_time(Index_day)
    resolution_day = transform_time(Resolution_day)
    s_to_idx_day = difference_day(index_day, start_day) # index day - start_day的天數
    e_to_res_day = difference_day(resolution_day, end_day)
    idx_to_e_day = difference_day(end_day, index_day)
    
    
    print('\n[%s] Criterion 1: Delay from initial drug component intake to onset of reaction (index day)' % Alden_score[0])
    if Alden_score[0] == 3:
        print('　* Suggestive +3 (From 5 to 28 days)\n　initial day: %s, index day: %s, 相差%s天' % (Start_day, Index_day, s_to_idx_day))
    elif Alden_score[0] == 2:
        print('　* Compatible +2 (From 29 to 56 days)\n　initial day: %s, index day: %s, 相差%s天' % (Start_day, Index_day, s_to_idx_day))
    elif Alden_score[0] == 1:
        print('　* Likely +1 (From 1 to 4 days)\n　initial day: %s, index day: %s, 相差%s天' % (Start_day, Index_day, s_to_idx_day))
    elif Alden_score[0] == -1:
        print('　* Unlikely −1 (>56 Days)\n　initial day: %s, index day: %s, 相差%s天' % (Start_day, Index_day, s_to_idx_day))
    elif Alden_score[0] == -3:
        print('　* Excluded −3 (Drug started on or after the index day)\n　initial day: %s, index day: %s, 相差%s天' % (Start_day, Index_day, s_to_idx_day))
        
    print('[%s] Criterion 2: Drug present in the body on index day' % Alden_score[1])
    if Alden_score[1] == 0:
        print('　* Definite 0 (Drug continued up to index day or stopped at a time point less than five times the elimination half-life before the index day)')
        print('　最後服用藥物日: %s, index day: %s' % (end_day.strftime("%Y/%m/%d"), Index_day))
    elif Alden_score[1] == -1:
        print('　* Doubtful −1 (Drug stopped at a time point prior to the index day by more than five times the elimination half-life but liver or kidney function alterations or suspected drug interactions are present)')
        print('　體內懷疑有藥物殘留(超過五個半衰期，但肝腎功能不良))')
    elif Alden_score[1] == -3:
        print('　* Excluded −3 (Drug stopped at a time point prior to the index day by more than five times the elimination half-life, without liver or kidney function alterations or suspected drug interactions)')
        print('　體內應無藥物殘留(超過五個半衰期)，且代謝功能正常')
        
    print('[%s] Criterion 3: Prechallenge/ rechallenge' % Alden_score[2])
    if Alden_score[2] == 4:
        print('　* Positive specific for disease and drug +4 (SJS/TEN after use of same drug)')
    elif Alden_score[2] == 2:
        print('　* Positive specific for disease or drug +2 (SJS/TEN after use of similar drug or other reaction with same drug)')
    elif Alden_score[2] == 1:
        print('　* Positive unspecific +1　(Other reaction after use of similar drug)')
    elif Alden_score[2] == 0:
        print('  * Other reaction after use of similar drug 0 (No known previous exposure to this drug)')
    elif Alden_score[2] == -2:
        print('  * Negative −2 (Exposure to this drug without any reaction (before or after reaction)')
        
    print('[%s] Criterion 4: Dechallenge' % Alden_score[3])
    if Alden_score[3] == -2:
        print('　* Negative -2 (Drug continued without harm)')
        print('　緩解時仍然服用藥物')
    elif Alden_score[3] == 0:
        print('　* Neutral 0 (Drug stopped (or unknown))')
    if rechallenge == 1:    print('　最後服用藥物日: %s, 症狀緩解日: %s' % (end_day.strftime("%Y/%m/%d"), Resolution_day))
    else: print('服用藥物日期: %s, 症狀緩解日: %s' % (', '.join(date_lst), Resolution_day))

    print('[%s] Criterion 5: Type of drug (notoriety)' % Alden_score[4])
    if Alden_score[4] == 3:
        print('　* Strongly associated +3 (Drug of the “high-risk” list according to previous case–control studies)')
    elif  Alden_score[4] == 2:
        print('  * Associated +2 (Drug with definite but lower risk according to previous case–control studies)')
    elif Alden_score[4] == 1:
        print('  * Suspected +1 (Several previous reports, ambiguous epidemiology results (drug under surveillance))')
    elif Alden_score[4] == 0:
        print('  * Unknown 0 (All other drugs including newly released ones))')
    elif Alden_score[4] == -1:
        print('  * Not suspected −1 (No evidence of association from previous epidemiology studyd with sufficient number of exposed controlsc)')
        
        
    print('[%s] Criterion 6: Other cause' % Alden_score[5])
    if Alden_score[5] == 0:
        print('　No other possible drug')
    elif  Alden_score[5] == -1:
        print('  * Possible −1')
        
    sums_A = 0
    for s in Alden_score:
        sums_A += s
    print('\n')    
    if sums_A >= 6: print('Alden_score總分: %s, very probable' % sums_A)
    elif sums_A >= 4: print('Alden_score總分: %s, probable' % sums_A)
    elif sums_A >= 2: print('Alden_score總分: %s, possible' % sums_A)
    elif sums_A >= 0: print('Alden_score總分: %s, unlikely' % sums_A)
    else: print('Alden_score總分: %s, very unlikely' % sums_A)

        
    sums_N = 0
    print('\n[%s] Are there previous conclusive reports of this reaction? %s' % (Naranjo_score[0][0], Naranjo_score[0][1]))
    print('[%s] Did the adverse event appear after the drug was given? %s' % (Naranjo_score[1][0], Naranjo_score[1][1]))
    print('[%s] Did the adverse reaction improve when the drug was discontinued or a specific antagonist was given? %s' % (Naranjo_score[2][0], Naranjo_score[2][1]))
    print('[%s] Did the adverse reaction reappear upon readministering the drug? %s' % (Naranjo_score[3][0], Naranjo_score[3][1]))
    print('[%s] Were there other possible causes for the reaction? %s' % (Naranjo_score[4][0], Naranjo_score[4][1]))
    print('[%s] Did the adverse reaction reappear upon administration of placebo? %s' % (Naranjo_score[5][0], Naranjo_score[5][1]))
    print('[%s] Was the drug detected in the blood or other fluids in toxic concentrations? %s' % (Naranjo_score[6][0], Naranjo_score[6][1]))
    print('[%s] Was the reaction worsened upon increasing the dose? Or, was the reaction lessened upon decreasing the dose? %s' % (Naranjo_score[7][0], Naranjo_score[7][1]))
    print('[%s] Did the patient have a similar reaction to the drug or a related agent in the past? %s' % (Naranjo_score[8][0], Naranjo_score[8][1]))
    print('[%s] Was the adverse event confirmed by any other objective evidence?) %s' % (Naranjo_score[9][0], Naranjo_score[9][1]))
          

    for i in range(10):
          sums_N += Naranjo_score[i][0]


    if sums_N >= 9: print('Naranjo score總分: %s, Definite' % sums_N)
    elif sums_N >= 5: print('Naranjo score總分: %s, Probable' % sums_N)
    elif sums_N >= 1: print('Naranjo score總分: %s, Possible' % sums_N)
    elif sums_N <= 0: print('Naranjo score總分: %s, Doubtful' % sums_N)
        
        
    return (sums_A, sums_N)


Sum_scores = []
for s in Drug_list:
    idx = Drug_list.index(s)
    print('--------------------------------------')
    print('目前評分藥物: %s, 使用日期: %s, 不良反應發生日期: %s' % (Drug_list[idx], ', '.join(Drug_date_list[idx]), Index_day))
    Sum_scores.append(read_score(Drug_score_list[idx], Drug_list[idx], Drug_date_list[idx]))
    print('--------------------------------------')
    input('完成度(%s / %s)' % (idx+1, len(Drug_list)))


# In[29]:


import pandas as pd

df_list = []
idx = 0
for i in range(len(Drug_list)):
    temp = []
    temp.append(Drug_list[i])
    temp.append(Sum_scores[i][0])
    temp.extend(Drug_score_list[i][0])
    temp.append(Sum_scores[i][1])
    temp.extend(Drug_score_list[i][1])
    df_list.append(temp)
Score_df = pd.DataFrame(df_list, columns = ["藥物名稱", "Alden_score總分", 'Criterion 1', 'Criterion 2', 'Criterion 3','Criterion 4','Criterion 5','Criterion 6', "Naranjo score總分",
                                       'Nar_Q1', 'Nar_Q2', 'Nar_Q3', 'Nar_Q4', 'Nar_Q5', 'Nar_Q6', 'Nar_Q7', 'Nar_Q8', 'Nar_Q9', 'Nar_Q10'])
Score_df.set_index("藥物名稱", inplace=True)
Score_df.sort_values('Alden_score總分', inplace=True, ascending=False )
Score_df.to_excel('./藥物分析結果.xls')
Score_df
input('儲存藥物分析結果至./藥物分析結果.xls...')


# In[30]:


import pandas as pd
import numpy as np
def date_range_to_lst(date):
    day_lst = []
    start_day = transform_time(date[0].split('-')[0])
    end_day = transform_time(date[0].split('-')[1])
    diff_day_counts = difference_day(end_day, start_day)
    for i in range(diff_day_counts+1):
        day_lst.append((start_day + datetime.timedelta(days=i)).strftime("%Y/%m/%d"))
    return day_lst

all_date_list = []

for dates in Drug_date_list:
    if len(dates) > 1:
        for d in dates:
            RESULT = date_range_to_lst([d])
    else: 
        RESULT = date_range_to_lst(dates)
    for R in RESULT:
        if R not in all_date_list: all_date_list.append(R)



all_date_list = (pd.to_datetime(all_date_list).sort_values()).tolist()
all_date_list = str(all_date_list[0]).split(' 00:00:00')[0].replace('-','/') + '-' + str(all_date_list [-1]).split(' 00:00:00')[0].replace('-','/')
all_date_list = date_range_to_lst([all_date_list])
all_date_list = (pd.to_datetime(all_date_list).sort_values())



Empty_df = [[""] * len(all_date_list)] * len(Drug_list)

Date_df = pd.DataFrame(Empty_df, columns = all_date_list)
Date_df['藥物名稱'] = Drug_list
Date_df.set_index("藥物名稱", inplace=True)


for info in Drug_info_list:
    info_index = Drug_info_list.index(info)
    date_lst = Drug_date_list[info_index]
    drug = Drug_list[info_index]
    if len(info) > 1:
        for idx in range(len(date_lst)):
            date = pd.to_datetime(date_range_to_lst([date_lst[idx]]))
            Date_df.loc[drug, date] = info[idx]
    else:
        date = pd.to_datetime(date_range_to_lst(date_lst))
        Date_df.loc[drug, date] = info

t = []
for time in Date_df.columns.tolist():
    t.append(time.strftime('%Y/%m/%d'))

Date_df.columns = t
Date_df.to_excel('./使用藥物清單.xls')
Date_df
input('儲存藥物清單結果至./使用藥物清單.xls...')
input('執行完成。')

