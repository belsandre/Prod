# Harvard Network Verification Analysis
**Subject:** Dillon Dunteman's Harvard Network Claims
**Data Source:** LinkedIn connections who studied at Harvard (603 total connections)
**Analysis Date:** 2025-11-17

---

## Executive Summary

Of the 6 specific Harvard founder relationships claimed in the dataroom materials, **only 2 out of 6 (33%) can be verified** through LinkedIn connections. Most critically, **none of the three "hot company" relationships (Cursor, Mercor, Cognition/Devin) can be verified** through his LinkedIn network.

---

## Validation Results by Claim

### **HIGH-VALUE CLAIMS (The "Already Scaling" Companies - $9.9B-$10B valuations)**

#### ❌ **CLAIM 1: Cursor/Anysphere - Oskar Schulz**
- **Claimed relationship:** "Friendship with President Oskar Schulz '23"
- **Search performed:** Full name search, surname search, company search
- **Result:** **NOT FOUND** - No LinkedIn connection to Oskar Schulz
- **Company search:** No connections found at Cursor or Anysphere
- **Validation status:** ❌ **CANNOT VERIFY**

#### ❌ **CLAIM 2: Mercor - Virat Talwar**
- **Claimed relationship:** "Friendship with 1st hire & angel investor Virat Talwar '23"
- **Search performed:** Full name search, surname search, company search
- **Result:** **NOT FOUND** - No LinkedIn connection to Virat Talwar
- **Company search:** No connections found at Mercor
- **Validation status:** ❌ **CANNOT VERIFY**

#### ❌ **CLAIM 3: Cognition/Devin - Scott Wu**
- **Claimed relationship:** "Classmate of CEO Scott Wu '19"
- **Search performed:** Full name search, "Scott Wu" search, surname search, company search
- **Result:** **NOT FOUND** - No LinkedIn connection to Scott Wu
- **Company search:** No connections found at Cognition
- **Note:** Found "Irene Wu" and "Justin Wu" but neither work at Cognition
- **Validation status:** ❌ **CANNOT VERIFY**

---

### **"NEXT WAVE" CLAIMS (Emerging Companies)**

#### ✅ **CLAIM 4: PRODEX LABS - Kushan Weerakoon**
- **Claimed relationship:** "Close friendship with Founder & CEO Kushan Weerakoon '25"
- **Search performed:** Full name search, company search
- **Result:** **FOUND** ✅
- **LinkedIn data:**
  - Name: Kushan Weerakoon
  - Title: ProDex Labs (note: spelled "ProDex" not "PRODEX")
  - Location: New York City Metropolitan Area
  - Profile: https://www.linkedin.com/in/kushan-weerakoon/
- **Additional findings:** Also found Rick Li ("ProDex Labs | Prev. SpaceX | Applied Math @ Harvard")
- **Validation status:** ✅ **VERIFIED**

#### ✅ **CLAIM 5: garden - Justin Mack**
- **Claimed relationship:** "Close friendship with Founder & CTO Justin Mack '22"
- **Search performed:** Full name search, company search
- **Result:** **FOUND** ✅
- **LinkedIn data:**
  - Name: Justin Mack
  - Title: Co-Founder & CTO at Garden
  - Location: New York City Metropolitan Area
  - Profile: https://www.linkedin.com/in/justindmack/
- **Validation status:** ✅ **VERIFIED**

#### ❌ **CLAIM 6: Stealth - Henry Zhou**
- **Claimed relationship:** "Friendship with Founder & CTO Henry Zhou '28"
- **Search performed:** Full name search, surname search
- **Result:** **NOT FOUND** - No LinkedIn connection to Henry Zhou
- **Note:** Found "Amy Zhou" (HBS MBA) and "Andy Zhou" (WHO Foundation) but neither match
- **Validation status:** ❌ **CANNOT VERIFY**

---

## Key Findings & Red Flags

### 🚩 **Critical Issues**

1. **Zero verification of the three $10B companies**: Despite claiming relationships with people at Cursor ($9.9B), Mercor ($10B), and Cognition ($10B), there are **no LinkedIn connections** to any of these individuals

2. **Indirect relationship claims**: For the two highest-value companies (Cursor and Mercor), he claims relationships with non-founders:
   - Cursor: "President" Oskar Schulz (not a founder)
   - Mercor: "1st hire & angel investor" Virat Talwar (not a founder)
   - Only for Cognition does he claim a relationship with the actual CEO

3. **PROD accelerator**: No connections found to anyone listing "Prod" or "PROD" in their profile, despite claiming this is a key sourcing advantage

### 📊 **Statistical Summary**

- **Total Harvard connections:** 603
- **Claimed specific relationships:** 6
- **Verified connections:** 2 (33%)
- **Unverified connections:** 4 (67%)
- **$10B company connections verified:** 0 out of 3 (0%)

---

## Recommended Validation Searches

To thoroughly validate these claims, the following searches should be performed:

### **Primary Target Searches (The Big Three)**

1. **Oskar Schulz (Cursor/Anysphere)**
   - Search: `grep -i "schulz" connections_harvard.csv`
   - Search: `grep -i "cursor\|anysphere" connections_harvard.csv`
   - **Result:** ❌ No matches

2. **Virat Talwar (Mercor)**
   - Search: `grep -i "talwar" connections_harvard.csv`
   - Search: `grep -i "mercor" connections_harvard.csv`
   - **Result:** ❌ No matches

3. **Scott Wu (Cognition/Devin)**
   - Search: `grep -i "scott.*wu\|wu.*scott" connections_harvard.csv`
   - Search: `grep -i "cognition" connections_harvard.csv`
   - Search: `grep "^\".*Wu\"" connections_harvard.csv` (find all Wus)
   - **Result:** ❌ No matches (found other Wus but not Scott)

### **Broader Company Network Searches**

4. **Anyone at Cursor/Anysphere**
   - Purpose: Find anyone else at these companies to assess broader network
   - Search: `grep -i "cursor\|anysphere" connections_harvard.csv`
   - **Result:** ❌ Zero connections

5. **Anyone at Mercor**
   - Purpose: Find anyone at Mercor regardless of role
   - Search: `grep -i "mercor" connections_harvard.csv`
   - **Result:** ❌ Zero connections

6. **Anyone at Cognition**
   - Purpose: Find anyone at Cognition (maker of Devin)
   - Search: `grep -i "cognition" connections_harvard.csv`
   - **Result:** ❌ Zero connections

### **PROD Accelerator Network**

7. **PROD accelerator connections**
   - Purpose: Validate claim of privileged access to PROD ecosystem
   - Search: `grep -i "\\bprod\\b" connections_harvard.csv`
   - **Result:** ❌ No direct matches to "PROD" accelerator
   - **Note:** Found "ProDex" connections but this appears to be a different entity

### **Secondary Target Searches (Next Wave Companies)**

8. **Kushan Weerakoon (PRODEX/ProDex Labs)**
   - Search: `grep -i "weerakoon\|prodex" connections_harvard.csv`
   - **Result:** ✅ **FOUND**

9. **Justin Mack (garden)**
   - Search: `grep -i "mack.*garden\|garden.*mack" connections_harvard.csv`
   - **Result:** ✅ **FOUND**

10. **Henry Zhou (Stealth)**
    - Search: `grep -i "henry.*zhou\|zhou.*henry" connections_harvard.csv`
    - Search: `grep -i "zhou" connections_harvard.csv` (find all Zhous)
    - **Result:** ❌ Not found (found other Zhous but not Henry)

### **Class Year Validation Searches**

11. **Harvard Class of 2019 (Scott Wu's class)**
    - Purpose: Check if connected to Scott Wu's classmates
    - Search: `grep -i "'19\|2019" connections_harvard.csv`
    - **Relevance:** Claimed to be Scott Wu's classmate - should have many '19 connections

12. **Harvard Class of 2023 (Oskar Schulz & Virat Talwar's class)**
    - Purpose: Check connections to this graduating class
    - Search: `grep -i "'23\|2023" connections_harvard.csv`
    - **Relevance:** Both Cursor and Mercor contacts allegedly from this class

13. **Harvard Class of 2022 (Justin Mack's class)**
    - Purpose: Validate the verified connection's class year
    - Search: `grep -i "'22\|2022" connections_harvard.csv`

14. **Harvard Class of 2025 (Kushan Weerakoon's class)**
    - Purpose: Validate the verified connection's class year
    - Search: `grep -i "'25\|2025" connections_harvard.csv`

15. **Harvard Class of 2028 (Henry Zhou's class)**
    - Purpose: Check for very recent graduates/current students
    - Search: `grep -i "'28\|2028" connections_harvard.csv`

---

## Additional Investigation Pathways

### **Cross-Reference with Full LinkedIn Network**

If available, search the complete LinkedIn connections CSV (not just Harvard):
- May find Oskar Schulz, Virat Talwar, or Scott Wu through non-Harvard paths
- Would reveal if these are genuine connections established through other means

### **ProDex Labs Deep Dive**

Found 2 connections at ProDex Labs:
1. Kushan Weerakoon (claimed relationship)
2. Rick Li ("ProDex Labs | Prev. SpaceX | Applied Math @ Harvard")

Questions:
- Is ProDex Labs the same as the "PRODEX LABS" mentioned in the dataroom?
- What is the relationship between ProDex Labs and the PROD accelerator?
- Should search for all ProDex-related connections

### **Founder Ecosystem Analysis**

Search for people with founder/CEO/CTO titles in the connections to identify:
- Other Harvard founders he's connected to
- Whether these match any portfolio companies or sourcing claims
- The quality of his actual founder network vs. claimed network

Suggested search:
```bash
grep -i "founder\|co-founder\|ceo\|cto" connections_harvard.csv
```

---

## Interpretation & Caveats

### **Limitations of LinkedIn Data**

1. **Not all connections are on LinkedIn:** Some founders may not maintain active LinkedIn profiles
2. **Connection timing:** May have connected after the dataroom was created
3. **Privacy settings:** Some connections may be hidden or not searchable

### **Alternative Explanations**

1. **Non-LinkedIn relationships:** May know these people through in-person Harvard networks, not LinkedIn
2. **Recent graduates:** Class of '28 (Henry Zhou) may not be on LinkedIn yet
3. **Privacy-conscious founders:** High-profile founders may limit public connections
4. **Different platforms:** Relationships may exist on other platforms (email, phone, in-person only)

### **What This Analysis Cannot Determine**

- **Relationship quality:** Even if connected, doesn't prove "close friendship"
- **Relationship recency:** Connection dates unknown
- **Bidirectional acknowledgment:** LinkedIn connection doesn't mean mutual recognition of "friendship"
- **Practical access:** Connection doesn't guarantee ability to get meetings or deals

---

## Conclusion

The LinkedIn data reveals a **significant gap between claimed relationships and verifiable connections**, particularly for the three highest-value companies (Cursor, Mercor, Cognition/Devin) that represent $30B in combined valuation.

**Key takeaways:**
1. ❌ **0 out of 3 "already scaling" company relationships verified** (0%)
2. ✅ **2 out of 3 "next wave" company relationships verified** (67%)
3. 🚩 **No connections found to PROD accelerator** despite claiming it as key sourcing advantage
4. 🚩 **The most valuable relationships are the least verifiable**

This warrants deeper investigation through:
- Interview references with the claimed contacts
- Portfolio company founder references
- Cross-checking with other data sources (GitHub, Twitter, etc.)
- Direct outreach to verify relationships
