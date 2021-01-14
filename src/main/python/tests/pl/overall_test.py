import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

from df.loader import load_polish_test, load_english_test
from predict.en.VADER import VADER
from predict.pl.RNN import RNN
from predict.pl.RandomForest import RandomForest

df = load_polish_test()
df_en = load_english_test()

vader_good = 0
vader_bad = 0

unclear_situations_count = 0
vader_true_in_unclear_situation = 0
vader_false_when_others_true = 0
vader_predicted_correctly_but_others_not = 0

RF_ = RandomForest()
RNN_ = RNN()
VADER_ = VADER()

result = pd.DataFrame(columns=['label'])

for index, row in df.iterrows():
    comment = row['tweet']
    comment_en = df_en.iloc[index]['tweet']
    expected_result = (row['label'] == 'hateful')
    RF_result = RF_.predict(comment)
    RNN_result = RNN_.predict(comment)
    VADER_result = VADER_.predict(comment_en)

    overall_result = (RNN_result and RF_result) or ((RNN_result or RF_result) and VADER_result)
    if overall_result:
        result = result.append({'label': 'hateful'}, ignore_index=True)
    else:
        result = result.append({'label': 'normal'}, ignore_index=True)

    if RF_result and not RNN_result:
        unclear_situations_count = unclear_situations_count + 1
        if VADER_result:
            vader_true_in_unclear_situation = vader_true_in_unclear_situation + 1
        if VADER_result and expected_result:
            vader_good = vader_good + 1
        else:
            vader_bad = vader_bad + 1
    if RNN_result and not RF_result:
        unclear_situations_count = unclear_situations_count + 1
        if VADER_result:
            vader_true_in_unclear_situation = vader_true_in_unclear_situation + 1
        if VADER_result and expected_result:
            vader_good = vader_good + 1
        else:
            vader_bad = vader_bad + 1
    if RNN_result and RF_result and not VADER_result:
        vader_false_when_others_true = vader_false_when_others_true + 1
    if RNN_result != expected_result and RF_result != expected_result and VADER_result == expected_result:
        vader_predicted_correctly_but_others_not = vader_predicted_correctly_but_others_not + 1

print("Is VADER helpful?")
print("Unclear situations: " + str(unclear_situations_count))
print("VADER solved to true: " + str(vader_true_in_unclear_situation))
print("VADER solved to false: " + str(unclear_situations_count - vader_true_in_unclear_situation))
print("VADER is wrong: " + str(vader_false_when_others_true))
print("VADER prediction good, when others not: " + str(vader_predicted_correctly_but_others_not))
print("VADER prediction good, resolved unclearance: " + str(vader_good))
print("VADER prediction bad, resolved unclearance: " + str(vader_bad))
print("------------------------------------------")
print('accuracy %s' % accuracy_score(result['label'], df['label']))
print(classification_report(df['label'], result['label'], target_names=['hateful', 'normal']))
