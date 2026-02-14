"""Part 1 - Query Understanding implementation.

This implementation focuses on:
- Classify different types of questions
- Format responses based on query type
- Present information professionally
"""

from enum import Enum
from typing import Dict, List, Optional, TypedDict

from perplexia_ai.core.chat_interface import ChatInterface

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END

class QueryType(str,Enum):
    FACTUAL = "factual"
    ANALYTICAL = "analytical"
    COMPARISON = "comparison"
    DEFINITION = "definition"
    OTHER = "other"

class State(TypedDict):
    message: str
    query_type: QueryType
    response: str

class QueryUnderstandingChat(ChatInterface):
    """Week 1 Part 1 implementation focusing on query understanding."""
    
    def __init__(self):
        self.llm = None
        self.query_classifier_prompt = None
        self.response_prompts = {}
    
    def initialize(self) -> None:
        """Initialize components for query understanding.
        
        Students should:
        - Initialize the chat model
        - Set up query classification prompts
        - Set up response formatting prompts
        """
        # TODO: Students implement initialization
        
        load_dotenv()

        self.llm = init_chat_model(
            "gpt-5-mini", 
            model_provider="openai", 
            reasoning_effort="minimal"
        )
        self.parser = StrOutputParser()

        graph_builder = StateGraph(State)
        graph_builder.add_node("classify_query", self.classify_query)
        graph_builder.add_node("factual_response", self.factual_response)
        graph_builder.add_node("analytical_response", self.analytical_response)
        graph_builder.add_node("comparison_response", self.comparison_response)
        graph_builder.add_node("definition_response", self.definition_response)
        graph_builder.add_node("other_response", self.other_response)

        graph_builder.add_edge(START, "classify_query")
        graph_builder.add_conditional_edges(
            "classify_query",
            lambda state: state["query_type"],
            {
                QueryType.FACTUAL: "factual_response",
                QueryType.ANALYTICAL: "analytical_response",
                QueryType.COMPARISON: "comparison_response",
                QueryType.DEFINITION: "definition_response",
                QueryType.OTHER: "other_response",
            }
        )
        graph_builder.add_edge("factual_response", END)
        graph_builder.add_edge("analytical_response", END)
        graph_builder.add_edge("comparison_response", END)
        graph_builder.add_edge("definition_response", END)
        graph_builder.add_edge("other_response", END)

        self.graph = graph_builder.compile()

    def classify_query(self, state: State):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Classify the query into exactly one label: factual, analytical, comparison, definition, other.  Return only the lowercase label with no punctuation or extra text."),
            ("user", "{message}"),
        ])
        chain = prompt | self.llm | self.parser
        result = chain.invoke({"message": state["message"]}).strip().lower()
        if result not in {q.value for q in QueryType}:
            return {"query_type": QueryType.OTHER.value}
        return {"query_type": QueryType(result)}

    def factual_response(self, state: State):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Provide a concise and direct answer to the question."),
            ("user", "{message}"),
        ])
        chain = prompt | self.llm | self.parser
        result = chain.invoke({"message": state["message"]})
        return {"response": result}

    def analytical_response(self, state: State):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Provide a detailed and reasoned answer to the question."),
            ("user", "{message}"),
        ])
        chain = prompt | self.llm | self.parser
        result = chain.invoke({"message": state["message"]})
        return {"response": result}

    def comparison_response(self, state: State):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Provide a structured comparison of the two items."),
            ("user", "{message}"),
        ])
        chain = prompt | self.llm | self.parser
        result = chain.invoke({"message": state["message"]})
        return {"response": result}

    def definition_response(self, state: State):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Provide a detailed definition of the term."),
            ("user", "{message}"),
        ])
        chain = prompt | self.llm | self.parser
        result = chain.invoke({"message": state["message"]})
        return {"response": result}

    def other_response(self, state: State):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Provide a generic response to the question."),
            ("user", "{message}"),
        ])
        chain = prompt | self.llm | self.parser
        result = chain.invoke({"message": state["message"]})
        return {"response": result}

    def process_message(self, message: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Process a message using query understanding.
        
        Students should:
        - Classify the query type
        - Generate appropriate response
        - Format based on query type
        
        Args:
            message: The user's input message
            chat_history: Not used in Part 1
            
        Returns:
            str: The assistant's response
        """
        # TODO: Students implement query understanding

        result = self.graph.invoke({"message": message})

        return result["response"]