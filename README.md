# ALDEN-Naranjo-score-helper
  * *此程式在處理問卷分數時仍可能有誤判的情形（程式設計時的邏輯設想**可能**不周全），故作出之結果僅做為參考使用*
  * *It's a simple project of adverse drug events, which can simplify the progress of accessing SJS/TEN cases by using Naranjo score and ALDEN score.*
  * *THIS PROGRAM IS **NOT APPLICABLE** in clinical due to simplication in my coding.* 
  * *This program contains 3 part: input drug information (drug name, dosage, duration) and further question (e.g. medication history), compute Naranjo score and ALDEN score, save excel file including questionnaire score and drug list.*

## 程式發想
  1. 在評估SJS/TEN時，因為服用期間的所有藥物都要進行ALDEN score及Naranjo score的分數判斷，想要藉由已知的病患病史資料，來簡化藥物評估之流程，並減少可能發生的錯誤
  
## 程式流程
  1. 執行SJS_TEN_helper.py會讀取./import.csv，第一欄為藥物名稱、第二欄為藥物劑量、第三欄為服用期間（相同名稱的藥物若服用期間有中斷，可以選填兩個不同的副用期間與劑量）
  2. 輸入需要的資料 (包含不良反應發生日期、不良反應緩解日期、評估量表所需問題）
  3. 程式判斷各藥物之ALDEN score及Naranjo score，並輸出成xls檔，同時輸出藥物服用期間之xls檔

## 待解決問題
  1. 目前同個藥物只能輸入兩個不同的服用期間，輸入三個的話程式會爆炸
  2. 程式設計專注於SJS/TEN之評估，應用面狹窄
  3. 無使用者介面之設計，若要提供給民眾使用，還需額外設計UI（如串聯至google survey??)
  4. 串聯病人資訊及用藥史的部分尚未設計
  5. 程式碼**很醜**，救救瓜泥QQ，邏輯如下：　讀取資料　→　輸入資料　→　個別藥物Naranjo score、ALDEN score判斷　→　計算初步分數　→　計算最終分數
　→　輸出分數表格、產生xls檔
  
## 未來展望
  1. 結合已有資訊(如用藥史、用藥情況)，減少須詢問的問題
  2. 將此概念應用到其他量表上
  3. 擷取程式中Naranjo score的部分，製作成給一般民眾使用的平台，當藥物不良反應事件發生時，讓民眾更有警覺心

