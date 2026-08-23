import sys, os

sys.path.insert( 0, os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) )

from deepeval.evaluate import evaluate
from deepeval.metrics import TurnRelevancyMetric, KnowledgeRetentionMetric, ConversationCompletenessMetric
from deepeval.test_case import ConversationalTestCase, Turn


from chatbot import chat

turns = []
history = []
for user_msg in [
        "Hi! I placed an order last week, the order ID is ORD-1042.",

        "Is it going to arrive on time?",
        "What was the ETA you just mentioned?",   # tests memory retention
        "Can I upgrade to express shipping?",
    ]:
       reply,history, _  = chat(user_msg,history)
       turns.append(Turn(role="user",content=user_msg))
       turns.append(Turn(role="assistant",content=reply))

turnRelevancyMetric = TurnRelevancyMetric(threshold=0.5)
retentionMetric = KnowledgeRetentionMetric(threshold=0.5)
completenessMetric = ConversationCompletenessMetric(threshold=0.5)


# ConversionalTestCase is for multi turn (meaning conversion is more than one step and it is ideal for chatbot automation)
test_case = ConversationalTestCase(
    turns = turns
)

evaluate(test_cases = [test_case], metrics = [turnRelevancyMetric,retentionMetric,completenessMetric])

""" 
Important Metric for chatbot automation:
    1. Turn Relevancy : Conversational metric that determines if LLM chatbot is able to consistently generate relevant responses throughout a conversation
    2. Knowledge Retention : Conversational metric that determines whether LLM chatbot is able to retain factual information presented throughout a conversation.
    3. Conversation Completeness : Conversational metric that determines whether LLM chatbot is able to complete an end to end conversation by satisfying user needs.

"""