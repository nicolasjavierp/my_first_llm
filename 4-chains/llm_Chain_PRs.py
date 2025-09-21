from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_ollama import ChatOllama
import logging
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

logging.basicConfig(level=logging.INFO)
my_logger = logging.getLogger(__name__)

model_name = "deepseek-r1:1.5b"
my_chat_model = ChatOllama(model=model_name, temperature=0) 

template_chain1 = "Summarize this review in 2-3 sentences: {review}"
prompt_chain1 = ChatPromptTemplate.from_template(template_chain1)

template_chain2 = "Identify the main weaknesses mentioned in this review: {review}"
prompt_chain2 = ChatPromptTemplate.from_template(template_chain2)

template_chain3 = """Based on this review summary: {review_summary}
And these identified weaknesses: {weaknesses}
Create an action plan to address the issues."""
prompt_chain3 = ChatPromptTemplate.from_template(template_chain3)

# LCEL Conversion with Parameter Preservation
class MultiOutputPreserver:
    def __init__(self):
        self.original_input = {}
        self.chain_outputs = {}
    
    def store_original_input(self, params):
        """Store the original input for later use"""
        self.original_input = params.copy()
        my_logger.info(f"=== STARTING SEQUENTIAL CHAIN ===")
        my_logger.info(f"Input: {params}")
        return params
    
    def store_chain1_output(self, chain1_response):
        """Store chain1 output and prepare for chain2"""
        self.chain_outputs['review_summary'] = chain1_response.content
        my_logger.info("=== CHAIN 1 COMPLETED: Review Summary ===")
        my_logger.info(f"Summary: {chain1_response.content}")
        
        # Return original input for chain2 (which also needs the review)
        return self.original_input
    
    def store_chain2_output(self, chain2_response):
        """Store chain2 output and prepare for chain3"""
        self.chain_outputs['weaknesses'] = chain2_response.content
        my_logger.info("=== CHAIN 2 COMPLETED: Weaknesses Identified ===")
        my_logger.info(f"Weaknesses: {chain2_response.content}")
        
        # Return both outputs for chain3
        return {
            'review_summary': self.chain_outputs['review_summary'],
            'weaknesses': self.chain_outputs['weaknesses']
        }
    
    def finalize_output(self, chain3_response):
        """Create final output with all results"""
        final_result = {
            'review_summary': self.chain_outputs['review_summary'],
            'weaknesses': self.chain_outputs['weaknesses'],
            'final_plan': chain3_response.content
        }
        my_logger.info("=== CHAIN 3 COMPLETED: Final Plan ===")
        my_logger.info(f"Plan: {chain3_response.content}")
        my_logger.info("=== SEQUENTIAL CHAIN COMPLETED ===")
        return final_result

# Create the preserver instance
output_preserver = MultiOutputPreserver()

# NEW LCEL Sequential Chain
seq_chain_lcel = (
    RunnableLambda(output_preserver.store_original_input)
    | prompt_chain1  # Review -> Summary
    | my_chat_model
    | RunnableLambda(output_preserver.store_chain1_output)
    | prompt_chain2  # Review -> Weaknesses
    | my_chat_model
    | RunnableLambda(output_preserver.store_chain2_output)
    | prompt_chain3  # Summary + Weaknesses -> Plan
    | my_chat_model
    | RunnableLambda(output_preserver.finalize_output)
)

streaming_handler = StreamingStdOutCallbackHandler()

sample_review = """
Mauricio consistently demonstrates dedication and a strong work ethic as a valued member of our team. He reliably resolves all assigned tickets and often proactively volunteers to help alleviate backlog pressures, showing his commitment. This unwavering reliability has been particularly valuable during challenging periods, demonstrating his resilience and positive contribution to team stability.

Technical Skill Development and Problem Solving
While Mauricio consistently tackles his assigned tasks and asks for help when needed, his technical skill development has shown limited growth during this period. He sometimes struggles initially with complex tasks, requiring significant ramp-up time to fully grasp the subject matter. However, once he achieves that comprehensive understanding, he typically excels in creating effective automation solutions for those specific problems. His contributions, though small in scope, are consistent.
It's important to consider his personal situation as a single parent with significant study commitments, which undoubtedly impacts his capacity for focused skill expansion.

Team Contributions and Future Growth
On a positive note, Mauricio's constructive contributions and feedback during our daily meetings are valuable. Despite the personal challenges he faces, his commitment to positive team dynamics remains evident.
In conclusion, Mauricio's performance reflects his strong work ethic and unwavering dedication to the team. He reliably ensures his responsibilities are met. However, to foster his continued professional development, he should prioritize a more focused approach to expanding his technical concepts and deepening his skills. Encouraging him to continue and even deepen his mentorship relationship is crucial to achieving previously established growth goals.
"""

result = seq_chain_lcel.invoke(
    {"review": sample_review},
    config={"callbacks": [streaming_handler]}
)

print("\n" + "="*50)
print("FINAL RESULTS:")
print("="*50)
print(f"Review Summary: {result['review_summary']}")
print(f"\nWeaknesses: {result['weaknesses']}")  
print(f"\nFinal Plan: {result['final_plan']}")

# ALTERNATIVE: Simpler approach if you want individual chain access
print("\n" + "="*50)
print("ALTERNATIVE: Step-by-step execution")
print("="*50)

# You can also run each step individually for more control:
def run_sequential_chains_manually(review_text):
    my_logger.info("=== Manual Sequential Execution ===")
    
    # Chain 1
    my_logger.info("Running Chain 1: Summarizing review...")
    chain1 = prompt_chain1 | my_chat_model
    summary_result = chain1.invoke({"review": review_text}, config={"callbacks": [streaming_handler]})
    review_summary = summary_result.content
    
    # Chain 2  
    my_logger.info("\nRunning Chain 2: Identifying weaknesses...")
    chain2 = prompt_chain2 | my_chat_model
    weakness_result = chain2.invoke({"review": review_text}, config={"callbacks": [streaming_handler]})
    weaknesses = weakness_result.content
    
    # Chain 3
    my_logger.info("\nRunning Chain 3: Creating action plan...")
    chain3 = prompt_chain3 | my_chat_model
    plan_result = chain3.invoke({
        "review_summary": review_summary,
        "weaknesses": weaknesses
    }, config={"callbacks": [streaming_handler]})
    final_plan = plan_result.content
    
    return {
        "review_summary": review_summary,
        "weaknesses": weaknesses, 
        "final_plan": final_plan
    }

# Run the manual version
manual_result = run_sequential_chains_manually(sample_review)
print(f"\nManual Result - Summary: {manual_result['review_summary'][:100]}...")
print(f"Manual Result - Weaknesses: {manual_result['weaknesses'][:100]}...")
print(f"Manual Result - Plan: {manual_result['final_plan'][:100]}...")