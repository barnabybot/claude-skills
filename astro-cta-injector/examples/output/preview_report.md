# CTA Injection Preview Report

**Generated:** 2025-01-21 10:35:00 UTC  
**CTA Type:** newsletter  
**Placement Strategy:** after-paragraph-50%  
**Mode:** DRY RUN (no changes made)

---

## Summary

| Metric | Value |
|--------|-------|
| Posts Scanned | 3 |
| Posts Qualified | 2 |
| Posts Skipped | 1 |
| Estimated Injections | 2 |

---

## Qualified Posts

### 1. productivity-tips.md

**Score:** 8.2/10 ⭐  
**Placement:** After paragraph 4 of 8  
**Matched Keywords:** productivity, tip, workflow, habit, strategy

**Preview Location:**

```markdown
## 4. Batch Similar Tasks

Context switching is the productivity killer. Group similar activities together...

<!-- CTA WILL BE INJECTED HERE -->

## 5. Design Your Environment

Your physical space shapes your behavior...
```

**CTA Content:**
```html
<aside class="cta cta-newsletter" data-cta-type="newsletter">
  <h3>Get Weekly Productivity Insights</h3>
  <p>Join 10,000+ readers getting actionable tips every Tuesday.</p>
  <form action="/api/newsletter/subscribe" method="post">
    <input type="email" placeholder="Your email" required />
    <button type="submit">Subscribe Free</button>
  </form>
</aside>
```

---

### 2. task-management.md

**Score:** 7.3/10 ⭐  
**Placement:** After paragraph 6 of 12  
**Matched Keywords:** productivity, workflow, habit, framework

**Preview Location:**

```markdown
### 3. Organize by Context

Traditional organization by project or category often fails...

<!-- CTA WILL BE INJECTED HERE -->

### 4. Review Systematically

The weekly review is where task management systems live or die...
```

**CTA Content:**
```html
<aside class="cta cta-newsletter" data-cta-type="newsletter">
  <h3>Get Weekly Productivity Insights</h3>
  <p>Join 10,000+ readers getting actionable tips every Tuesday.</p>
  <form action="/api/newsletter/subscribe" method="post">
    <input type="email" placeholder="Your email" required />
    <button type="submit">Subscribe Free</button>
  </form>
</aside>
```

---

## Excluded Posts

### weekly-update.md

**Score:** 0.0/10  
**Reason:** Score below minimum threshold (5.0)

Post is too short (42 words) and contains no relevant keywords.

---

## Next Steps

To apply these changes, run:

```bash
python scripts/inject_ctas.py \
  --input ./output/scored_posts.json \
  --dry-run false
```

⚠️ **Backups will be created automatically in `./backups/`**
