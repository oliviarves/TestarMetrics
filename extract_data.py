import csv
import settings
from os import listdir
from os.path import isfile, join


def get_files(path, filename='stateModelMetrics'):
    for file in listdir(path):
        if isfile(join(path, file)) and filename in file:
            yield file


def get_ASM(filename):
    cleaned = filename[54:]
    cleaned = cleaned.replace('rl_', '')
    cleaned = cleaned[cleaned.find('_') + 1:]
    return cleaned[:cleaned.find('_')]


def extract_coverage_data():
    row = 0
    file_num = 0
    coverage_vars = ['InstructionCoverage', 'BranchCoverage']
    with open(join(settings.RESULT_PATH, settings.COVERAGE_FILE), 'w', newline='') as csv_file:
        cov_w = csv.writer(csv_file, delimiter=',')
        cov_w.writerow(
            ['abstraction', 'file_name', 'sut', 'ASM', 'machine', 'sequence', 'action',
             'absolute_action'] + coverage_vars)
        for file in get_files(settings.METRIC_FILES, 'coverageMetricsMerged'):
            file_num += 1
            with open(join(settings.METRIC_FILES, file), mode='r', encoding='utf-8') as file_r:
                for i, line in enumerate(file_r):
                    if (i > settings.MAX_VALUE):
                        break
                    row += 1
                    splitted = line.split('|')
                    cov_w.writerow(
                        [settings.METRIC_FILES, file[54:], file[54:54 + file[54:].find('_')], get_ASM(file),
                         file_num, splitted[1],
                         splitted[3], i + 1, splitted[9], splitted[13]])
    return file_num


def extract_state_model_data():
    row = 0
    file_num = 0
    state_vars = ['AbstractStates', 'AbstractActions', 'UnvisitedActions', 'ConcreteStates', 'ConcreteActions']
    with open(join(settings.RESULT_PATH, settings.STATE_MODEL_FILE), 'w', newline='') as csv_file:
        cov_w = csv.writer(csv_file, delimiter=',')
        cov_w.writerow(
            ['abstraction', 'file_name', 'sut', 'ASM', 'machine', 'absolute_action', 'SequenceTotal', 'actionnr', ]+state_vars)
        for file in get_files(settings.METRIC_FILES, 'stateModel'):
            file_num += 1
            with open(join(settings.METRIC_FILES, file), mode='r', encoding='utf-8') as file_r:
                for i, line in enumerate(file_r):
                    row += 1
                    splitted = line.split('|')
                    action = int(splitted[3])
                    cov_w.writerow(
                        [settings.METRIC_FILES, file[54:], file[54:54+file[54:].find('_')], get_ASM(file), file_num, i + 1, splitted[1], row, splitted[4].split()[1], splitted[5].split()[1],  splitted[6].split()[1], splitted[7].split()[1], splitted[7].split()[1]])
    return file_num
