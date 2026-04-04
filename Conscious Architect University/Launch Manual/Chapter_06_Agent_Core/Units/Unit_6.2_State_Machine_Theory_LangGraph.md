# Unit 6.2: State Machine Theory — LangGraph

## 🧠 THE SCIENCE (148 words)

**UNLEARN:** Engineering agent intelligence does not follow a linear "A → B → C" pipeline. Linear thinking is a hallucination of the conveyor-belt era; in the agentic realm, information does not flow—it cycles. 

Think of the human brain's synaptic pruning and the hippocampal-neocortical loop. During memory consolidation (REM sleep), the hippocampus does not simply "copy" files to the neocortex. It initiates a cyclic dialogue—a back-and-forth "ping" of neural patterns. Information that fails the "relevance validation" is pruned or looped back for further refinement. This is why you remember the *meaning* of a conversation but prune the literal syntax.

In the CCP architecture, we reject the fragility of linear chains. If a validation gate (Sophia or Guardian) detects drift, the system must loop back to the generation node, not crash. LangGraph is the bridge that allows us to build these cyclic, self-correcting neural architectures, turning a "step-by-step" process into a living state machine.

## 🧠 TECHNICAL KNOWLEDGE (234 words)

At its systems level, LangGraph 0.3+ operates on four fundamental primitives that decouple execution logic from routing logic: Nodes, Edges, State, and Checkpointers.

1.  **Nodes (Compute):** A node is a discrete unit of computation (usually a Python function or a Pydantic AI agent). It takes the current `State` as input, performs an action (e.g., `aria_processor.py` extracting context), and returns an update to the state.
2.  **Edges (Routing):** Edges define the path between nodes. In LangGraph, we utilize **Conditional Edges** to implement the "OODA" logic. A routing function examines the state—specifically validation scores from ` sophia_ttt_validator.py`—and decides whether to move to the next stage or loop back.
3.  **State (Memory):** The `AgentState` is a shared, typed schema (typically a Pydantic `BaseModel`) that persists across node transitions. It acts as the "Short-Term Memory" of the graph, holding everything from raw transcripts to 12D context premises.
4.  **Checkpointers (Persistence):** This is the most critical primitive for the CCP's non-24/7 reality. Checkpointers (like `AsyncPostgresSaver`) save the entire state of the graph after every node execution. This allows an agent to "go to sleep" between scheduled voice sessions and "wake up" exactly where it left off, maintaining a durable thread of consciousness.

Failure to use a cyclic state machine results in "Cascading Context Collapse," where a single low-quality LLM output poisons every downstream node without the possibility of an automated retry.

## 📂 OUR CODE (182 words)

In our current codebase, we see the evolutionary transition between a manual OODA loop and a native LangGraph implementation.

Open `src/ccp/pipelines/cral_orchestrator.py`. Look at the `run()` method (line 476). You will notice it executes Stage 1, then a sequential loop for Stages 2+3, then Stage 4. This is a **manual state machine**. It handles error recovery using Python `try/except` blocks and `if/else` checks, but it lacks true cyclic persistence.

Compare this to `CBCS/backend/core/graph.py`. Here, we see the `StateGraph` in action:

```python
# CBCS/backend/core/graph.py, lines 198-214
workflow = StateGraph(AgentState)
workflow.add_node("listening", listening_node)
workflow.add_node("extraction", extraction_node)
workflow.add_node("processing", processing_node)

# The cyclic dependency: listening → extraction → processing → (script | END)
workflow.add_edge("listening", "extraction")
workflow.add_edge("extraction", "processing")
workflow.add_conditional_edges("processing", should_generate_script, {
    "script": "script",
    "end": END,
})
```

By defining nodes and conditional edges, we decouple the *what* (nodes) from the *when* (edges), allowing the `processing` node to trigger a specialized `script` node only when specific context thresholds are met.

## 🤖 AGENT PROMPT (124 words)

> **Prompt for Claude Code:**
> Assist in the architectural migration of `src/ccp/pipelines/cral_orchestrator.py` to a LangGraph-native `StateGraph`. 
> 
> 1. Read `src/ccp/pipelines/cral_orchestrator.py` and `CBCS/backend/core/graph.py`.
> 2. Create a new file at `src/ccp/pipelines/cral_graph.py` that wraps the 4 Stages of the CRAL OODA loop into LangGraph nodes: `init_node`, `research_node`, `assembly_node`.
> 3. Implement a `should_continue` conditional edge after `research_node` that checks `state.completed_count < 7`. If true, loop back to `research_node`. If false, move to `assembly_node`.
> 4. Use `src.ccp.models.cral_research_models.OODAState` as the basis for the `AgentState`.
> 5. Ensure `AsyncPostgresSaver` is configured for persistence.

## ⌨️ TERMINAL (86 words)

```bash
# Verify the LangGraph environment is live
pip list | grep langgraph
# Expected: langgraph 0.3.x

# Test the graph compilation for the CBCS graph
python -c "from CBCS.backend.core.graph import get_graph; g = get_graph(); print('Graph Compiled Successfully')"
# Expected: Graph Compiled Successfully

# Check the Postgres checkpointer status (requires local DB)
docker ps | grep postgres
# Expected: Up .. seconds ... postgres:16-alpine
```

## ✅ IMPLEMENTATION STEPS (165 words)

1. Open `src/ccp/pipelines/cral_orchestrator.py`. Trace the `_execute_moment_sequence` loop from line 204. Notice how it is bounded by a fixed Python `for` loop—this is the linear constraint we are breaking.
2. Open `CBCS/backend/core/graph.py`. Study the `StateGraph` definition starting at line 198. 
3. Map the OODA stages to the graph:
   - **Stage 1 (Init)** → `workflow.add_node("init", stage_1_node)`
   - **Stages 2/3 (Moment Execution)** → `workflow.add_node("moment_research", stage_2_3_node)`
   - **Stage 4 (Assembly)** → `workflow.add_node("assembly", stage_4_node)`
4. Identify the **Cyclic Edge**: In `cral_orchestrator.py`, if a moment fails, it simply logs an error. In a LangGraph implementation, you would add a conditional edge from `moment_research` back to itself with a `RetryStrategy` if an LLM failure is detected.
5. Paste the Agent Prompt from Section 4 into your Claude Code session to generate the `cral_graph.py` prototype.

## ✅ VERIFY (42 words)

Run `pytest CBCS/backend/tests/test_graph.py`. All tests must pass, confirming the LangGraph engine can successfully transition between `listening`, `extraction`, and `processing` nodes while maintaining `AgentState` integrity across the cycles.

## 🔗 BRIDGE (39 words)

Unit 6.3 builds on this "State Integrity" by introducing **Schema Enforcement with Pydantic AI**—teaching you how to ensure that the data being passed between graph nodes remains structurally perfect, even when the LLM is hallucinating.

<!-- FACT-CHECK: "LangGraph 0.3 features 2026" → LangGraph 0.3+ shifted higher-level abstractions to langgraph-prebuilt and introduced LangGraph Supervisor for multi-agent coordination. Persistence (AsyncPostgresSaver) and Cyclic State Graphs remain the core infrastructure for stateful agents. Verified April 2026. -->
