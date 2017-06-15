# -*- coding: utf-8 -*-
from pynlple.data.jsonsource import YSProdElasticSource, FileJsonDataSource, ElasticJsonDataSource
from pynlple.data.datasource import TsvDataframeSource
from pynlple.data.filesource import FilePathSource
from pynlple.data.source import BulkSource
from pynlple.exceptions import DataSourceException
from pynlple.processing.preprocessor import DefaultPreprocessorStack
from pynlple.module import append_paths, file_name
import io

def get_theme_id(filepath):
    filename = file_name(filepath)
    theme_id = filename[:filename.index('_')]
    return int(theme_id)

# preprocessor = DefaultPreprocessorStack()
preprocessor = None
stamp = 'mentions'
extension_suffix = '.json'
# theme_ids = [int(line) for line in io.open('E:/active_themes.txt', 'rt', encoding='utf8')]
# theme_ids = [int(line.split('\t')[0]) for line in io.open('E:\Projects\YouScan\data-science-lab\lab\youscan\\nestle-rus_commercial_theme_tag_ids.txt', 'rt', encoding='utf-8')]
# theme_tags_df = TsvDataframeSource('../lab/classification/target_tags.tsv', index_column='').get_dataframe()
# types = {'commercial'}
# target_theme_ids = theme_tags_df[theme_tags_df['type'].isin(types)]['Theme_Id'].tolist()
data_folder_path = 'E:/Projects/YouScan/data-science-lab/data/youscan/2017-06-14'
# downloaded_filepaths = {get_theme_id(path_) for path_ in FilePathSource([data_folder_path], extension_suffix='_tags.json').get_files()}
# theme_ids = list(filter(lambda t: t not in downloaded_filepaths, target_theme_ids))
target_commercial_theme_ids = [ 41546,  41550,  47250,  48378,  49155,  49165,  49206,  49341,
        49443,  49445,  49475,  49601,  49694,  49701,  49725,  49727,
        49755,  49756,  49788,  49795,  49952,  49954,  49956,  49961,
        49968,  50004,  50218,  50223,  50224,  50285,  50286,  50287,
        50488,  50492,  50833,  50849,  71171,  71331,  63181,  64360,
        67156,  67160,  78516,  78518,  78519,  83944, 100069,  24874,
        49971,  50030]
theme_ids = target_commercial_theme_ids[1:]
print(', '.join(str(id_) for id_ in theme_ids))

bulk_size = 10000
take = 300000
query = {
    'sort': [{'published': {'order': 'desc'}}],
    'query': {
        'filtered': {
            'filter': {
                'bool': {
                    'should': [
                        {'missing': {'field': 'spam3'}},
                        {'term': {'spam3': {'value': False}}}
                    ],
                    'must': [
                        {'term': {'deleted': False}}
                    ]
                }
            }
        },
        # 'range': {
        #     "published": {
        #         "gte": "2015-12-18",
        #         "lte": "2016-11-30",
        #     }
        # }
    }
}
# fields = 'uid language text title tags authorId published postType resourceType sourceName'.split()
fields = None
# stamp += '_' + query['query']['range']['published']['gte'] + '-' + query['query']['range']['published']['lte']

for theme_id in theme_ids:
    out_file_path = append_paths(data_folder_path,  str(theme_id) + '_' + stamp + extension_suffix)
    index = str(theme_id)
    try:
        print('Getting index {}'.format(index))
        elastic_source = YSProdElasticSource(index=index,
                                             query=query,
                                             keys=fields)
        datasource = BulkSource(elastic_source, bulk_size=bulk_size).take(take)
        result_json = datasource.get_data()
        if preprocessor:
            for result in result_json:
                result['prep_text'] = preprocessor.preprocess(result['text'])
        FileJsonDataSource(file_path=out_file_path).set_data(result_json)
    except DataSourceException as e:
        message = u'Could not dump {0} data due to: {1}'.format(str(theme_id), e)
        print(message)
