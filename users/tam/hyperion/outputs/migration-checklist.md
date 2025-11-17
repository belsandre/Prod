# Hyperion Folder Reorganization - Migration Progress Checklist

**Started**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD]
**Current Status**: Not Started / In Progress / Completed
**Overall Progress**: 0/15 steps completed

---

## Quick Status Overview

| Phase | Status | Steps Completed | Notes |
|-------|--------|-----------------|-------|
| Phase 1: Objective Migration | ⬜ Not Started | 0/4 | |
| Phase 2: Structured Data | ⬜ Not Started | 0/1 | |
| Phase 3: Subjective Content | ⬜ Not Started | 0/5 | |
| Phase 4: Validation & Cleanup | ⬜ Not Started | 0/5 | |

**Legend**: ⬜ Not Started | 🟡 In Progress | ✅ Completed | ⚠️ Blocked/Issues

---

## PHASE 1: OBJECTIVE MIGRATION (Safe, No Deletion)

### ⬜ Step 1: Create New Folder Structure
**Status**: Not Started
**Time Estimate**: 5 minutes
**Assigned to**: [Your name or "Claude"]

**Commands to run**:
```bash
cd users/tam/hyperion/
mkdir -p research/{dataroom,companies,people}
mkdir -p findings/{_data,_process,_archive}
mkdir -p recommendations/{critical,high-priority,medium-priority}
```

**Test**:
- [ ] All folders exist: `ls -la | grep -E 'research|findings|recommendations'`
- [ ] Nested folders created: `ls -la research/` shows dataroom, companies, people
- [ ] Findings subfolders exist: `ls -la findings/` shows _data, _process, _archive

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

### ⬜ Step 2: Migrate Dataroom (Objective Content)
**Status**: Not Started
**Time Estimate**: 10 minutes
**Assigned to**: [Your name or "Claude"]

**Commands to run**:
```bash
cp -r dataroom/* research/dataroom/
```

**Test**:
- [ ] File count matches: `ls dataroom/ | wc -l` == `ls research/dataroom/ | wc -l`
- [ ] Sample files present: `ls research/dataroom/ | head -5`
- [ ] Original dataroom/ folder still intact

**Files migrated**: [List count or key files]

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

### ⬜ Step 3: Migrate Company Research (Objective Content)
**Status**: Not Started
**Time Estimate**: 30 minutes
**Assigned to**: [Your name or "Claude"]

**Commands to run**:
```bash
cp -r research/deals/tier-1/* research/companies/
cp -r research/deals/tier-2/* research/companies/

# Then rename files within each company folder:
# Example: figure/research-notes.md → figure/independent-research.md
#          figure/pitch-deck-notes.md → figure/target-sources.md
```

**Test**:
- [ ] All 24 companies present in `research/companies/`
- [ ] Files renamed to new structure (independent-research.md, target-sources.md)
- [ ] Original research/deals/ folder still intact
- [ ] No tier-1/tier-2 terminology in new structure

**Companies migrated**: [0/24]

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
[List any renaming decisions or exceptions]
```

---

### ⬜ Step 4: Migrate GP/People Research (Objective Content)
**Status**: Not Started
**Time Estimate**: 15 minutes
**Assigned to**: [Your name or "Claude"]

**Work to do**:
- Reorganize research/people/ structure
- Move raw data files (LinkedIn exports) to target-sources/ subfolder
- Separate independent-research.md from target-sources/

**Test**:
- [ ] dillon-dunteman/ has independent-research.md
- [ ] dillon-dunteman/target-sources/ exists with LinkedIn data
- [ ] CSV files present: connections_1k.csv, connections_harvard.csv, connections_deeptech.csv
- [ ] henry-bellew/ research-notes.md present

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

## PHASE 2: STRUCTURED DATA CONVERSION (Objective Extraction)

### ⬜ Step 5: Extract Structured Data to JSON
**Status**: Not Started
**Time Estimate**: 3-4 hours
**Assigned to**: [Your name or "Claude"]

**Files to create**:
- [ ] `findings/_data/portfolio.json` - Companies, valuations, funding rounds, co-investors
- [ ] `findings/_data/network.json` - LinkedIn stats, connection counts, relationships
- [ ] `findings/_data/timeline.json` - Chronological events with dates and sources
- [ ] `findings/_data/claims.json` - GP claims + validation status + evidence links
- [ ] `findings/_data/gp-profiles.json` - Dillon, Henry backgrounds and involvement

**Test**:
- [ ] All 5 JSON files exist in findings/_data/
- [ ] JSON validates (no syntax errors): `python -m json.tool findings/_data/portfolio.json`
- [ ] Schema matches proposal (see "Structured Data Opportunities" section)
- [ ] All 24 companies in portfolio.json
- [ ] Source citations included in all data

**Progress**: [0/5 JSON files created]

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
[Note any schema decisions or data challenges]
```

---

## PHASE 3: SUBJECTIVE CONTENT (Preserve Old for Reference)

### ⬜ Step 6: Preserve Old Findings for Reference
**Status**: Not Started
**Time Estimate**: 2 minutes
**Assigned to**: [Your name or "Claude"]

**Commands to run**:
```bash
mkdir -p migration-reference
cp -r outputs/* migration-reference/
cp -r research/deals/ migration-reference/old-company-structure/
```

**Test**:
- [ ] migration-reference/ folder exists
- [ ] All outputs/ files copied to migration-reference/
- [ ] research/deals/ copied to migration-reference/old-company-structure/
- [ ] File counts match originals

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

### ⬜ Step 7: Create New index.md (Executive Summary)
**Status**: Not Started
**Time Estimate**: 2-3 hours
**Assigned to**: [Your name or "Claude"]

**Work to do**:
- Create `index.md` using template from proposal
- Include: Current Status, Key Findings, Critical Recommendations
- Link to new folder structure (findings/, research/, recommendations/)
- Reference migration-reference/ as needed

**Test**:
- [ ] index.md exists in users/tam/hyperion/
- [ ] All sections present (Status, Findings, Recommendations)
- [ ] Links work to research/ files
- [ ] Links work to findings/ files (if any created yet)
- [ ] No broken links

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
[Note any content decisions or structural changes]
```

---

### ⬜ Step 8: Create New Findings (Rewrite from Old)
**Status**: Not Started
**Time Estimate**: 4-6 hours
**Assigned to**: [Your name or "Claude"]

**Files to create**:
- [ ] `findings/portfolio-assessment.md` (from migration-reference/vc-research-summary.md)
- [ ] `findings/claims-validation.md` (from migration-reference/claims-validation.md)
- [ ] `findings/network-analysis.md` (from migration-reference/network-analysis.md)
- [ ] `findings/timeline.md` (create new)
- [ ] `findings/gp-analysis.md` (consolidate from old files)

**Test**:
- [ ] All 5 finding files exist
- [ ] Links to research/ folder work
- [ ] Links to findings/_data/ work
- [ ] Compare to migration-reference/ originals - no critical content lost
- [ ] Each finding has clear source citations

**Progress**: [0/5 findings created]

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
[Document what changed from old to new]
```

---

### ⬜ Step 9: Create Recommendations (New Content)
**Status**: Not Started
**Time Estimate**: 3-4 hours
**Assigned to**: [Your name or "Claude"]

**Files to create**:
- [ ] `recommendations/critical/verify-gp-relationships.md`
- [ ] `recommendations/critical/validate-figure-execution.md`
- [ ] `recommendations/high-priority/investigate-henry-bellew.md`
- [ ] `recommendations/high-priority/validate-customer-claims.md`
- [ ] `recommendations/medium-priority/benchmark-portfolio.md`
- [ ] `recommendations/medium-priority/deep-dive-quantinuum.md`

**Test**:
- [ ] All recommendation files created
- [ ] Each links back to findings/
- [ ] Each links to research/ evidence
- [ ] Full traceability: recommendation → finding → evidence
- [ ] Priority folders organized correctly

**Progress**: [0/6 recommendations created]

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
[Note any new recommendations discovered]
```

---

### ⬜ Step 10: Create Process Documentation
**Status**: Not Started
**Time Estimate**: 1-2 hours
**Assigned to**: [Your name or "Claude"]

**Files to create**:
- [ ] `findings/_process/methodology.md` (evidence quality framework)
- [ ] `findings/_process/analysis-log.md` (chronological work done)
- [ ] `findings/_process/workflows-used.md` (which workflows generated what)
- [ ] `findings/_process/change-log.md` (migration documentation)
- [ ] `findings/_process/data-updates.md` (when new data added)

**Test**:
- [ ] All 5 process files exist
- [ ] Methodology clearly explains source types (independent, target, dataroom)
- [ ] Analysis log documents migration
- [ ] Change log has initial entry

**Progress**: [0/5 process docs created]

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

## PHASE 4: VALIDATION & CLEANUP

### ⬜ Step 11: Validate Migration Differences
**Status**: Not Started
**Time Estimate**: 2-3 hours
**Assigned to**: [Your name or "Claude"]

**Work to do**:
- Create `migration-validation.md` documenting changes
- Compare new findings to migration-reference/ originals
- Document what changed, what stayed same, structural changes

**Test**:
- [ ] migration-validation.md exists
- [ ] Documented changes for each finding
- [ ] Documented structural changes
- [ ] Confirmed no critical findings lost
- [ ] Reviewed by [your name]

**Key differences found**:
```
[List major differences between old and new]
```

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

### ⬜ Step 12: Update Eleventy Config
**Status**: Not Started
**Time Estimate**: 1 hour
**Assigned to**: [Your name or "Claude"]

**Work to do**:
- Update `sites/tam/.eleventy.js` to recognize new structure
- Ensure `/hyperion/` routes to `index.md`
- Test JSON file passthrough (`findings/_data/*.json`)
- Update navigation menus if needed
- Include migration-reference/ folder (for reference)

**Test**:
- [ ] `npm run build:tam` succeeds with no errors
- [ ] Site serves locally: `npm run serve:tam`
- [ ] /hyperion/ shows new index.md
- [ ] JSON files downloadable from findings/_data/
- [ ] All links work in local preview
- [ ] migration-reference/ accessible (if desired)

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

### ⬜ Step 13: Review & Decision Point
**Status**: Not Started
**Time Estimate**: 1-2 hours
**Assigned to**: [Your name]

**Review checklist**:
- [ ] End-to-end navigation works (index → recommendation → finding → evidence)
- [ ] Compared new findings to migration-reference/ originals
- [ ] Read migration-validation.md
- [ ] No critical content lost
- [ ] Navigation flow intuitive
- [ ] Ready to delete old structure? YES / NO

**Decision**: [KEEP BOTH STRUCTURES / PROCEED WITH DELETION]

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

### ⬜ Step 14: Delete Old Structure (Optional)
**Status**: Not Started
**Time Estimate**: 5 minutes
**Assigned to**: [Your name or "Claude"]

**⚠️ ONLY DO THIS AFTER VALIDATION COMPLETE**

**Commands to run**:
```bash
# Delete old folders (migration-reference stays!)
rm -rf outputs/
rm -rf research/deals/
rm -rf dataroom/

# KEEP migration-reference folder indefinitely
```

**Test**:
- [ ] outputs/ deleted
- [ ] research/deals/ deleted
- [ ] dataroom/ deleted
- [ ] migration-reference/ STILL EXISTS
- [ ] Site still builds: `npm run build:tam`
- [ ] No broken links in site

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

### ⬜ Step 15: Deploy
**Status**: Not Started
**Time Estimate**: 30 minutes
**Assigned to**: [Your name or "Claude"]

**Commands to run**:
```bash
git add .
git commit -m "Reorganize hyperion to output-focused structure (objective-first migration)"
git push -u origin claude/review-reorg-proposal-01WCf9Y8ssCGRbMptPbyybif
```

**Test**:
- [ ] Committed successfully
- [ ] Pushed to GitHub
- [ ] GitHub Actions build passing
- [ ] Deployed to Cloudflare Pages
- [ ] Site live and functional: [URL]

**Notes**:
```
[Add any observations, issues, or decisions made during this step]
```

---

## Migration Issues & Blockers

### Open Issues
| # | Issue | Status | Assigned to | Resolution |
|---|-------|--------|-------------|------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### Decisions Made During Migration
| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| | | | |

---

## Final Verification Checklist

**After all steps complete, verify**:
- [ ] index.md is main entry point
- [ ] All findings link to evidence
- [ ] All recommendations link to findings
- [ ] JSON files validate and contain correct data
- [ ] Site builds without errors
- [ ] Site deployed successfully
- [ ] migration-reference/ preserved for future reference
- [ ] migration-validation.md documents all changes

**Sign-off**:
- Completed by: [Your name]
- Date: [YYYY-MM-DD]
- Review notes:
```
[Final review observations]
```

---

## How to Use This Checklist

1. **Update Status**: Change ⬜ to 🟡 when starting a step, ✅ when complete
2. **Check boxes**: Mark [ ] as [x] for each completed test
3. **Add Notes**: Document decisions, issues, observations in Notes sections
4. **Track Progress**: Update "Overall Progress" counter at top as you go
5. **Resume Later**: Any Claude agent can read this file and continue from current step

**To continue in new conversation**: Share this checklist file with Claude and say "Continue migration from Step X"
