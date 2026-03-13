# Review Checklist — source.pdf

**Batch**: `ncdit-audit-10-20260311-041056`
**Pipeline Status**: FAIL: 3/4 chunks failed (below 50% threshold): chunk 1 (pages 1-2): API call budget exhausted for source.pdf [pages 1-2]; chunk 3 (pages 5-6): API call budget exhausted for source.pdf [pages 5-6]; chunk 4 (pages 6-7): API call budget exhausted for source.pdf [pages 6-7]
**Processing Time**: 27.2s
**Confidence**: N/A
**Edge Case Flags**: none

---

## Quality Fix Validation

### Fix 1: Image Resolution (CRITICAL)
- [ ] Images render correctly (no broken image icons)
- [ ] Image render rate ~80%+
- Log: `(not found in logs)`

### Fix 2: Decorative Image Guard
- [ ] Background/pattern images remain decorative
- [ ] Government seals and content photos are correctly shown

### Fix 3: Running Header Deduplication
- [ ] No repeated section headings
- Log: `(not found in logs)`

### Fix 4: Table Extraction Accuracy
- [ ] Tables have `<th>` header cells
- [ ] Table count matches baseline
- Log: `(not found in logs)`

### Fix 5: Link Fragmentation
- [ ] No adjacent `<a>` tags with same href
- Log: `(not found in logs)`

### Fix 6: Bare Domain Auto-Linking
- [ ] `.gov`/`.edu`/`.org` bare URLs are clickable links

### Fix 7: CSS Fallback
- [ ] `(opens in new window)` text is NOT visible on screen

---

## Audit Results
Score=15, Grade=Critical, Routing=reject

## Visual Review Notes

- Overall quality: _[good / acceptable / needs work]_
- Issues found: _[describe any issues]_
