from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
# Note: The following import is based on LangChain 1.0 docs. 
# If running on older versions, this might be 'from langgraph.prebuilt import create_react_agent'
# and HITL might be handled via 'interrupt_before' in compile().
try:
    from langchain.agents.middleware import HumanInTheLoopMiddleware
except ImportError:
    # Fallback or placeholder if specifically using a different version
    HumanInTheLoopMiddleware = None

from langgraph.checkpoint.memory import MemorySaver
from src.tools import get_weather, magic_calculator
from src.rag import setup_rag_tools

def get_model():
    return ChatOpenAI(model="gpt-4o", temperature=0)

def build_simple_agent():
    """Creates a simple agent with basic tools."""
    model = get_model()
    tools = [get_weather, magic_calculator]
    
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="You are a helpful assistant."
    )
    return agent

def build_hitl_agent():
    """Creates an agent with Human-in-the-Loop for sensitive tools."""
    model = get_model()
    tools = [get_weather, magic_calculator]
    
    # Configure HITL to interrupt before 'magic_calculator'
    # In LangChain 1.0, this is done via middleware
    if HumanInTheLoopMiddleware:
        middleware = [
            HumanInTheLoopMiddleware(
                interrupt_on={"magic_calculator": True}
            )
        ]
    else:
        middleware = []
        print("Warning: HumanInTheLoopMiddleware not found. HITL might not work as expected.")

    checkpointer = MemorySaver()
    
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="You are a helpful assistant. You must ask for permission (implicitly handled) before doing math.",
        middleware=middleware,
        checkpointer=checkpointer
    )
    return agent

async def build_rag_agent():
    """Creates an agent with RAG capabilities."""
    model = get_model()
    
    # Setup RAG tools
    try:
        rag_tools = await setup_rag_tools()
    except Exception as e:
        print(f"Failed to setup RAG tools (likely missing keys): {e}")
        rag_tools = []
        
    tools = [get_weather, magic_calculator] + rag_tools
    
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="You are a helpful assistant. Use the search_langchain_updates tool to answer questions about the LangChain 1.0 release."
    )
    return agent

async def build_multi_agent_system():
    """
    Demonstrates a simple multi-agent setup.
    We create a 'Researcher' and a 'Writer' and a 'Supervisor' to manage them.
    In LangChain 1.0, since agents are graphs, we can use them as tools.
    """
    model = get_model()
    
    # 1. Researcher Agent
    rag_tools = []
    try:
        rag_tools = await setup_rag_tools()
    except:
        pass
        
    researcher = create_agent(
        model=model,
        tools=rag_tools,
        system_prompt="You are a researcher. Search for facts about LangChain 1.0 and report them accurately."
    )
    
    # 2. Writer Agent
    writer = create_agent(
        model=model,
        tools=[], # Writer just writes, maybe has some basic tools
        system_prompt="You are a writer. specific style: Tech Blog. Use facts provided by the user."
    )
    
    # To compose them, we can wrap them as tools for a Supervisor
    # Or use LangGraph's supervisor pattern. 
    # For simplicity in this 'create_agent' centric demo, we will treat them as tools.
    
    from langchain_core.tools import tool

    @tool
    def ask_researcher(query: str) -> str:
        """Ask the researcher to find information."""
        result = researcher.invoke({"messages": [{"role": "user", "content": query}]})
        return result["messages"][-1].content

    @tool
    def ask_writer(topic: str, content: str) -> str:
        """Ask the writer to write about a topic using provided content."""
        prompt = f"Topic: {topic}\nContent: {content}"
        result = writer.invoke({"messages": [{"role": "user", "content": prompt}]})
        return result["messages"][-1].content

    supervisor_tools = [ask_researcher, ask_writer]
    
    supervisor = create_agent(
        model=model,
        tools=supervisor_tools,
        system_prompt="""You are a supervisor. 
        1. Ask the researcher for info. 
        2. Then ask the writer to write a post based on that info.
        """
    )
    
    return supervisor
