from nltk import word_tokenize
from nltk.corpus import stopwords

if __name__ == '__main__':
    stop = set(stopwords.words('english'))
    with open('./newtext.csv', 'r') as f:
        lines = f.readlines()
        with open ('./aftertrim.csv', 'w') as n:
            for line in lines:
                tmp = ""
                for i in line.lower().split():
                    if i not in stop:
                        tmp = tmp + i + ' '
                n.write(tmp.strip() + "\n")

    '''stop = set(stopwords.words('english'))
    sentence = '6,"Israel is at a crossroads: two states or not two states. Of course, the world does not expect a deal to be made tomorrow -- or even soon. But it does want to hear from Israel that there has been no paradigm shift, no retreat to the old dream of a Greater Israel by annexation, and no abandonment of the commitment to Palestinian statehood.",cnn'
               '6,"israel crossroads: two states two states. course, world expect deal made tomorrow -- even soon. want hear israel paradigm shift, retreat old dream greater israel annexation, abandonment commitment palestinian statehood.",cnn'
    tmp = "'"
    for i in sentence.lower().split():
        if i not in stop:
            tmp = tmp + i + ' '
    #tmp = [i for i in sentence.lower().split() if i not in stop]
    print tmp.strip() + "'"'''
