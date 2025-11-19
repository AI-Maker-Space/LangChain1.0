<p align="center" draggable="false">
<img src="https://blog.langchain.com/content/images/2025/10/LangChain-1.0-Blog-Header.png" width="600px" height="auto"/>
</p>

# LangChain 1.0 Guide & RAG Demo

A comprehensive guide and demonstration of **LangChain 1.0** features, including the new `create_agent` workflow, Human-in-the-Loop (HITL) middleware, and Multi-Agent systems.

This project also includes a RAG pipeline that ingests the official [LangChain 1.0 announcement blog post](https://blog.langchain.com/langchain-langgraph-1dot0/) to answer questions about the framework updates.

## Features Covered

*   **Standard Agents**: Using `create_agent` with custom tools.
*   **Human-in-the-Loop**: Pausing execution for approval using `HumanInTheLoopMiddleware`.
*   **RAG**: Integrating `Qdrant` and `OpenAIEmbeddings` to query external documents.
*   **Multi-Agent Orchestration**: Composing agents (Supervisor -> Researcher + Writer).

## Pre-Reqs

You'll need to ensure you have [uv installed](https://docs.astral.sh/uv/getting-started/installation/) before proceeding.

```bash
# Install dependencies
uv sync
```

You will also need an **OpenAI API Key** (`OPENAI_API_KEY`).

## Running the Example

The core logic is in the `src/` directory, but the best way to explore is via the Jupyter Notebook.

1.  **Launch the Notebook**:
    ```bash
    uv run jupyter notebook langchain_v1_0_guide.ipynb
    ```

2.  **Run the Cells**:
    *   The notebook will guide you through setting up your environment.
    *   It will demonstrate a simple agent, then a HITL agent, then a RAG agent, and finally a Multi-Agent system.

## Project Structure

*   `src/agent.py`: Contains the agent construction logic (`create_agent`, middleware setup).
*   `src/rag.py`: Handles the RAG pipeline (loading the blog post, chunking, vector store).
*   `src/tools.py`: Simple example tools (`get_weather`, `magic_calculator`).
*   `langchain_v1_0_guide.ipynb`: The interactive guide.
*   `pyproject.toml`: Dependency management.
*   `langgraph.json`: Configuration for deploying through LangSmith.

## Deploy with LangSmith

LangSmith is the fastest way to turn agents into production systems.

### 1. Prerequisites
*   A [GitHub account](https://github.com/)
*   A [LangSmith account](https://smith.langchain.com/)

### 2. Create a Repository
Your application's code must reside in a GitHub repository. Push this code to a new repository.

### 3. Deploy
1.  Go to [LangSmith](https://smith.langchain.com/) and navigate to the **Deployments** tab.
2.  Click **+ New Deployment**.
3.  Connect your GitHub repository.
4.  LangSmith will detect the `langgraph.json` file and automatically configure your deployment.
    *   **Entrypoint**: `langgraph.json` defines multiple graphs (`agent`, `hitl_agent`, `rag_agent`, `multi_agent`). You can choose which one to expose or deploy them all.
5.  Set your environment variables (e.g., `OPENAI_API_KEY`) in the deployment settings.
6.  Click **Deploy**.

Once deployed, you can interact with your agent via the LangSmith Studio, API, or SDK.

## Credits

Built using [LangChain](https://www.langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/).
