# LinkedIn Posts - Seezo Episode (Sandesh Mysore Anand)

## Variation 1: Personal Discovery Angle

Most security teams are failing at threat modeling.

I just spent 45 minutes with Sandesh Mysore Anand, who spent 12 years doing AppSec before starting CISO, and he completely reframed how I think about security coverage.

Here's what hit me: When your security activity has 10% coverage, are you really doing security at all?

That's the reality for most companies with threat modeling and security design reviews. They're incredibly valuable when you do them, but they're so manual that security teams can only review a fraction of what developers ship.

The math is brutal. For every 100 engineers, you have 2-3 security engineers who can do threat modeling. There's no way to keep up.

What changed? LLMs can finally process unstructured data. All those Jira tickets, Word docs, diagrams, and tribal knowledge that used to require hours of human translation can now be analyzed automatically.

But here's the nuanced part Sandesh taught me: The hardest problem isn't extracting information. It's making the results explainable and contextual. Every company has their own jargon. One customer has a microservice called "Stark" for notifications. The LLM has no idea what that means without company-specific context.

The opportunity is massive. When you can go from 10% coverage to 100% coverage, you're not just doing more security reviews. You're fundamentally changing what's possible in secure software development.

In this episode, Sandesh breaks down how they're solving explainability, why security standards are finally becoming operational, and how the maker-checker model must evolve with AI-powered development.

Link in comments if you're thinking about how to scale AppSec in the AI era.

#appsec #threatmodeling #LLMs #securityengineering

**Character count:** 1,621

---

## Variation 2: Contrarian/Surprising Angle

The people writing your code have never been trained in security.

Not your developers. I'm talking about your product managers, designers, and sales engineers who are now generating code with AI tools.

Sandesh Mysore Anand (founder of CISO, 12 years in AppSec) just explained something that should terrify every security team: We spent 15 years trying to teach developers to write secure code with mixed results. Now non-developers are mass-producing code, and we have no budget for new security engineers.

The numbers tell the story. Companies are generating more PRs and more repos than ever. But they're not pushing more code to production. Why? Code reviews have become the bottleneck.

Here's the insight I wasn't expecting: The solution isn't just better code scanning. It's moving security earlier in the process.

When developers use tools like Cursor or Claude Code, they're not thinking about security while writing code anymore. They're thinking about it when they write the prompt or PRD. If you can inject security requirements at that design stage, the AI generates more secure code by default.

Sandesh shared a perfect example: One company went from doing 10 security design reviews per quarter to 100. Not because they hired more people. Because they automated the first pass with LLMs and used humans only for high-risk features.

The counterintuitive part? Writing good security standards is suddenly a superpower. Those dusty 50-page documents that nobody ever read? LLMs can actually read them and tell developers exactly which 5 standards apply to their specific feature.

We're in this weird moment where AI is both creating and solving the security problem.

Full conversation covers how to measure "good enough" AI results, why makers and checkers can't be the same entity, and what happens when code generation outpaces code review.

Worth a listen if you're rethinking AppSec for the AI era.

#security #artificialintelligence #devops #startups

**Character count:** 1,882

---

## Variation 3: Practical/Actionable Angle

We just added 100% security coverage without hiring anyone.

That's what Sandesh Mysore Anand told me about the best users of CISO, his company that automates security design reviews using LLMs.

If you're struggling to scale threat modeling, here are the three metrics he tracks to know if automation is actually working:

**Input metric** - Are more people using it? If you went from 10 reviews per quarter to 100, someone is finding value.

**Output metric** - Is the output being used? If the number of static analysis findings is dropping over time, your design requirements are working. Developers are building it right the first time.

**Impact metric** - What's the effect on code velocity? If you're seeing fewer vulnerabilities AND code shipping faster to production, you've hit the sweet spot.

The implementation pattern that works best: Automate 100% of first-pass reviews. Use AI to assign risk rankings (high, medium, low). Route high-risk features to human security engineers. Let low-risk features proceed with AI-generated requirements only.

One detail that stuck with me: A "good enough" AI-generated security requirement isn't just "don't log sensitive data." It's "don't log sensitive data, and here's the approved library your company already uses, with a link to the Confluence page explaining how."

Context is everything. Generic advice from an LLM is worthless. Company-specific, actionable guidance is a game-changer.

Sandesh also explained why this matters more now than ever. The bottleneck in software development is shifting from writing code to reviewing code. AI is making code generation 10x faster, but code review hasn't caught up.

In our conversation, he breaks down how to customize LLM outputs for your company's jargon, where to place humans in the loop based on your culture, and why 10% security coverage means you're not really doing security.

Link in comments. Highly practical for anyone running AppSec or security engineering.

#cybersecurity #appsecurity #automation #engineering

**Character count:** 1,876

---

## Variation 4: Big Picture/Industry Trend Angle

Security is about to change as much as code generation just did.

I just talked to Sandesh Mysore Anand, founder of CISO and 12-year AppSec veteran, about what happens when the entire software development lifecycle gets AI-powered.

His observation: AppSec has always evolved with SDLC changes. Waterfall had one security model. Agile forced us to work in two-week sprints. CI/CD meant scanning every pull request. Now we're entering the AI-powered SDLC era.

The pattern is clear. Every time developer workflows change, security has to completely reinvent itself.

What's different this time? The shift is happening faster and the stakes are higher.

Three forces are colliding right now:

1. AI tools can finally process unstructured data (the limiting factor for threat modeling for 20+ years)
2. Non-developers are writing code at scale (PMs, designers, sales engineers)
3. Companies are generating way more code but not shipping faster (review bottleneck)

The most fascinating insight from our conversation: Security tools that eliminate entire vulnerability classes will win. Just like CSRF disappeared when frameworks added automatic nonces, certain vulnerabilities will vanish as AI code generation improves. But new ones (like prompt injection) will emerge.

The maker-checker principle still applies. The entity that makes something can't be the only one checking it. That's why Sandesh believes cursor writing secure code isn't enough. You need independent verification.

One surprising GTM lesson: When selling security tools, geography matters less than maturity. Selling to an Indian fintech is more similar to selling to a US fintech than to an Indian bank. The patterns between Bangalore and Silicon Valley mirror each other more than the patterns within India.

We covered how LLMs are finally making security standards operational, why 100% coverage should be the baseline, and how to balance automation with human judgment based on organizational culture.

This is one of the best conversations I've had about where security is heading in the next 3-5 years.

Link in comments for the full episode.

#cybersecurity #AI #futureofwork #securityleadership

**Character count:** 1,996

---

## Notes

- All posts written from host perspective (Chang/Ashish)
- No em dashes used
- Strong opening hooks on each variation
- Different angles: personal, contrarian, practical, trend-based
- Character counts within LinkedIn optimal range
- Ready to post with minimal edits
