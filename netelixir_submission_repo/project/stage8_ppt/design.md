# Design Document

## Project
- **Name:** AIgnition Executive Report
- **Type:** Business Insight / Strategic Consulting Report
- **Audience:** Marketing executives, data science leaders, C-suite stakeholders
- **Language:** English

## Design Philosophy
- **Conclusion first (Pyramid Principle):** Action titles are complete insight sentences
- **Ultimate restraint:** Zero decoration — no rounded corners, shadows, gradients, or colored cards
- **Typography as hierarchy:** Visual hierarchy through font size, weight, and serif/sans-serif contrast
- **High density:** 90%+ content fill rate; no empty pages
- **Verifiability:** All data cites sources

## Color System

```yaml
colors:
  primary: "#1a1a2e"      # Dark navy — AIgnition brand, titles, headers
  accent: "#4a90e2"       # Bright blue — charts, key data, emphasis
  background: "#ffffff"     # White — page backgrounds
  text: "#1f2937"         # Dark gray — body text
  secondary: "#6b7280"    # Medium gray — captions, sources, footnotes
  light: "#f3f4f6"        # Light gray — alternating table rows, subtle fills
  border: "#e5e7eb"       # Border gray — table borders, divider lines
  white: "#ffffff"        # Pure white
```

## Font System

```yaml
fonts:
  title: "Oranienbaum"      # Serif, elegant, professional authority for cover/action titles
  body: "Liter"             # Sans-serif, modern, clean, rational for body text and data
  caption: "Liter"          # Same sans-serif for captions
```

## Text Styles

```yaml
textStyles:
  coverTitle:
    fontSize: 52
    color: "$primary"
    fontFamily: "Oranienbaum"
    lineHeight: 1.2
  coverSubtitle:
    fontSize: 22
    color: "$secondary"
    fontFamily: "Liter"
    lineHeight: 1.4
  actionTitle:
    fontSize: 26
    color: "$primary"
    fontFamily: "Oranienbaum"
    lineHeight: 1.3
  body:
    fontSize: 18
    color: "$text"
    fontFamily: "Liter"
    lineHeight: 1.5
  caption:
    fontSize: 12
    color: "$secondary"
    fontFamily: "Liter"
    lineHeight: 1.3
  bigNumber:
    fontSize: 48
    color: "$primary"
    fontFamily: "Oranienbaum"
    lineHeight: 1.1
  sectionHeader:
    fontSize: 20
    color: "$primary"
    fontFamily: "Oranienbaum"
    lineHeight: 1.3
  highlight:
    fontSize: 18
    color: "$accent"
    fontFamily: "Liter"
    lineHeight: 1.5
```

## Table Styles

```yaml
tableStyles:
  default:
    fontSize: 14
    fontFamily: "Liter"
    headerFill: "$primary"
    headerColor: "$white"
    headerBold: true
    bodyFill: ["$white", "$light"]
    bodyColor: "$text"
    border:
      style: solid
      width: 1
      color: "$border"
    headerBorder:
      style: solid
      width: 1
      color: "$primary"
```

## Layout Grid

- **Page size:** 1280 x 720 px
- **Top margin:** 40 px
- **Left margin:** 60 px
- **Right margin:** 60 px
- **Bottom margin:** 40 px
- **Content width:** 1160 px
- **Content height:** 640 px

## Common Elements

- **Top accent bar:** [0, 0, 1280, 4] solid `$primary`
- **Action title:** [60, 20, 1160, 36] — fontSize 26, Oranienbaum, bold, `$primary`
- **Divider line:** [60, 62, 1160, 1] solid `$border`
- **Content area:** [60, 75, 1160, 585] 
- **Source footer:** [60, 670, 1000, 16] — fontSize 12, `$secondary`
- **Page number:** [1180, 670, 40, 16] — fontSize 12, `$secondary`, right-aligned

## Decoration Rules
- **NO shadows, gradients, rounded corners, or decorative icons**
- **NO abstract background textures or stock photos**
- **Solid fills only**
- **Divider lines for structural separation**
- **Informational images only** (product photos, technical diagrams, brand logos)

## Chart Style
- Primary data series: `$primary` or `$accent`
- Secondary series: neutral grays (`#9ca3af`, `#d1d5db`)
- Grid lines: `#f0f0f0`
- Axis labels: `#6b7280`, fontSize 12
- Data labels: show for key values only
- Legends: bottom or right

## Image Strategy
- Cover: Solid color or subtle brand-appropriate background (no stock photos)
- Content pages: No decorative images; use charts, tables, shapes, and text only
- Information density prioritized over visual embellishment
