The Journey

For each of the parts below, refer to the attached test cases to understand the expected behavior of the assistant.

Part 1: Building the Query Understanding Engine

Your first users are excited about having an AI assistant, but they quickly realize that getting good answers depends heavily on how questions are interpreted and processed. Let's build a smart query understanding system:

1. Create a Query Classifier

Build a prompt template that can categorize questions into types:

Factual Questions ("What is...?", "Who invented...?")

Analytical Questions ("How does...?", "Why do...?")

Comparison Questions ("What's the difference between...?")

Definition Requests ("Define...", "Explain...")

For consistent and reliable routing, the classifier must output only the category label (e.g., factual).

2. Design Response Templates

Create different prompt templates for each query type:

Factual answers should be concise and direct

Analytical responses should include reasoning steps

Comparisons should use structured formats (tables, bullet points)

Definitions should include examples and use cases

Implementation Tips:

Use LangChain only for the prompt and LLM call utilities:

ChatPromptTemplate class to create your classification and response prompt templates. It allows for more structured prompts with system and user messages.

Use StrOutputParser to keep outputs clean.

Use LangGraph for orchestration: Implement a simple router using conditional logic to direct queries to the right template.

Helpful Components:

Use conditional edges in LangGraph (as described in last week's demo) for selecting the right prompt based on the category.

LangChain’s ChatPromptTemplate: https://reference.langchain.com/python/langchain_core/prompts/

Output Parser (StrOutputParser): https://reference.langchain.com/python/langchain_core/output_parsers/

Remember: Focus on getting the basic query understanding working before moving to the next parts! This foundation will be crucial when we add tools and memory in the next parts!

Part 2: Introducing Simple Tools

User feedback after part 1: "The responses are much more organized now! I love how it gives me bullet points for comparisons and step-by-step explanations for 'how' questions. But it would be nice if it could help with calculations too..."

Users want more than just information - they need practical help with everyday tasks. In this part, we'll improve the assistant by:

Adding a calculator for handling mathematical questions performed by a simple calculator.

Create a smart router that knows when to use tools vs. simple responses as in part 1.

Remember: Tools should enhance, not complicate, the user experience. Start with simple calculations that add immediate value!

Implementation Tips:

Create a tool detection prompt to identify when calculations are needed.

If calculations are required, call the calculation tool.

NOTE 1: You don't need to implement your own calculator function/class, just re-use the one mentioned in tools/calculator.py.

NOTE 2: DO NOT use Agent related classes like AgentExecutor, create_react_agent etc. We'll be learning how to use them in the future assignments.

There are 2 ways of solving this part:

[Easy] Prompt LLM to provide a string which can then be passed to the tool. This way, you can use StrOutputParser and then call the tool to get the final answer.

[Hard] Using bind_tools approach. Refer to LangChain_LLM_Tool_Demo.ipynb Jupyter notebook provided as an aside in Google Drive here to learn a different paradigm of calling tools.

Bonus (For the adventurous😊):

Similar to Calculator, add a DateTime tool to handle time-related queries (e.g. "What is the date today?"). Since date/time queries can be complex, you can define a tool to run arbitrary python code and let LLM produce the Python code to answer the question.

Part 3: Making it Conversational with Memory

User feedback after part 2: "Great! It helps me calculate tips now. But I have to keep repeating my questions to provide context. It would be nice if it could remember our conversation history."

Until now, the assistant has been a bit robotic - calling an API for each question. Time to make your assistant feel more natural and context-aware:

Add conversation memory to track context

Make responses reference previous context where required to handle follow-up questions naturally.

Remember: Memory should feel natural - your assistant should use previous context only when it makes sense!

NOTE: For this part, we recommend you to manually construct the message history from the list provided in process_message function. LangChain officially recommends LangGraph/LangMem for tracking memory, which we'll be covering in next week's assignment.

Implementation Tips:

Use chat_history list provided in process_message function to manually construct message history.

Modify your prompt templates to include conversation history

Test with follow-up questions to ensure context is maintained

Start with short conversations (2-3 messages) before testing longer ones

Helpful LangChain Components:

[Recommended] Construct your own message history list from the input argument of process_message function.

Do not use Checkpointer module in LangGraph - we'll be covering this in later assignments with other forms of memory.

Final user feedback: "Now we're talking! It remembers our conversation context and can handle follow-up questions. It feels like talking to a real assistant!"

Example Interactions

Here's what your final implementation should handle:

User: "What is machine learning?"
Assistant: [Provides clear, concise explanation]

User: "Compare the benefits of using a SQL database vs. a NoSQL database."
Assistant: [Provides a structured comparison table]

User: "If I have a dinner bill of $120, what would be a 15% tip?"
Assistant: "Based on your $120 bill, a 15% tip would be $18, making your total $138."

User: "What about 20%?"
Assistant: [Uses previous context] "For your $120 bill, a 20% tip would be $24, bringing the total to $144."


Remember: Great products start simple and grow. Focus on getting the core functionality working well before adding complexity. Refer to the test cases file for a detailed list of expected interactions.

Remember that building AI systems is not just writing code but also coming up with possible examples and refining your system based on them.

Good luck! We're excited for you to be building this foundation of your AI search assistant.

Report Template

We created a report template here which is useful for documenting your learnings as you progress. Remember to chose the template written for LangGraph.

Update: NOTE: You do not need to submit anything! We'll release a full reference implementation one week later i.e. the next Saturday at 9AM PT.