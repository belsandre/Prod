# LinkedIn Post Variations - AI Security Podcast

**Episode:** The Def Podcast with Sandy Dun (SPLX)
**Host Perspective:** Ashish Popley
**Date Generated:** 2025-01-12

---

## Variation 1: Personal Story Angle

Most CISOs are having the wrong conversation with their boards.

I just recorded an episode with Sandy Dun from SPLX, and she completely reframed how I think about AI security risk communication.

Here's what hit me hardest: We've been trying to give boards binary answers (secure vs. not secure) in a world that's fundamentally statistical. Sandy put it perfectly: "It was really a statistical conversation before. We just weren't honest about it."

She told me about the "Smoky the Bear" approach. Simple fire danger signs. High, medium, low. That's what boards actually need. Not 47-slide decks about prompt injection vectors.

But here's the twist. AI is forcing us to have these honest conversations because the math literally doesn't work anymore. You can't audit every model behavior. You can't test every edge case. It's mathematically impossible.

So what do you do? You become what you always were: a risk manager having investment conversations, not a cost center defending against unknown threats.

The episode goes deep on how Sandy helped build SPLX's approach to this problem, including why they test prompts 200 times and what "prompting in Navajo" tells you about attacker behavior.

Link to full episode in comments. Essential listening if you're building or securing AI systems.

#aisecurity #ciso #enterpriserisk

**Character Count:** 1,247
**Word Count:** 214

---

## Variation 2: Contrarian/Surprising Angle

Attackers aren't trying to jailbreak your AI models.

At least not yet. And that's the part everyone's getting wrong about AI security.

Sandy Dun from SPLX just walked me through why all the research on prompt injection and adversarial attacks is real, but not what's actually happening in production today.

The truth? Adversaries are using AI the same way your developers are. For reconnaissance. For vulnerability research. For converting legacy code. The attack surface hasn't changed. Just the speed.

Zero-day exploitation used to take months. Now it's 24 hours.

Supply chain attacks used to require sophisticated coordination. Now AI makes it trivial to scan dependencies and find backdoors.

Sandy's line that stuck with me: "AI is here to help previous workflows, not create new workflows yet."

So while everyone's worried about exotic model attacks, the npm registry is getting compromised and CrowdStrike is getting hit with supply chain vulnerabilities. Traditional attacks, AI-accelerated speed.

The episode covers what SPLX learned from actually testing production systems (spoiler: they had to run one test 200 times because of non-deterministic behavior) and why runtime monitoring beats guardrails.

Worth your 45 minutes. Link in comments.

#cybersecurity #ai #supplychain

**Character Count:** 1,336
**Word Count:** 213

---

## Variation 3: Practical/Actionable Angle

Three things every CISO needs to know about AI security right now.

Just wrapped a conversation with Sandy Dun (SPLX, OWASP AI Security lead, 20+ years in the field) and these are the takeaways you can actually use on Monday morning:

**1. Stop trying to achieve binary security metrics.**
With AI, you're in the statistical realm whether you admit it or not. The attack surface is too large. Governance at the core level is mathematically impossible. Start communicating in probabilities and investment trade-offs.

**2. Focus on runtime detection, not just guardrails.**
Sandy's team found that over-aggressive guardrails just push users to unprotected models (she literally went to Hugging Face to bypass corporate restrictions). Better strategy: light guardrails + behavioral anomaly detection. If someone's prompting in Navajo for your healthcare chatbot, that's a flag.

**3. Speed is your only sustainable advantage.**
The OODA loop applies to security now. Observe, orient, decide, act. Faster than your adversaries. That means rethinking approval processes, legal reviews, and how quickly you can deploy fixes.

Sandy also dropped this gem: "Throwing AI on top of broken digital infrastructure is like lighting a match in a gasoline factory."

So if you're rushing to deploy AI, maybe fix your asset management and data catalog first.

The full conversation covers SPLX's approach to context-aware AI red teaming, why they test prompts hundreds of times, and how to communicate AI risk to boards using the "Smoky the Bear" framework.

Link in comments.

#aisecurity #practicaladvice #ciso

**Character Count:** 1,576
**Word Count:** 253

---

## Variation 4: Big Picture/Trend Angle

We're at the exact moment in AI security that we were in 2000 for application security.

Everything looks overwhelming. The attack surface seems infinite. Everyone's trying to solve it with binary answers that don't scale.

Sandy Dun just reminded me of this during our Def Podcast recording, and it completely shifted my perspective.

Back in 2000, we were building static code analysis for Java web apps, trying to find XSS and SQL injection in first-party code. Meanwhile, we were pulling in hundreds of third and fourth-party libraries. The scope felt impossible.

Sound familiar?

Today it's AI models, training data provenance, supply chain attacks on npm packages, and the "Lego nature" of modern code stacks. CrowdStrike gets hit. Open source gets compromised. And we're still trying to patch Log4j instances buried six layers deep.

Here's what changed in application security: We stopped trying to secure everything and started thinking in terms of risk appetite and crown jewels. We got honest about statistical probability instead of pretending we had complete coverage.

Sandy argues AI is forcing the same evolution, but faster. Because the speed differential is insane. Zero-days go from discovery to exploitation in 24 hours now. Decision cycles have to match that pace.

The conversation goes deep on how SPLX approaches this problem (automated AI red teaming with context awareness, testing prompts 200+ times for non-deterministic systems), why California's SB53 chatbot regulations carry $1,000-per-incident fines, and why security leaders need C-suite conversations about investment, not just compliance checklists.

If you lived through the application security wars of the 2000s, this episode will feel eerily familiar. If you're newer to security, it's a masterclass in how to think about emerging threat landscapes.

Full episode linked in comments.

#aisecurity #securitytrends #leadership

**Character Count:** 1,841
**Word Count:** 303

---

## Usage Notes

### Testing Recommendations:
- **Variation 1** (Personal Story): Best for building thought leadership, high engagement with security leaders
- **Variation 2** (Contrarian): High shareability, challenges assumptions, good for sparking debate
- **Variation 3** (Practical): Most actionable, appeals to practitioners looking for immediate takeaways
- **Variation 4** (Big Picture): Best for reaching broader audience, appeals to strategic thinkers and executives

### Posting Strategy:
1. **Week 1:** Post Variation 3 (Practical) on Monday/Tuesday morning when professionals seek actionable content
2. **Week 2:** Post Variation 2 (Contrarian) mid-week to spark discussion
3. **Week 3:** Post Variation 1 (Personal Story) on Thursday/Friday when engagement is high
4. **Week 4:** Post Variation 4 (Big Picture) as a "retrospective" tying to industry news

### Performance Tracking:
- [ ] Variation 1 posted on: _____ | Engagement: _____ | Click-through: _____
- [ ] Variation 2 posted on: _____ | Engagement: _____ | Click-through: _____
- [ ] Variation 3 posted on: _____ | Engagement: _____ | Click-through: _____
- [ ] Variation 4 posted on: _____ | Engagement: _____ | Click-through: _____

### Quality Checklist:
- [x] First sentence of each post is a strong hook
- [x] No em dashes (—) anywhere in the text
- [x] Written in host's narrative voice (first person from Ashish's perspective)
- [x] Each variation uses a different angle/theme
- [x] Posts are 150-300 words (LinkedIn optimal length)
- [x] Includes clear call-to-action (link in comments)
- [x] 2-3 relevant hashtags included
- [x] Line breaks for readability (not wall of text)
- [x] Guest's name and credentials mentioned
- [x] Sounds conversational, not corporate

---

*Generated via podcast-marketer workflow*
