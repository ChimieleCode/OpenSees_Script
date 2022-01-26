
from ModelOptions import run_pushover,run_time_history,compute_section_gaps_evnelopes,performance_point

print(f'-o-o-o- Generating Graphs -o-o-o-')

if run_pushover or performance_point:

    import Graphs.PushPullGraph

if run_time_history:

    import Graphs.ControlNodeGraph
    import Graphs.DriftGraph
    import Graphs.AccelerationGraph
    import Graphs.VelocityGraph

    import PostProcessing.ExportDrifts
    import PostProcessing.ExportAcc

    if compute_section_gaps_evnelopes:

        import PostProcessing.SectionGaps
        import PostProcessing.Cloud

print(f'-o-o-o- Graphs Saved -o-o-o-')

