import sys, os

sys.path.insert( 0, os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )

from deepeval.contextvars import get_current_golden
from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import TaskCompletionMetric, ToolCorrectnessMetric
from deepeval.test_case import ToolCall
from deepeval.tracing import observe, update_current_trace




from agent_instrumented import support_agent as _support_agent
#Trace have expected values and actual values - Track every activity of the agent and give the result
@observe(name="support_agent")  #tracing is initiated and tracing context is also sent together while we call this
def support_agent(user_input: str) -> str:  #overriding the behavior of the original agent
    golden = get_current_golden()
    if golden:
        if golden.expected_tools:
            update_current_trace( expected_tools=golden.expected_tools )
        if golden.expected_output:
            update_current_trace( expected_output=golden.expected_output )

    return _support_agent( user_input )



# Initialize the metric
task_completion = TaskCompletionMetric(threshold=0.7,model="gpt-4o")

# Initialize the Toolcorrectness metric, we do no need argument here because we need which tool/function it should call exactly
tool_correctness = ToolCorrectnessMetric()

#Create Dataset - Array of the testdata sets
dataSet = EvaluationDataset(goldens= [
    Golden(input = "Where is my order ORD-1042?",
           expected_tools=[ToolCall(name="get_order_status")]), #one Golden object

    Golden(input = "What is refund policy for electronics?",
           expected_tools=[ToolCall(name="get_refund_policy")]) #Second Golden Object
])

# loop through dataset with metrics include task completion and tool correctness
for golden in dataSet.evals_iterator(metrics =[task_completion,tool_correctness]):
    support_agent(golden.input)

