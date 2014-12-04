import numpy
from pandas.core.frame import DataFrame
from pandas.io.excel import read_excel
from pycerego.core.wrapper import CeregoWrapper

__author__ = 'jacob'


def load_dataframe(dataframe, name, token):

    dataframe = dataframe.replace('', numpy.nan)
    dataframe = dataframe.fillna(method='ffill')
    raw_data = []
    for key, value in dataframe.iterrows():
        data_dict = value.to_dict()
        raw_data.append(data_dict)
    final_dict = {}
    for d in raw_data:
        if d['anchor'] in final_dict:
            n_key = d.pop('anchor')
            final_dict[n_key].append(d)
        else:
            n_key = d.pop('anchor')
            final_dict[n_key] = [d]

    cg_wrapper = CeregoWrapper()
    cg_wrapper.set_misc(token)
    cg_wrapper.create_set_and_populate(name, final_dict)

def load_from_excel(excel_file, sheet, token):

    df = read_excel(excel_file, sheet, index_col=None)
    df = df.rename(columns={'Topic': 'anchor', 'Selector': 'label', 'Message': 'association'})
    load_dataframe(df, sheet, token)

if __name__ == "__main__":

    token = "HSJXbAXVEcORLfp4bzyH9+mJqedIFgVXrMeJyDY0I5cV+x/M1B4NKKrXIKYKsdp1"
    load_from_excel("CFAData.xlsx", "Corporate Finance and Portfolio", token)

'''
    token = "HSJXbAXVEcORLfp4bzyH9+mJqedIFgVXrMeJyDY0I5cV+x/M1B4NKKrXIKYKsdp1"
    data = [["Anchor1", "Definition", "Its an anchor"],
            ['', "Significance", "Blah Blah"],
            ['Anchor2', "Another Def", 'BBBB'],
            ['', "Significance", "tada"]]
    columns = ['anchor', 'label', 'association']
    df = DataFrame(data, columns=columns)
    load_dataframe(df, "my_set", token)
'''