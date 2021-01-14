import re


def remove_quotes(sentence):
    return sentence.lstrip("'").rstrip("'").lstrip('\"').rstrip('\"')


def reduce_multiplied_letters(sentence):
    rx = re.compile(r'(.)\1{2,}')
    offset = 0
    for m in re.finditer(rx, sentence):
        start_index = m.start(0)
        end_index = m.end(0)
        sentence = sentence[0:start_index - offset] + sentence[end_index - offset-1:]
        offset = offset + end_index - start_index - 1
    return sentence
