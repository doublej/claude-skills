# Platform Export Specifications

## Social Media

### X / Twitter
| Type | Dimensions | Aspect | Notes |
|------|-----------|--------|-------|
| In-feed image | 1200×675 | 16:9 | Optimal for timeline display |
| Card image | 800×418 | ~1.91:1 | Link preview cards |
| Header | 1500×500 | 3:1 | Profile banner |

Safe zone: keep key content 60px from edges (mobile crop).

**Multi-image strategy:** X supports up to 4 images per post. For multi-screenshot promotions, use dual side-by-side layouts on middle images to pack more content. See compose-guide.md for the full mapping logic.

### Threads
| Type | Dimensions | Aspect | Notes |
|------|-----------|--------|-------|
| Portrait (optimal) | 1080×1350 | 4:5 | Maximum feed real estate |
| Square | 1080×1080 | 1:1 | Also supported |
| Landscape | 1080×566 | ~1.91:1 | Loses vertical space |

### LinkedIn
| Type | Dimensions | Aspect | Notes |
|------|-----------|--------|-------|
| Square post | 1200×1200 | 1:1 | Best engagement |
| Landscape | 1200×627 | ~1.91:1 | Link previews |
| Portrait | 1080×1350 | 4:5 | Supported |

### Substack
| Type | Dimensions | Aspect | Notes |
|------|-----------|--------|-------|
| Article header | 1456×750 | ~1.94:1 | Hero image |
| Inline image | 1456×auto | — | Full-width in article |

## Developer Platforms

### GitHub
| Type | Dimensions | Aspect | Notes |
|------|-----------|--------|-------|
| Social preview | 1280×640 | 2:1 | Repository card image |
| README image | 1200×auto | — | Width-constrained to container |

### Product Hunt
| Type | Dimensions | Aspect | Notes |
|------|-----------|--------|-------|
| Gallery image | 1270×760 | ~1.67:1 | Product gallery |
| Thumbnail | 240×240 | 1:1 | Small logo/icon |

## App Stores

### Apple App Store
| Device | Dimensions | Notes |
|--------|-----------|-------|
| iPhone 6.9" | 1320×2868 | Required (iPhone 16 Pro Max) |
| iPhone 6.7" | 1290×2796 | Required (iPhone 15 Pro Max) |
| iPhone 6.5" | 1284×2778 | Optional |
| iPad 13" | 2064×2752 | Required for iPad apps |
| Mac | 2880×1800 | Required for Mac apps |

Up to 10 screenshots per localization. First 3 are most important (visible without scrolling).

### Google Play Store
| Device | Dimensions | Notes |
|--------|-----------|-------|
| Phone | 1080×1920 | 16:9 minimum |
| Tablet 7" | 1080×1920 | Same as phone |
| Tablet 10" | 1920×1200 | Landscape |

## General Guidelines

- Always export as PNG for lossless quality
- Use 2x/3x assets where the platform serves high-DPI
- Keep file size under 5MB per image (most platform limits)
- Test that text is legible at the platform's typical display size
