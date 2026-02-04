# Reflection: Multi-Agent vs Single Agent Approach

When we started this project, we weren't sure if having multiple agents would be worth the extra architectural complexity. After building and testing the system, the advantages became clear.

### 1. Specialization Reduces Errors
The biggest win is **specialization**. Our Researcher agent is excellent at searching FAQs because that is its *only* job. Similarly, the Order Specialist focuses purely on database lookups. In our earlier single-agent experiments, the model would often get confused—mixing up return policies with shipping info or trying to "search" for an order when the user asked a general question. With specialized agents, each one "stays in its lane," resulting in much higher accuracy. It functions like a real team of experts rather than one overworked generalist.

### 2. The Power of "Reflection"
The **Quality Reviewer** agent proved to be the most valuable addition. Having a separate agent critique the response *before* it reaches the user caught many issues, such as raw database dumps or overly lengthy replies. A single agent often struggles to critique its own output effectively because it generates and evaluates in the same pass. The distinct reviewer acts as a fresh pair of eyes, mirroring real-world QA processes.

### 3. Debugging & Maintenance
Surprisingly, using multiple agents made debugging easier. When an answer was wrong, we could trace it to the specific agent responsible (e.g., "The Researcher found the wrong text" vs "The Reviewer formatted it badly"). In a monolithic single-agent system, debugging is often a black box of prompt engineering. Here, we could tune specifically the Researcher's prompt without breaking the Greeter.

### Only Downside: Coordination Overhead
The main trade-off is coordination. Orchestrating 6 agents required careful state management (passing context) and initially caused high latency. We solved this by implementing **routing logic** to skip unnecessary agents, which gave us the best of both worlds: the speed of a small team for simple tasks, and the power of the full crew for complex ones.
