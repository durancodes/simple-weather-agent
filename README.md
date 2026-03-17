
# A Simple Weather Agent

This project implements a strict, tool-driven AI agent designed to demonstrate agentic AI principles rather than traditional chatbot behavior.

The system enforces a clear separation of responsibilities:

The LLM is used only for reasoning

All real-world data is fetched through deterministic Python tools

Execution control is handled by code, not the model

The agent follows an explicit Thought → Action → Observation → Final Answer loop, ensuring that responses are generated only after observing authoritative tool output. This design prevents hallucinations and makes the system deterministic, auditable, and debuggable.

The project also explores a key challenge in agentic AI:
LLMs may still infer or enrich information unless architectural boundaries are enforced. Addressing this reinforced the importance of tool-first design over prompt-only constraints.

This project reflects a shift from prompt engineering to agent engineering, focusing on internal decision loops, execution control, and reliability in real-world AI systems.

This project implements a strict, tool-driven AI agent designed to demonstrate agentic AI principles rather than traditional chatbot behavior. The system enforces a clear separation of responsibilities: The LLM is used only for reasoning All real-world data is fetched through deterministic Python tools Execution control is handled by code, not the model The agent follows an explicit Thought → Action → Observation → Final Answer loop, ensuring that responses are generated only after observing authoritative tool output. This design prevents hallucinations and makes the system deterministic, auditable, and debuggable. The project also explores a key challenge in agentic AI: LLMs may still infer or enrich information unless architectural boundaries are enforced. Addressing this reinforced the importance of tool-first design over prompt-only constraints.

This project reflects a shift from prompt engineering to agent engineering, focusing on internal decision loops, execution control, and reliability in real-world AI systems.

Skills: Python (Programming Language) · Hugging Face

<img width="527" height="246" alt="image" src="https://github.com/user-attachments/assets/a987fa37-f088-46f2-be35-b7596bd5c25d" />

