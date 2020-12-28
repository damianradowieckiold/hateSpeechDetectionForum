from df.loader import load_english_all

df = load_english_all()

# hateful = df[df['label']=='hateful']
# print(hateful.shape[0])
# print(df.shape[0] - hateful.shape[0])

from predict.en.RandomForest import predict as RFPredict
from predict.en.RNN_EN import predict as RNNPredict
from predict.en.VADER_EN import predict as VADERPredict

unclear_situations_count = 0
vader_true_in_unclear_situation = 0

for index, row in df.iterrows():
    comment = row['tweet']
    RFResult = RFPredict(comment)
    RNNResult = RNNPredict(comment)
    VADERResult = VADERPredict(comment)
    if RFResult and not RNNResult:
        unclear_situations_count = unclear_situations_count + 1
        if VADERResult:
            vader_true_in_unclear_situation = vader_true_in_unclear_situation + 1
    if RNNResult and not RFResult:
        unclear_situations_count = unclear_situations_count + 1
        if VADERResult:
            vader_true_in_unclear_situation = vader_true_in_unclear_situation + 1

print(unclear_situations_count)
print(vader_true_in_unclear_situation)