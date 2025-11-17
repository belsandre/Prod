Root folder: users/tam/hyperion
1. Ingest data room to be readable by LLMs - use `text-converter` skill on `raw`, output as `dataroom`
2. Prioritize deals to research - run `deals-prioritization` workflow on `dataroom`, output as `research/deals/priority-deals.md`
3. Research GPs and track record - run `vc-research` workflow, use `priority-deals.md` (to identify Tier 1 and Tier 2 deals) and `dataroom` (to identify the GPs)
	1. Need to run several times to complete given the amount of research and stochasticity of LLMs
	2. Resolve name conflict - run `conflict-resolver` to resolve name conflict between Scout vs Scout AI
	3. run validator workflow in users/tam/workflows to see if you followed instructions for company-research workflow
4. Construct a timeline & validate main marketing claims - Use the `timeline-constructor` skill on `dataroom` and `research` folders. output to `outputs` folder
5. Scrape Dillon's LinkedIn connections in VCPE - Run the `linkedin-to-csv` workflow on https://www.linkedin.com/search/results/people/?origin=FACETED_SEARCH&network=%5B%22F%22%2C%22S%22%5D&industry=%5B%22106%22%5D&connectionOf=%22ACoAAB0Y8lABYY5QRgDrmyqPEy8oVtta973NiHo%22&page=63&spellCorrectionEnabled=true for pages 1-x, output to `research/people/linkedin/connections_vcpe.csv`
	1. Split Title into Firm and Role - Run the `linkedin-csv-processor` workflow on `connections_vcpe.csv`
6. Run the `reference-identifier` workflow on dataroom, output as `outputs/reference-check-targets.md` and `outputs/investor-mentions-map.csv`
	1. Add names from LinkedIn connections - Run the `reference-linkedin-checker` workflow on `research/people/linkedin/connections_vcpe.csv`, update `outputs/reference-check-targets.md` and `outputs/investor-mentions-map.csv`
7. Run network analysis to classify network into early, mid, late-stage VC, PE, LPs, etc. - run `network-analyzer` workflow on `research/people/linkedin/connections_vcpe.csv`, output as `outputs/network_analysis.md`
8. Network analysis
	1. LinkedIn search with all Harvard alums = ~600 connections -> output as connections_harvard.csv
	2. LinkedIn search with Industries = Computer and Network Security, Semiconductor Manufacturing, Automation Machinery Manufacturing, Renewable Energy Semiconductor Manufacturing, Computers and Electronics Manufacturing, Biotechnology Research, Utilities, Mining, Research Services, Appliances, Electrical and Electronics Manufacturing, Machinery Manufacturing, Oil and Gas, Computer Hardware Manufacturing, Software Development, Nanotechnology Research, Chemical Manufacturing, Computer Networking Products -> ~380 connections
		1. Informed by `linkedin-industry-analysis` workflow
		2. outputs as connections_deeptech.csv