import pickle
#import utils

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


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as my_file:
        word = my_file.read()
    print(deepcut(word))

    
