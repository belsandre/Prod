# LinkedIn Posts - Seidman Episode (David Seidman)

## Variation 1: Personal Discovery Angle

I just heard something that made me rethink everything about SOC operations.

David Seidman, who leads platform security at Plaid after 20 years at Microsoft, Google, Salesforce, and Robinhood, told me something I wasn't prepared for: "If this was 2015, I would have hired SOC analysts. Because there's an AI option now, I haven't hired those people, and it doesn't look like we're going to need to."

Jobs are already being eliminated. Not in the future. Today.

But here's what actually surprised me about our conversation. The AI SOC tools David's team has been testing can take a security alert that would normally require 30-60 minutes of human analysis and reduce it to a 30-second review. They saw essentially zero instances where the AI came to the wrong conclusion.

The technology isn't just promising anymore. It's working.

But the implications go way beyond faster alert triage. David walked me through a future that's only 3-5 years away: AI generates 10,000 detection rules automatically. Those rules create tons of false positives. Another AI layer eliminates virtually all of those false positives before they reach humans.

The result? Security teams finally get comprehensive threat coverage instead of having to pick and choose which attacks to detect.

The open secret he shared: Even very mature organizations frequently fail to detect their own red team. Detection today is just really not very good. AI might actually fix that at a fundamental level.

We also covered the darker side. The vulnerability cataclysm theory from researchers like Bruce Schneier and Heather Adkins. When AI makes finding and exploiting zero-days trivial, we're facing an industry-wide fire drill. The good news? Defenders have a temporary lead time. The bad news? It could be years, months, or days.

In this episode, David breaks down what's hype versus what's real, why Tier 1 analyst jobs are disappearing permanently, and how product security will go from 20% coverage to 100% coverage with AI reviews.

This is one of the most honest conversations I've had about AI in security. No vendor pitches. Just a practitioner telling you what's actually working in production.

Link in comments if you're in security operations or thinking about the future of the field.

#cybersecurity #SOC #AI #securityoperations #threatdetection

**Character count:** 2,083

---

## Variation 2: Contrarian/Surprising Angle

The AI SOC is not coming.

It's already here.

David Seidman, Head of Platform Security at Plaid, just finished running POCs on AI SOC tools. His team saw essentially no instances where the AI came to the wrong conclusion when triaging security alerts.

Zero wrong conclusions in their testing.

Here's what that means: A task that takes humans 30-60 minutes now takes 30 seconds for an AI to complete. The technology can run every query you'd think to run, perform effective analysis, and give you an accurate summary.

But everyone's asking the wrong question about AI in security.

The question isn't "Will AI replace humans?" The question is "What happens when AI makes both attack and defense dramatically cheaper?"

David explained something I haven't heard anyone else talk about: We're in a race. Security code review tools using AI are widely available today. AI vulnerability discovery and exploitation tools are not widely available yet.

Defenders have a temporary lead. How long? Could be years. Could be months. Could be days.

When those exploitation tools become accessible (and they will, thanks to open source and competitive pressure), we hit what researchers call the "vulnerability cataclysm." AI will discover zero-days, turn them into exploits, and orchestrate attack campaigns with minimal human skill required.

The result? An industry-wide fire drill. Everyone scrambling to fix vulnerabilities. Then afterward, a completely transformed security landscape where vulnerabilities become rare and hard to find.

The counterintuitive insight: Even mediocre AI security reviews are transformative. Not because they're better than humans (they're not). But because they can review 100% of code from day one, while humans can only review about 20% of what ships.

100% mediocre beats 20% excellent when the alternative is 80% never gets reviewed at all.

David also didn't sugarcoat the job displacement reality. Tier 1 SOC analyst positions are already being eliminated. If this was 2015, Plaid would have hired multiple SOC analysts. They haven't hired any. Because of AI, they don't need to.

We covered what's actually working in production today, what's still hype, how large companies (Google/Microsoft) differ from smaller companies (Plaid/Robinhood), and why LinkedIn comments are the only place on the internet worth reading.

This conversation will change how you think about the next 3-5 years in security.

#security #AI #cybersecurity #SOC #futureofwork

**Character count:** 2,258

---

## Variation 3: Practical/Actionable Angle

We just eliminated multiple SOC analyst positions before we ever hired them.

That's the reality David Seidman shared with me. As Head of Platform Security at Plaid, he would have hired SOC analysts in 2015. But in 2024, AI SOC tools made those positions unnecessary.

If you're running security operations, here's what's actually working in production right now:

**AI Alert Triage** - Already here. Tools can analyze security alerts, run all relevant queries, and produce accurate summaries in 30 seconds instead of 30-60 minutes. In David's POC testing, they saw essentially zero wrong conclusions from the AI.

**AI Threat Intelligence** - Already here. An intern at Robinhood automated the entire process of finding applicable threat intelligence from open source feeds in 3 weeks using foundational ChatGPT APIs.

**AI Rule Generation** - Coming soon (in progress). The companies David's team is working with can auto-generate detection rules. Combined with AI SOC, you could generate 10,000 rules, accept the high false positive rate, and let AI eliminate those false positives before humans see them.

The practical implication: Security teams might finally achieve comprehensive threat coverage instead of picking and choosing which attacks to detect.

But here's the honest part nobody's talking about. The limitations aren't AI science problems. They're basic engineering: deployment, configuration, log ingestion, permission management. Those will get solved because we know how to do that engineering work.

For product security, the transformation is even more dramatic. David's seeing AI tools that can do security code review on 100% of code from day one. Is it better than a human? No. Humans still do better reviews. But AI can scale to review everything, while humans only review about 20% of what ships.

The math: 100% mediocre coverage beats 20% excellent coverage when the alternative is 80% gets zero review.

One critical detail: AI product security tools are better than existing SaaS scanning tools in many cases. But each vendor is only good in a narrow slice. Different code types, different security problems. Buying all of them is too expensive even for well-resourced organizations. That will improve over time.

The vulnerability cataclysm risk: AI vulnerability discovery tools will become publicly available. Attackers will get them for free. When that happens, we'll face an industry-wide fire drill with widespread zero-day exploitation. Defenders have a temporary lead time. It could be years, months, or days. Nobody knows.

In our conversation, David covers what's real versus what's hype, why legacy vendors are just slapping AI on query translation, how to think about the job displacement happening today, and the security risks of prompt injection in agentic AI deployment.

Highly practical for anyone making AI security tool decisions or planning SOC staffing.

Link in comments.

#cybersecurity #SOC #security #AI #secops

**Character count:** 2,524

---

## Variation 4: Big Picture/Industry Trend Angle

In 3 to 5 years, security operations will be unrecognizable.

I just talked to David Seidman, who's spent 20 years in security across Microsoft, Google, Salesforce, Robinhood, and now Plaid. His prediction: The field is transforming faster than most people realize.

The pattern he's seeing: AI is changing both sides of the security equation simultaneously.

**The Defense Transformation:**

AI SOC tools can already triage alerts with essentially zero wrong conclusions. 30-60 minute tasks become 30-second reviews. This isn't theoretical. David's team tested this in production POCs.

More important: The combination of AI rule generation plus AI SOC creates a completely new capability. Generate 10,000 detection rules automatically. Let them create high false positives. Use AI to eliminate those false positives before humans see them.

The result is something the industry has never had: comprehensive threat coverage. Today, even the most mature organizations fail to detect their own red team. Detection is just not very good. AI might fundamentally change that.

On the product security side, AI enables 100% coverage of security code reviews from day one of development. Not because AI is better than humans (it's not). But because AI can scale to review everything, while humans only review about 20% of what ships.

**The Attack Transformation:**

The vulnerability cataclysm is coming. Researchers like Bruce Schneier, Heather Adkins, and Gotti Everon are warning about an inflection point where AI makes vulnerability discovery, exploitation, and attack orchestration trivial.

When that happens, we'll see widespread exploitation of new zero-days. An industry-wide fire drill. Everyone scrambling to patch. Then a completely different security landscape where vulnerabilities become rare and hard to find.

Right now, defenders have a lead. Security code review tools are widely available. AI exploitation tools are not. But that lead could disappear in years, months, or days. Open source models and competitive pressure mean no single company can keep this technology locked down.

**The Job Displacement Reality:**

David was brutally honest. Tier 1 SOC analyst jobs are already being eliminated. If this was 2015, Plaid would have hired multiple analysts. They haven't hired any. The AI SOC option made those positions unnecessary.

The pattern: Where human work has been codified into playbooks, AI can replicate it. Tier 1 follows playbooks. Tier 2 and 3 do work that's not fully codified yet. But AI is increasingly capable of even Tier 3 work.

The limiting factor saving jobs isn't AI capability. It's slow corporate deployment cycles.

**The Scale Insight:**

Large companies (Google, Microsoft, Salesforce) have to build everything themselves because their needs are weird and their scale is immense. Small companies (Plaid, Robinhood) can buy off-the-shelf vendor solutions because their needs are simpler and their infrastructure is more modern.

This changes how AI security tools get adopted. Large companies will build custom AI solutions. Small companies will accelerate vendor adoption.

We covered what's actually working today versus what's still hype, why every AI marketing claim needs to be deflated, the unsolved problems like prompt injection, and why LinkedIn is the only place on the internet where reading comments is worthwhile.

This is the most comprehensive, honest look at AI's impact on security operations I've encountered. No vendor spin. Just a practitioner with 20 years of experience telling you what's real.

Link in comments for the full conversation.

#cybersecurity #AI #futureofwork #security #transformation

**Character count:** 3,280 (Note: Longer than optimal, but packed with insights. Could trim if needed.)

---

## Notes

- All posts written from host perspective (Chang/Ashish)
- No em dashes used
- Strong opening hooks on each variation
- Different angles: personal/surprising, contrarian/dark, practical, comprehensive trend analysis
- Seidman's brutal honesty about job displacement preserved
- Variation 4 is longer but comprehensive (can be trimmed if needed)
- Ready to post with minimal edits
