import sys

from predict.en.VADER import VADER
from predict.pl.RNN import RNN
from predict.pl.RandomForest import RandomForest


def predict(sentence):
    VADER_result = VADER().translate_and_predict(sentence)
    RF_result = RandomForest().translate_and_predict(sentence)
    RNN_result = RNN().translate_and_predict(sentence)
    return (RNN_result and RF_result) or ((RNN_result or RF_result) and VADER_result)


if len(sys.argv) > 1:
    sentence_ = sys.argv[1]
else:
    sentence_ = input("Wprowadz linie do oceny: ")

print(predict(sentence_))
