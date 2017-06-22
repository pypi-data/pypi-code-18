import pickle
import pandas as pd
import keras
from keras.models import Model
from keras.layers import Input, Dense, Embedding, Concatenate, Flatten, Dropout, SpatialDropout1D, BatchNormalization, Conv1D, MaxPooling1D, Maximum 
from keras.layers import TimeDistributed
from keras.optimizers import Adam

def create_n_gram_df(df, number = 11):
    n = int((number-1)/2)

    for i in range(n):
        df['char-{}'.format(i+1)] = df['char'].shift(i+1)
        df['type-{}'.format(i+1)] = df['type'].shift(i+1)
        df['char{}'.format(i+1)] = df['char'].shift(-i-1)
        df['type{}'.format(i+1)] = df['type'].shift(-i-1)

    return df[n:-n].copy()

def add_padding(df, number = 11):
    n = int((number-1)/2)
    df0 = pd.DataFrame(columns=df.columns)
    for i in range(n):
        df0 = df0.append({'char': ' ', 'type': 'p', 'target': True}, ignore_index=True)
    df = pd.concat([df0, df, df0])
    df.reset_index(inplace=True, drop=True)
    return df

def df_transform(df, le_char, le_type):
    df['char'] = le_char.transform(df['char'])
    df['type'] = le_type.transform(df['type'])

    for i in range(5):
        df['char-{}'.format(i+1)] = le_char.transform(df['char-{}'.format(i+1)])
        df['char{}'.format(i+1)] = le_char.transform(df['char{}'.format(i+1)])
        df['type-{}'.format(i+1)] = le_char.transform(df['type-{}'.format(i+1)])
        df['type{}'.format(i+1)] = le_char.transform(df['type{}'.format(i+1)])
    return df
'''
def get_file(my_path):
    f = []
    for (dirpath, dirnames, filenames) in walk(my_path):
        f.extend(filenames)
        break
    return f
'''
def create_df(words):
    cha_type = {
    'กขฃคฆงจชซญฎฏฐฑฒณดตถทธนบปพฟภมยรลวศษสฬอ':'c',
    'ฅฉผฟฌหฮ':'n',
    'ะาำิีืึุู':'v',  # า ะ ำ ิ ี ึ ื ั ู ุ
    'เแโใไ':'w',
    '่้๊๋':'t', # วรรณยุกต์ ่ ้ ๊ ๋
    '์ๆฯ.':'s', # ์  ๆ ฯ .
    '0123456789๑๒๓๔๕๖๗๘๙':'d',
    '"':'q',
    "'":'q',
    ' ':'p',
    'abcdefghijklmnopqrstuvwxyz':'s_e',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ':'b_e'
    }

    data_dict = {'char':[],'type':[],'target':[]}

    for i,word in enumerate(words):
        for idx, char in enumerate(word):
            in_dict = 0
            for key in cha_type.keys():
                if char in key:
                    data_dict['char'].append(char)
                    data_dict['type'].append(cha_type[key])
                    data_dict['target'].append((idx==0))
                    in_dict = 1
                    break
                else:
                    pass
            if in_dict == 0:
                data_dict['char'].append(char)
                data_dict['type'].append('o')
                data_dict['target'].append((idx==0))
            else:
                pass

    df = pd.DataFrame(data_dict, columns=['char','type','target'])
    return df

def get_convo_nn(no_word = 200, n_gram=21, no_char = 178):
    input1 = Input(shape=(n_gram,))
    input2 = Input(shape=(n_gram,))

    a = Embedding(no_char, 32, input_length=n_gram)(input1)
    a = SpatialDropout1D(0.2)(a)
    
    a2 = Conv1D(no_word, 2, strides=1, padding="same", activation='relu')(a)
    a2 = TimeDistributed(Dense(5, input_shape=(n_gram, no_word)))(a2)
    a3 = Conv1D(no_word, 3, strides=1, padding="same", activation='relu')(a)
    a3 = TimeDistributed(Dense(5, input_shape=(n_gram, no_word)))(a3)
    a4 = Conv1D(no_word, 4, strides=1, padding="same", activation='relu')(a)
    a4 = TimeDistributed(Dense(5, input_shape=(n_gram, no_word)))(a4)
    a5 = Conv1D(no_word, 5, strides=1, padding="same", activation='relu')(a)
    a5 = TimeDistributed(Dense(5, input_shape=(n_gram, no_word)))(a5)
    a6 = Conv1D(no_word, 6, strides=1, padding="same", activation='relu')(a)
    a6 = TimeDistributed(Dense(5, input_shape=(n_gram, no_word)))(a6)
    a7 = Conv1D(no_word, 7, strides=1, padding="same", activation='relu')(a)
    a7 = TimeDistributed(Dense(5, input_shape=(n_gram, no_word)))(a7)
    
    a_sum = Maximum()([a2,a3,a4,a5,a6,a7])
    
    b = Embedding(12, 12, input_length=n_gram)(input2)
    b = SpatialDropout1D(0.2)(b) 
    
    x = Concatenate(axis=-1)([a, a_sum, b])
    x = BatchNormalization()(x)
    
    x = Flatten()(x)
    x = Dense(100, activation='relu')(x)
    
    out = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=[input1,input2], outputs=out)
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['acc'])
    return model



def deepcut(word):

    n_gram = 21
    n_gram2 = int((n_gram-1)/2)

    df_test = create_df(word)
    df = df_test.copy()

    df_test = add_padding(df_test, n_gram)

    with open('weight/object.pk', 'rb') as handle:
        char_le, type_le, listed_char = pickle.load(handle)

    to_be_replaced = list(set(df_test['char'].unique()) - set(listed_char))

    if len(to_be_replaced) != 0:
        df_test.replace(to_replace=to_be_replaced, value='other', inplace=True)

    df_test['char'] = char_le.transform(df_test['char'])
    df_test['type'] = type_le.transform(df_test['type'])

    df_n_gram_test = create_n_gram_df(df_test, number = n_gram)

    char_row = ['char'+str(i+1) for i in range(n_gram2)] + ['char-'+str(i+1) for i in range(n_gram2)] + ['char']
    type_row = ['type'+str(i+1) for i in range(n_gram2)] + ['type-'+str(i+1) for i in range(n_gram2)] + ['type']

    x_test1 = df_n_gram_test[char_row].as_matrix()
    x_test2 = df_n_gram_test[type_row].as_matrix()

    model = get_convo_nn()

    model.load_weights("weight/best_cnn.h5")

    y_predict = model.predict([x_test1,x_test2])
    y_predict = [(i[0]>0.5)*1 for i in y_predict]

    result = ''

    for idx, row in df.iterrows():
        if y_predict[idx] == True:
            result += '|'
        result += row['char']
    return result

