---
name: synergy-reviewer
description: Evaluate synergy opportunities against ICAEW and PwC assurance frameworks. Use when reviewing cost or revenue synergy cases, challenging assumptions, or preparing for auditor review.
---

# Synergy Reviewer

Structured challenge and evaluation of synergy opportunities against ICAEW Tech 04/20 and PwC assurance frameworks.

## When to Use

- Reviewing a cost or revenue synergy case
- Preparing synergy documentation for PwC review
- Challenging assumptions on a synergy initiative
- Assessing if a synergy is "assurable" or needs reclassification
- Gap analysis before auditor submission

## Assessment Framework

### The "Very Little Risk" Standard

> Per ICAEW: "There should be **very little risk** that the quantum of synergies announced is not achieved."

This is the gold standard. Every synergy must pass this test.

## Review Workflow

### Step 1: Gather Context

Ask the user:
```
What synergy would you like me to review?

Please provide:
1. Synergy name and area (e.g., "CMB LC Front Office")
2. Gross synergy amount (USD m)
3. Brief description of the synergy case
4. Any supporting documentation or notes

I'll evaluate it against ICAEW and PwC frameworks.
```

### Step 2: Apply the Four Attributes Test

Evaluate against ICAEW's four core attributes:

| Attribute | Question | Pass/Fail |
|-----------|----------|-----------|
| **Relevant** | Does this synergy influence shareholder decisions? Is timing clear? | |
| **Reliable** | Is it based on sound business analysis, not hypothetical? | |
| **Understandable** | Are assumptions, risks, and mitigations clearly disclosed? | |
| **Comparable** | Can this be validated against future historical results? | |

### Step 3: Transaction Attribution Test

**Critical Question**: Could this synergy have been achieved without the transaction?

Challenge prompts:
- "What specifically changes post-transaction that enables this?"
- "Why wasn't this done before under CCT arrangements?"
- "Is this really transaction-enabled or organic growth?"

#### Structural vs Operational Barriers

**STRUCTURAL barriers** (stronger evidence for transaction-enablement):
- Legal/regulatory constraints (e.g., card scheme rules, listing requirements)
- Contractual obligations requiring arm's length treatment
- Minority shareholder rights preventing preferential arrangements
- Data sharing restrictions between separate entities

**OPERATIONAL barriers** (weaker evidence - challenge these):
- Investment budget prioritisation
- Management attention/focus
- Organisational alignment
- Technology integration complexity

> **Key insight:** If the barrier was operational (e.g., "we couldn't agree on investment"), it may NOT be transaction-enabled. If the barrier was structural (e.g., "card schemes require interchange between separate banks"), it IS transaction-enabled.

#### Strong Transaction Attribution Example

**On-Us Card Transactions:** Amber and Jade have >50% combined card market share in HK. Currently, Amber cards at Jade terminals pay interchange to Visa/Mastercard because card scheme rules require it between separate banking entities. Post-privatisation, these could be treated as "on-us" internal transfers, eliminating interchange fees.

- ✅ **Structural barrier**: Card scheme rules legally require interchange between separate banks
- ✅ **Cannot be done pre-transaction**: Separate listing prevents internal treatment
- ✅ **Quantifiable**: Transaction volume × interchange rate
- ✅ **Low execution risk**: Contractual/system change, not behavioural

If the answer is unclear, it is **not a synergy** and should be:
- Excluded from quantified synergy statement
- Potentially included as qualitative "transaction-enabled opportunity" (not quantified)
- Flagged for further analysis

### Step 4: Evidence Checklist

For **Cost Synergies**, verify:

| Evidence | Status | Notes |
|----------|--------|-------|
| Cost baseline documented | ⬜ | |
| Headcount baseline with FTE detail | ⬜ | |
| KPIs for capacity (workload per FTE) | ⬜ | |
| Amber capacity to absorb Jade | ⬜ | |
| Process mapping (Jade → Amber) | ⬜ | |
| Retained FTE sufficient for residual | ⬜ | |
| Business owner validation | ⬜ | |
| Market benchmarks referenced | ⬜ | |

For **Revenue Synergies**, verify:

| Evidence | Status | Notes |
|----------|--------|-------|
| Addressable customer pool quantified | ⬜ | |
| Penetration rate justified | ⬜ | |
| Revenue model documented | ⬜ | |
| Cannibalization assessed | ⬜ | |
| Why transaction-enabled explained | ⬜ | |
| Alternative view articulated | ⬜ | |
| External benchmarks referenced | ⬜ | |
| Business owner validation | ⬜ | |
| **Data provider vs sign-off authority identified** | ⬜ | Distinguish functional leads who supply data from executives (CEO/CFO) who PwC will interview |

### Step 5: Challenge Questions

Apply these probing questions based on synergy type:

**For FTE Reductions:**
- "What is the capacity headroom in the absorbing function?"
- "How was the FTE baseline calculated - point in time or average?"
- "What attrition rate is assumed and how does this compare to historical?"
- "Are severance costs included in CTA at realistic levels?"

**For Process Consolidation:**
- "Are the Jade and Amber processes truly comparable?"
- "What investment is needed to harmonise platforms/tools?"
- "Is the timeline realistic given technology dependencies?"

**For Revenue Synergies:**
- "What is the counterfactual - why didn't this happen before?"
- "How does the assumed penetration compare to comparable propositions?"
- "Is there cannibalization of existing Jade or Amber products?"
- "What happens if customer take-up is 50% of plan?"
- "Who provides the data vs who has authority to sign off? PwC will interview executives (CEO/CFO), not data leads."

**For Delisting/Governance Savings:**
- "Which specific obligations cease post-privatisation?"
- "Are there any residual entity-specific requirements?"
- "How quickly can costs actually be removed?"

### Step 6: Rate the Synergy

Assign ratings per PwC framework:

**Management Validation:**
- ✅ Validated by business/functional owner
- ⬜ Not yet validated

**Evidence Status:**
- 🟢 G - Evidence exists or is being obtained
- 🟡 A - Evidence to be developed post-vote
- 🔴 R - No evidence exists, difficult to produce

**Synergy Logic:**
- 🟢 High - Readily achievable, practically executable, in line with market experience
- 🟡 Medium - Plausible but execution uncertainty, ambitious vs market
- 🔴 Low - Theoretical, not grounded, high execution risk

### Step 7: Provide Recommendations

Output a structured review:

```markdown
## Synergy Review: [Name]

### Summary
| Metric | Value |
|--------|-------|
| Gross Synergy | $XXm |
| Validation | ✅/⬜ |
| Evidence | 🟢/🟡/🔴 |
| Logic | High/Medium/Low |
| Recommendation | Include/Qualify/Exclude |

### Key Findings

**Strengths:**
- [What's working well]

**Gaps:**
- [What's missing or weak]

**Challenge Areas:**
- [Questions that need answers]

### Recommendations

1. [Specific action to strengthen the case]
2. [Evidence to obtain]
3. [Assumption to validate]

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | H/M/L | H/M/L | [Action] |

### Suggested Contingency

Based on [factors], recommend [X]% contingency for this synergy.
```

## Quick Reference: Red Flags

Watch for these common issues:

| Red Flag | Issue | Action |
|----------|-------|--------|
| "Top-down percentage" | Not bottom-up | Require granular analysis |
| "In line with past deals" | No specific analysis | Get comparable evidence |
| "To be validated" | No business sign-off | Get owner confirmation |
| "Capacity exists" | No headroom analysis | Quantify spare capacity |
| "Could have done anyway" | Not transaction-enabled | Reclassify or exclude |
| "Revenue uplift" | Often organic growth | Prove counterfactual |
| No CTA estimate | Incomplete case | Quantify costs to achieve |
| No phasing | Not implementable | Develop timeline |
| "Source: FRP" | Insufficient sourcing | Get specific document + date |
| Hardcoded figures | No traceability | Link to source cell |
| Cumulative totals | Wrong metric | Use run-rate only |
| Undefined acronyms | Not understandable | Add glossary |
| Data provider as sign-off | Wrong authority level | Verify exec-level ownership (CEO/CFO) |
| "Investment budget disagreement" | Operational barrier language | NOT transaction-enabled - exclude |
| "Management preference/control" | Operational barrier language | NOT transaction-enabled - exclude |
| "Couldn't agree on priorities" | Operational barrier language | NOT transaction-enabled - exclude |

---

## 80/20 Prioritization

When time-constrained, focus efforts on synergies with the strongest transaction attribution:

**Prioritize (worth defending to PwC):**
- Synergies with explicit CCT/structural barrier in source papers
- Synergies where sponsor paper states "could only occur if we privatize" or similar
- Synergies with legal/contractual barriers (e.g., card scheme rules)

**Deprioritize (put in "internal upside" bucket):**
- Synergies where meeting notes cite operational barriers
- Capability catch-up or "co-build" initiatives without structural justification
- Initiatives that could theoretically be done under CCT arrangements

> **Key insight:** Don't waste time building evidence for weak attribution cases. If meeting notes say "the barrier was management preference not legal feasibility" - that synergy is NOT assured. Move on.

---

## KPMG Review Standards

Based on KPMG detailed synergy reviews, apply these specific checks that PwC will scrutinize.

### Source Documentation Drill-Down

For every data point, ask:

| Question | Why It Matters |
|----------|----------------|
| "What is the specific source?" | "FRP" alone is insufficient - need document name |
| "What date was this extracted?" | Data ages quickly; date provides context |
| "Is this internal or external?" | External benchmarks carry more weight |
| "Is this the most granular view?" | Aggregated data hides assumptions |

**Example challenge:**
> "The customer base shows 424,741 - what is the specific source and date? Noting we would need more detail than just 'FRP'"

### Data Linkage Audit

Check for:

| Issue | Question to Ask |
|-------|-----------------|
| **Hardcoded values** | "These figures appear hardcoded - where do they come from?" |
| **Inconsistent figures** | "This figure is 25,200 here but 25,000 above - why the difference?" |
| **Screenshot references** | "This screenshot is sourced to November 2025 dashboard - can we confirm the date and system?" |
| **Broken links** | "How do the figures highlighted link to the calculation?" |

**Example challenge:**
> "Hardcoded figures are slightly different to above - why? Where are they from? Would be better to link to the source."

### Assumption Benchmarking

For every assumption, require:

| Check | Standard |
|-------|----------|
| **Benchmarked** | Compare to actuals or market data |
| **Differential explained** | If segments differ, explain why |
| **Pending items flagged** | Mark "Pending for A" clearly |

**Example challenges:**
> "Assumption only. Pending for A - would need some form of benchmarking or actuals to verify data"
> "Why would we expect twice the success for PSE customers vs PP? What justifies 0.10% vs 0.05%?"

### FX Rate Standards

| Check | Requirement |
|-------|-------------|
| Rate stated explicitly | "USD/HKD 7.8" not just "7.8" |
| Date provided | "As of [date]" |
| Consistency | Same rate throughout model |

**Example challenge:**
> "Is the 7.8 an exchange rate? What date is that from?"

### Run-Rate vs Cumulative Error

**Critical**: Synergies are run-rate, not cumulative.

| Wrong | Right |
|-------|-------|
| "Total: $2,380k over 5 years" | "Run-rate: $569k by Year 5" |
| Summing annual figures | Stating the steady-state annual value |

**Example challenge:**
> "Unless calculated benefit is not expected to carry on into the future, then a sum is not required for synergies - we are only looking at the run-rate figure"

### Acronym & Terminology Check

Before submission, verify:
- [ ] All acronyms defined on first use
- [ ] Customer segment codes explained (PP, PSE, PB, etc.)
- [ ] Product codes defined
- [ ] Glossary table included

**Example challenge:**
> "What do the acronyms (e.g. PB) mean?"

### Revenue Model Specific Checklist

For revenue synergies, verify each element:

| Element | Check | Status |
|---------|-------|--------|
| Customer base | Source + date documented | ⬜ |
| Segmentation | All segment codes defined | ⬜ |
| Penetration rates | Benchmarked or evidenced | ⬜ |
| Revenue per customer | Calculation shown with source | ⬜ |
| Incremental calculation | Logic clear and correct | ⬜ |
| FX assumption | Rate + date stated | ⬜ |
| Hardcoded values | All traced to source | ⬜ |
| Differential assumptions | Rationale provided | ⬜ |
| Screenshots | Dated and sourced | ⬜ |
| Output metric | Run-rate (not cumulative) | ⬜ |
| **Transaction attribution quotes** | Direct quotes from source documents (stronger than interpretation) | ⬜ |
| CTA included | Costs quantified | ⬜ |
| ROI calculation | Methodology clear | ⬜ |

### Sample KPMG-Style Comments to Generate

When reviewing, generate comments like:

**On sourcing:**
> "What is the specific source and date of the source? Noting we would need more detail than [generic reference]"

**On linkage:**
> "How do the figures highlighted link to [reference]?"
> "Assume hardcoded figures come from above but would be better to link to the above and source"

**On assumptions:**
> "Assumption only. Pending for A - would need some form of benchmarking or actuals to verify data"

**On differentials:**
> "Why would we expect [X] for [segment A] vs [Y] for [segment B]?"

**On FX:**
> "Is the [number] an exchange rate? What date is that from?"

**On run-rate:**
> "Unless calculated benefit is not expected to carry on into the future, then a sum is not required for synergies - we are only looking at the run-rate figure"

**On terminology:**
> "What do the acronyms (e.g. [acronym]) mean?"

**On transaction attribution:**
> "What specific statement in the source document supports this being transaction-enabled? Direct quotes are stronger than interpretation."
> "The source states '[exact quote]' - this evidences the structural barrier"

## Reliability Hierarchy

Per ICAEW, some synergies are inherently more reliable:

**More Reliable (lower contingency):**
- Duplicate board costs
- Central overheads (where clearly duplicate)
- Headcount with access to detailed data
- Delisting costs with clear documentation

**Less Reliable (higher contingency):**
- Revenue enhancements
- Procurement savings
- Synergies based only on public information
- Operational efficiencies requiring behavioural change

## Output Formats

### Quick Assessment (2-minute review)
```
[Synergy Name]: [Rating] - [One-line summary]
Key gap: [Main issue]
Action: [Next step]
```

### Full Review (detailed analysis)
Use the full template from Step 7.

### Batch Summary (multiple synergies)
```
| Synergy | $m | Validation | Evidence | Logic | Action |
|---------|-----|------------|----------|-------|--------|
| [Name] | [X] | ✅/⬜ | 🟢🟡🔴 | H/M/L | [Next step] |
```

## Integration with Falcon Vault

When reviewing synergies for Project Falcon, reference:
- `PwC Evidence Requirements by Initiative.md` - Area-specific checklists
- `Cost Synergy Assessment Template.md` - Per-initiative documentation
- `Revenue Synergy Assessment Template.md` - Revenue case structure
- `PwC Interim Status Update - December 2025.md` - Current gap status

## Example Usage

**User:** "Review the CMB LC Front Office synergy of $15m"

**Response:**
"I'll review the CMB LC Front Office synergy. Let me gather the context and apply the ICAEW/PwC framework..."

[Runs through Steps 1-7, produces structured output]
