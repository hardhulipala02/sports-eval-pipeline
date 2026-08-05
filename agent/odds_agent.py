from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from mcp_server.sports_data_mcp import query_player_props

local_llm = ChatOllama(
    model="llama3.2",
    temperature=0.0
)

class MarketAnalysisResponse(BaseModel):
    target_event: str = Field(description="The player prop or game analyzed")
    retrieved_context: list[str] = Field(description="Sharp market data used")
    fair_line_recommendation: str = Field(description="Recommended zero-vig fair market price")
    risk_assessment: str = Field(description="Explanation of market exposure and risk")

# pydantic validation
structured_llm = local_llm.with_structured_output(MarketAnalysisResponse)

def analyze_sports_market(query: str) -> MarketAnalysisResponse:
    """Fetches FastMCP sports data and generates a structured market analysis."""
    context_text = query_player_props(query)
    
    prompt = f"""
    You are an automated Quantitative Market-Maker for a sports exchange.
    Analyze the provided market context for the Texas A&M vs Texas rivalry game and determine the zero-vig fair line.
    
    Market Context:
    {context_text}
    
    User Query: {query}
    """
    
    for attempt in range(3):
        try:
            parsed: MarketAnalysisResponse = structured_llm.invoke(prompt)
            parsed.target_event = query
            parsed.retrieved_context = [context_text]
            return parsed
        except Exception as e:
            print(f"[Retry {attempt + 1}] Output parsing failed: {e}")
            
    raise RuntimeError("Failed to generate valid market analysis locally.")