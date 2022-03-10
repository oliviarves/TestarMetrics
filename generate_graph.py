import settings
from rpy2 import robjects
from rpy2.robjects.packages import importr
from rpy2.tests import utils


utils = importr('utils')
scales = importr('scales')


def read_data(file):
    return 'read.csv2("{path}/{file}", sep=\',\', fileEncoding = "UTF-8-BOM")'.format(path=settings.RESULT_PATH, file=file)


def save_data(file_name, type):
    return 'ggsave(p1, filename = "{path}/{file}_{type}.png",height = 4, width = 7)'.format(path=settings.RESULT_PATH, file=file_name, type='multiple' if type else 'single')


def get_graph(stat, file_data, multi=False):

    ggplot = 'ggplot(data, aes(x=absolute_action, y=as.numeric({0}), color=ASM)) + geom_line()  + xlab("Actions") + ylab("{0}")'.format(stat)

    if multi:
        ggplot += ' + facet_wrap(\'~ASM\', ncol=4)'

    r_cmd = '''
            library(ggplot2)
            library(dplyr)
            library(tidyr)
            
            data <- {data}
            
            p1 = {plot}
              
            {save}
            
            '''.format(data=read_data(file_data), plot=ggplot, save=save_data(stat, multi))

    robjects.r(r_cmd)


def get_state_model_graph():

    robjects.r('''
        data = read.csv2('results/StateModel.csv', sep=',', fileEncoding = "UTF-8-BOM")
    
        p1 = ggplot(data, aes(x=machine_action, y=as.numeric(UnvisitedActions), color=ASM)) +
             geom_line() +
             facet_wrap('~ASM', ncol=1)
    
        ggsave(p1, filename = "{1}/{2}_{4}.png",height = 4, width = 7)
    ''')
