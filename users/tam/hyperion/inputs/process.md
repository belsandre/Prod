Root folder: users/tam/hyperion
1. Ingest data room to be readable by LLMs - use `text-converter` skill on `raw`, output as `dataroom`
2. Prioritize deals to research - run `deals-prioritization` workflow on `dataroom`, output as `research/deals/priority-deals.md`
3. Research GPs and track record - run `vc-research` workflow, use `priority-deals.md` (to identify Tier 1 and Tier 2 deals) and `dataroom` (to identify the GPs)
	1. Need to run several times to complete given the amount of research and stochasticity of LLMs
	2. Resolve name conflict - run `conflict-resolver` to resolve name conflict between Scout vs Scout AI
	3. run validator workflow in users/tam/workflows to see if you followed instructions for company-research workflow
4. use the `timeline-constructor` skill on `dataroom` and `research` folders. output to `outputs` folder