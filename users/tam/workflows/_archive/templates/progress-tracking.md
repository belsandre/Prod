# Progress Tracking Template

**Purpose**: Standard template for tracking research progress across sessions, enabling resumability and clear status visibility.

---

## Progress Tracker Template

```markdown
# [Project/Research Name] Progress Tracker

**Project**: [Project or Fund Name]
**Started**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD]
**Status**: [Not Started / In Progress / Completed / Blocked]

---

## Phase 1: [Phase Name]

**Purpose**: [Brief description of phase objectives]

**Tasks**:
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

**Progress**: 0/[total] complete

**Notes**:
[Document any issues, blockers, or important observations]

---

## Phase 2: [Phase Name]

**Purpose**: [Brief description of phase objectives]

**Tasks**:
- [ ] [Task 1]
- [ ] [Task 2]

**Progress**: 0/[total] complete

**Notes**:
[Document any issues, blockers, or important observations]

---

## Phase 3: [Phase Name]

**Purpose**: [Brief description of phase objectives]

**Tasks**:
- [ ] [Task 1]
- [ ] [Task 2]

**Progress**: 0/[total] complete

**Notes**:
[Document any issues, blockers, or important observations]

---

## Overall Progress Summary

**Total Tasks**: [X]
**Completed**: [Y]
**Completion Rate**: [Y/X %]

**Estimated Time Remaining**: [Hours]

---

## Blockers & Issues

[Document any blockers, missing information, or items requiring follow-up]

**Critical**:
- [Issue requiring immediate attention]

**Non-Critical**:
- [Issue that can be addressed later]

---

## Session Log

### Session 1: [YYYY-MM-DD]
- **Duration**: [Hours]
- **Completed**: [Tasks completed]
- **Notes**: [Key observations or decisions]

### Session 2: [YYYY-MM-DD]
- **Duration**: [Hours]
- **Completed**: [Tasks completed]
- **Notes**: [Key observations or decisions]

[Continue for each work session...]
```

---

## Update Frequency Guidelines

### When to Update

**Required Updates**:
- At the start of each work session (review and identify next tasks)
- At phase boundaries (after completing each major phase)
- Before ending any work session (document progress and next steps)
- When encountering blockers or issues

**Optional Updates**:
- After completing batches of related tasks (e.g., every 3-5 items)
- Mid-session if significant findings emerge

### What NOT to Do

- ❌ Update after every single task (causes excessive interruptions)
- ❌ Over-document minutiae (tracker should be high-level)
- ❌ Create nested trackers (keep single source of truth)

---

## Resumability Guidelines

### Starting a New Session

1. **Read the tracker**: Check "Last Updated", overall progress, and current phase
2. **Review file system**: Verify completed work exists (file system = source of truth)
3. **Reconcile discrepancies**: If tracker shows incomplete but files exist, mark as complete
4. **Identify next task**: Choose next unchecked task from current phase
5. **Update status**: Mark "Last Updated" and note session start

### Ending a Session

1. **Mark completed tasks**: Check off all tasks finished this session
2. **Update progress counters**: Recalculate completion rates
3. **Document blockers**: Note any issues encountered
4. **Plan next steps**: Add notes about what to tackle next session
5. **Update timestamp**: Set "Last Updated" to current date

---

## Task Naming Conventions

**Good Task Names** (specific, actionable):
- ✅ "Research Company A (Tier 1)"
- ✅ "Extract GP names from dataroom"
- ✅ "Create executive summary"
- ✅ "Verify high-value claims for Company B"

**Poor Task Names** (vague, unclear):
- ❌ "Do research"
- ❌ "Next steps"
- ❌ "Finish analysis"
- ❌ "Other work"

---

## Completion Criteria

**Task Completion**:
- Task is marked complete `[x]` when all deliverables exist
- Include completion date: `[x] Task Name (completed: YYYY-MM-DD)`
- Brief note if task modified or partially completed

**Phase Completion**:
- All tasks in phase are checked off
- Phase notes document any limitations or caveats
- Deliverables exist in file system

**Project Completion**:
- All phases complete
- Final deliverables exist
- Status updated to "Completed"
- Final notes document overall limitations or follow-ups

---

## Batch Updates (Recommended for Efficiency)

**Strategy**: Update tracker at natural checkpoints rather than after every task.

**Checkpoints**:
- After completing 3-5 related tasks
- At the end of a work session
- At phase boundaries
- When switching between major work types

**Why Batch**: Reduces context switching, maintains flow, file system shows real-time status anyway.

**Example**:
```markdown
✅ Instead of:
- Research Company A → update tracker
- Research Company B → update tracker
- Research Company C → update tracker

✅ Do this:
- Research Company A, B, C → update tracker once marking all 3 complete
```

---

## Progress Visualization (Optional)

For complex projects, consider adding progress visualization:

```markdown
## Visual Progress

Phase 1: ████████████████████░░ 95% (19/20 complete)
Phase 2: ██████████░░░░░░░░░░░░ 40% (8/20 complete)
Phase 3: ░░░░░░░░░░░░░░░░░░░░░░ 0% (0/15 complete)

Overall: ██████████░░░░░░░░░░░░ 49% (27/55 complete)
```

---

## Customization by Workflow Type

### Research Workflows
- Track by entity (companies, people, topics)
- Include quality thresholds met/not met
- Document source counts per entity

### Analysis Workflows
- Track by analysis component
- Include data gathering vs. analysis vs. writing
- Document analytical decisions made

### Multi-Stage Workflows
- Track by stage gate
- Include approval/review status
- Document handoffs between stages

---

## Integration with File System

**File System = Source of Truth**: The progress tracker is a convenience layer. If discrepancies exist:

1. **Check file system** for actual deliverables
2. **Update tracker** to match file system reality
3. **Investigate discrepancy**: Document why files missing or unexpected files present

**Automated Status Checks** (optional): Workflows can scan directories and auto-update tracker:
```markdown
## Automated Status Check
- Scanned research/deals/tier-1/: 8 companies found
- Tracker shows: 6 companies complete
- **Action**: Mark Company G and Company H as complete
```

---

## Usage in Workflows

**Reference this template by including**:
```markdown
## Progress Tracking
Use `users/tam/workflows/templates/progress-tracking.md` template for tracking work across sessions.

Update at:
- Start/end of each session
- Phase boundaries
- When encountering blockers
```

**Workflow-specific extensions**: Workflows can add custom fields, progress visualizations, or tracking categories while maintaining core structure.
