# Podcast to LinkedIn Posts Workflow

## Overview

This workflow uses an LLM (like Claude Code) to generate multiple LinkedIn post variations from a podcast interview transcript. Simply provide the transcript and use the prompts below to generate 6 different post styles.

## Input

- **Podcast interview transcript** (text file or pasted text)
- Can be from any transcription service (Otter.ai, Descript, Rev, etc.)
- Plain text format works best

## Output

6 LinkedIn post variations in different styles:
1. Teaser Post (engagement hook)
2. Key Takeaways List
3. Featured Quote Post
4. Behind-the-Scenes Narrative
5. Call-to-Action Post
6. Thread Starter (multi-part)

---

## Workflow Steps

### Step 1: Prepare Your Transcript

Save your podcast transcript as a text file in your `inputs/` folder, or have it ready to paste.

### Step 2: Generate Posts Using LLM

Use the prompts below with Claude Code or any LLM. For each prompt, paste your transcript when requested.

---

## LLM Prompts for Each Post Type

### Prompt 1: Teaser Post (Engagement Hook)

```
I have a podcast transcript. Please create an engaging LinkedIn teaser post to promote this episode.

Requirements:
- Start with an intriguing question that hooks the reader
- Include 3 bullet points highlighting what's covered
- End with an engagement question
- Add relevant emojis (but don't overuse)
- Include placeholder for link
- Suggest 3-5 relevant hashtags
- Keep it under 300 words

Style: Conversational, curiosity-driven, high energy

Here's the transcript:
[PASTE YOUR TRANSCRIPT]
```

**Expected Output:** Attention-grabbing post that makes people want to click and listen.

---

### Prompt 2: Key Takeaways List

```
I have a podcast transcript. Please extract and format the top 3-5 key takeaways as a LinkedIn post.

Requirements:
- Start with a hook line about the episode
- Create a numbered list (3-5 items) of the most valuable insights
- Each takeaway should be 1-2 sentences
- End with a question to drive engagement
- Include emoji indicators for each point
- Add relevant hashtags
- Mention this is from a podcast episode

Style: Educational, value-first, scannable

Here's the transcript:
[PASTE YOUR TRANSCRIPT]
```

**Expected Output:** Easy-to-scan list of insights that provides immediate value.

---

### Prompt 3: Featured Quote Post

```
I have a podcast transcript. Please find the most powerful quote from the guest and create a LinkedIn post featuring it.

Requirements:
- Select one compelling quote (1-3 sentences max)
- Format the quote prominently
- Add context about who said it and when
- Explain why this quote is meaningful
- Connect it to a broader insight or lesson
- End with a reflective question
- Include relevant hashtags

Style: Thoughtful, inspirational, wisdom-focused

Here's the transcript:
[PASTE YOUR TRANSCRIPT]
```

**Expected Output:** Highlighted quote with context that resonates emotionally.

---

### Prompt 4: Behind-the-Scenes Narrative

```
I have a podcast transcript. Please create a behind-the-scenes LinkedIn post about recording this episode.

Requirements:
- Write in first person (host perspective)
- Share a personal moment or surprise from the recording
- Use storytelling to build connection
- Include what made this conversation special
- Mention unexpected topics or insights that came up
- Keep it authentic and vulnerable
- End with anticipation for the episode
- Use emojis sparingly for emphasis

Style: Personal, storytelling, authentic, warm

Here's the transcript:
[PASTE YOUR TRANSCRIPT]
```

**Expected Output:** Personal narrative that builds connection with audience.

---

### Prompt 5: Call-to-Action Post

```
I have a podcast transcript. Please create a results-focused LinkedIn post with a strong call-to-action.

Requirements:
- Lead with the value proposition (what listeners will learn)
- Include 3 specific, actionable takeaways
- Use checkmarks or bullets for visual scanning
- Clearly state when/how to listen
- Include multiple CTAs (save, share, listen, comment)
- Add urgency or FOMO element
- Format for mobile readability
- Include relevant hashtags

Style: Action-oriented, benefit-driven, clear CTA

Here's the transcript:
[PASTE YOUR TRANSCRIPT]
```

**Expected Output:** Conversion-focused post that drives podcast plays.

---

### Prompt 6: Thread Starter (Multi-part Series)

```
I have a podcast transcript. Please create a LinkedIn thread-style post (6 connected posts) breaking down the key insights.

Requirements:
- Post 1: Hook and introduction to the topic
- Posts 2-4: Individual insights/lessons (one per post)
- Post 5: How to apply these insights
- Post 6: CTA to listen to full episode
- Each post should be 100-150 words
- Use clear numbering [1/6], [2/6], etc.
- Make each post work standalone but flow together
- Include thread emoji 🧵 in first post
- Add relevant hashtags in final post only

Style: Educational thread, in-depth, comprehensive

Here's the transcript:
[PASTE YOUR TRANSCRIPT]
```

**Expected Output:** 6-part thread that can be posted as a series or carousel.

---

## Step 3: Save Your Generated Posts

Create a folder in your `outputs/` directory:

```
outputs/
  podcast_episode_[date]/
    post_1_teaser.txt
    post_2_takeaways.txt
    post_3_quote.txt
    post_4_bts.txt
    post_5_cta.txt
    post_6_thread.txt
```

Save each generated post in a separate file for easy access.

---

## Step 4: Customize and Schedule

### Customization Checklist

For each post:
- [ ] Replace any placeholder text (guest name, topic, etc.)
- [ ] Add your actual podcast link
- [ ] Customize hashtags for your niche
- [ ] Adjust tone to match your voice
- [ ] Add episode artwork or visual if posting on LinkedIn
- [ ] Tag your guest (if applicable)
- [ ] Verify all details are accurate

### Suggested Posting Schedule

Space out your posts throughout the week for maximum reach:

| Day | Post Type | Purpose |
|-----|-----------|---------|
| Day 1 (Launch) | Teaser Post | Announce episode, create curiosity |
| Day 2 | Key Takeaways | Provide immediate value |
| Day 4 | Featured Quote | Midweek engagement boost |
| Day 6 | Behind-the-Scenes | Weekend deeper engagement |
| Day 7 | Call-to-Action | End-of-week conversion push |
| Week 2+ | Thread Starter | Evergreen content, thought leadership |

---

## Advanced Tips

### Getting Better Results from the LLM

1. **Provide Context**: Along with the transcript, mention:
   - Guest's name and credentials
   - Main topic/theme
   - Target audience
   - Your podcast's unique angle

2. **Refine Iteratively**: After the first generation, ask the LLM to:
   - "Make it more conversational"
   - "Add more specific details from the transcript"
   - "Shorten to 200 words"
   - "Make the hook stronger"

3. **Request Variations**: Ask for multiple options:
   - "Give me 3 different opening hooks"
   - "Suggest 5 different hashtag combinations"
   - "Provide 2 versions - one formal, one casual"

### Example Refinement Prompt

```
That's good, but can you:
1. Make the opening hook more intriguing
2. Add a specific data point or statistic from the transcript
3. Include a personal anecdote the guest shared
4. Make it feel less promotional and more value-driven
```

---

## Workflow Variations

### For Multiple Episodes

Process multiple transcripts in one session:

1. Batch prepare all transcripts
2. Use the same prompts for each
3. Save in separate output folders by episode number/date
4. Build a content calendar for the month

### For Different Platforms

Adapt the prompts for other platforms:

**Twitter/X Thread:**
- Reduce character count per section
- Make it snappier
- More emojis, shorter sentences

**Instagram Caption:**
- More visual language
- Story-driven approach
- Call-out for "link in bio"

**Newsletter:**
- Longer form
- More detail and context
- Direct quotes
- Deeper analysis

---

## Quality Checklist

Before posting, ensure each LinkedIn post has:

- ✅ Compelling first line (hook)
- ✅ Clear value proposition
- ✅ Specific details (not generic)
- ✅ Your unique voice and tone
- ✅ Engagement question or CTA
- ✅ Relevant hashtags (3-5)
- ✅ Link to podcast (in comments or bio)
- ✅ Proper formatting for mobile
- ✅ No typos or errors
- ✅ Guest tagged (if appropriate)

---

## Metrics to Track

Monitor which post styles perform best:

| Metric | What It Tells You |
|--------|-------------------|
| Impressions | Reach and visibility |
| Engagement Rate | Quality of content |
| Click-throughs | Effectiveness of CTA |
| Shares | Resonance with audience |
| Comments | Discussion quality |
| Profile visits | Brand building |

Use these insights to refine your prompts and post styles over time.

---

## Troubleshooting

**Problem:** LLM output is too generic

**Solution:**
- Provide more context about your guest and episode
- Ask for specific quotes or moments from the transcript
- Request more specificity: "Don't use generic phrases, use actual details from the episode"

**Problem:** Posts are too long

**Solution:**
- Add word count limits to prompts
- Ask for "mobile-optimized length"
- Request "under 300 words" or specific character count

**Problem:** Tone doesn't match your brand

**Solution:**
- Provide examples of your previous posts in the prompt
- Specify tone: "conversational and warm" vs "professional and authoritative"
- Ask for revisions: "Make this more casual and approachable"

**Problem:** Not getting unique angles

**Solution:**
- Ask LLM to identify unique or surprising moments
- Request "What's the most contrarian point in this transcript?"
- Ask for "What angle hasn't been covered yet?"

---

## Example Output

Here's what a generated post might look like:

### Teaser Post Example

```
🎙️ "If you're waiting for the perfect time to start, you've already missed it."

That's what Sarah Chen told me in our latest podcast episode, and it completely
reframed how I think about timing.

In this conversation, we dive into:
• Why "perfect timing" is a myth that keeps you stuck
• The 3 signs it's actually the right time to make a move
• How Sarah launched her company with $500 and a laptop

What's something you've been waiting for the "right time" to do?

Listen now (link in comments) 👇

#Podcast #Entrepreneurship #Leadership #Startup #GrowthMindset
```

---

## Notes

- All prompts can be customized to your specific needs
- You can combine elements from different prompts
- Feel free to create your own prompt variations
- The key is providing good context and being specific about what you want

## Related Workflows

- `newsletter_from_podcast.md` - Convert podcast to newsletter
- `blog_post_from_podcast.md` - Create long-form blog content
- `social_clips_script.md` - Generate scripts for short video clips

---

Last Updated: 2025-11-07
