import pandas as pd
import spacy
from textblob import TextBlob

nlp = spacy.load("ru_core_news_sm") # использовала маленькую модель для экономии времени

PATH = 'C:\\Users\\Acer\\Documents\\news.txt'
with open (PATH, 'r', encoding="utf-8") as f:
    text = f.read().replace('\n\n', ' ').replace('\n', ' ') # возможна и другая предобработка
print(text)

doc = nlp(text)

sentences = list(doc.sents)

df = pd.DataFrame(columns = [
    'Тип объекта',
    'Имя объекта',
    'Контекст',
    'Тональность'
])

for sentence in sentences:
    ents = list(sentence.ents)
    result_ents = []
    for ent in ents:
        if ent.lemma_ not in result_ents: #избегаем дубирования сущности в предложении
            df.loc[len(df.index)] = [
                ent.label_,
                ent.lemma_,
                sentence.text,
                TextBlob(sentence.text).sentiment.polarity]
            result_ents.append(ent.lemma_)
            
            # если использовать ent.text вместо ent.lemma_ сохраняется капитализация и падеж:
            #df.loc[len(df.index)] = [ent.label_, ent.text, sentence.text]

df1 = df.replace({'Тип объекта' : {
    'ORG' : 'организация',
    'LOC': 'место',
    'PERSON': 'персона',
    'NORP': 'национальная / религиозная принадлежность',
    'FAC': 'объект инфраструктуры',
    'ORG': 'организация',
    'GPE': 'страна / город',
    'PRODUCT': 'продукт',
    'EVENT ': 'событие',
    'WORK_OF_ART': 'произведение',
    'LAW': 'законодательный акт',
    'LANGUAGE': 'язык',
    'DATE': 'дата',
    'TIME': 'время',
    'PERCENT': 'процент',
    'MONEY': 'стоимость',
    'QUANTITY': 'количество',
    'ORDINAL': 'порядковые числительные',
    'CARDINAL': 'количественные числительные'
}})

df1.loc[df1['Тональность'] > 0, 'Тональность'] = 'положительный'
df1.loc[df1['Тональность'] < 0, 'Тональность'] = 'отрицательный'
df1.loc[df1['Тональность'] == 0, 'Тональность'] = 'нейтральный'
df1.head()

RESULT_PATH = "C:\\Users\\Acer\\Desktop\\result.xlsx"
df1.to_excel(RESULT_PATH,
             sheet_name='Sheet_name_1')