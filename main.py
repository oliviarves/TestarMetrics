import extract_data
import generate_graph
import settings


def process_coverage_metrics():
    file_num = extract_data.extract_coverage_data()

    state_model_stats = ['InstructionCoverage', 'BranchCoverage']

    for stat in state_model_stats:
        generate_graph.get_graph(stat, settings.COVERAGE_FILE)
        if file_num >= 1:
            generate_graph.get_graph(stat, settings.COVERAGE_FILE, multi=True)


def process_state_model_metrics():
    file_num = extract_data.extract_state_model_data()

    state_model_stats = ['UnvisitedActions', 'AbstractStates', 'AbstractActions', 'ConcreteStates', 'ConcreteActions']

    for stat in state_model_stats:
        generate_graph.get_graph(stat, settings.STATE_MODEL_FILE)
        if file_num >= 1:
            generate_graph.get_graph(stat, settings.STATE_MODEL_FILE, multi=True)


process_coverage_metrics()
process_state_model_metrics()

