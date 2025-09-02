# NexusEnroll CSS Design System Documentation

## Overview

This document outlines the design system implemented for the NexusEnroll application to maintain UI consistency across all components.

## File Structure

### Core Files

1. **design-system.css** - Main design system with all CSS variables, base styles, and reusable components
2. **dashboard-overrides.css** - Global overrides to ensure consistency across all dashboards
3. **admin.css** - Admin dashboard specific styles (extends design system)
4. **student.css** - Student dashboard specific styles (extends design system)
5. **faculty.css** - Faculty dashboard specific styles (extends design system)
6. **enrollment.css** - Enrollment management styles
7. **scheduleProgress.css** - Schedule and progress tracking styles
8. **reports.css** - Reports dashboard styles

### Loading Order

All HTML templates should load CSS in this order:

1. design-system.css (base system)
2. Component-specific CSS (admin.css, student.css, etc.)
3. Feature-specific CSS (enrollment.css, etc.)
4. dashboard-overrides.css (global consistency)

## Design System Variables

### Color Palette

```css
/* Primary Colors */
--primary-navy: #0d2d66;
--primary-blue: #1e4fa3;
--primary-light-blue: #e3f0ff;
--primary-accent: #ffb347;
--primary-accent-light: #ffcc80;
--primary-accent-dark: #ff9800;

/* Status Colors */
--success-color: #10b981;
--warning-color: #f59e0b;
--danger-color: #ef4444;
--info-color: #3b82f6;

/* Background Colors */
--bg-primary: #f9f9f9;
--bg-secondary: #ffffff;
--bg-card: #ffffff;
```

### Typography

```css
/* Font Family */
--font-family-primary: "Segoe UI", "Inter", -apple-system, BlinkMacSystemFont, Arial,
  sans-serif;

/* Font Sizes */
--text-xs: 0.75rem; /* 12px */
--text-sm: 0.875rem; /* 14px */
--text-base: 1rem; /* 16px */
--text-lg: 1.125rem; /* 18px */
--text-xl: 1.25rem; /* 20px */
--text-2xl: 1.5rem; /* 24px */
--text-3xl: 1.875rem; /* 30px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Spacing

```css
--space-xs: 0.25rem; /* 4px */
--space-sm: 0.5rem; /* 8px */
--space-md: 0.75rem; /* 12px */
--space-lg: 1rem; /* 16px */
--space-xl: 1.25rem; /* 20px */
--space-2xl: 1.5rem; /* 24px */
--space-3xl: 2rem; /* 32px */
```

### Border Radius

```css
--radius-sm: 4px;
--radius-md: 6px;
--radius-lg: 8px;
--radius-xl: 12px;
--radius-2xl: 16px;
```

## Component Classes

### Headers

```css
.nexus-header      /* Standard application header */
/* Standard application header */
.nexus-logo        /* Application logo styling */
.nexus-portal-badge; /* Portal type badge (Admin, Student, Faculty) */
```

### Buttons

```css
.btn               /* Base button class */
/* Base button class */
.btn-primary       /* Primary action buttons */
.btn-secondary     /* Secondary action buttons */
.btn-accent        /* Accent colored buttons (Add, Create) */
.btn-success       /* Success state buttons */
.btn-warning       /* Warning state buttons */
.btn-danger        /* Danger/delete buttons */
.btn-sm            /* Small buttons */
.btn-lg; /* Large buttons */
```

### Cards

```css
.card              /* Base card container */
/* Base card container */
.card-header       /* Card header section */
.card-title; /* Card title text */
```

### Tables

```css
.table-container   /* Table wrapper with scroll */
/* Table wrapper with scroll */
.table; /* Styled table */
```

### Forms

```css
.form-group        /* Form field container */
/* Form field container */
.form-label        /* Form field labels */
.form-input        /* Text inputs */
.form-select       /* Select dropdowns */
.form-textarea; /* Textarea fields */
```

### Navigation

```css
.tabs              /* Tab navigation container */
/* Tab navigation container */
.tab-button        /* Individual tab buttons */
.tab-content; /* Tab content areas */
```

### Status Indicators

```css
.status-active     /* Active status badge */
/* Active status badge */
.status-inactive   /* Inactive status badge */
.status-warning    /* Warning status badge */
.status-danger; /* Danger status badge */
```

### Layout

```css
.welcome-section   /* Welcome message container */
/* Welcome message container */
.content; /* Main content area */
```

## Best Practices

### 1. Use Design System Variables

Always use CSS variables instead of hardcoded values:

```css
/* Good */
color: var(--primary-navy);
padding: var(--space-lg);

/* Avoid */
color: #0d2d66;
padding: 16px;
```

### 2. Follow Component Hierarchy

Load CSS files in the correct order to maintain consistency:

1. Base design system
2. Component-specific styles
3. Feature-specific styles
4. Global overrides

### 3. Use Semantic Class Names

Choose class names that describe the purpose, not the appearance:

```css
/* Good */
.btn-primary
.status-active
.welcome-section

/* Avoid */
.blue-button
.green-text
.big-box;
```

### 4. Maintain Responsive Design

Use the provided responsive utilities and breakpoints:

```css
@media (max-width: 768px) {
  /* Mobile styles */
}
```

### 5. Ensure Accessibility

- Use proper contrast ratios
- Include focus states
- Provide semantic HTML structure

## Migration from Legacy Styles

### Phase 1: Global System (Completed)

- ✅ Created design-system.css with variables
- ✅ Updated main dashboard templates
- ✅ Created global overrides

### Phase 2: Component Updates (In Progress)

- ✅ Updated admin dashboard styles
- ✅ Updated student dashboard styles
- ✅ Updated faculty dashboard styles
- 🔄 Update remaining component CSS files

### Phase 3: Feature Integration

- 🔄 Update enrollment management styles
- 🔄 Update schedule progress styles
- 🔄 Update reports dashboard styles

### Phase 4: Legacy Cleanup

- 🔄 Remove redundant CSS
- 🔄 Consolidate similar components
- 🔄 Optimize for performance

## Common Issues and Solutions

### Issue: Inconsistent Button Styles

**Solution:** Use the standardized `.btn` classes with appropriate modifiers

### Issue: Misaligned Headers

**Solution:** Ensure all headers use `.nexus-header` class and proper structure

### Issue: Spacing Inconsistencies

**Solution:** Use the spacing variables (`--space-*`) instead of custom values

### Issue: Color Variations

**Solution:** Use the defined color variables from the design system

## Testing Checklist

- [ ] All dashboards use consistent header styling
- [ ] Button styles are uniform across components
- [ ] Tables follow the same visual pattern
- [ ] Forms use consistent styling
- [ ] Colors match the design system palette
- [ ] Spacing is consistent using design system variables
- [ ] Typography follows the established hierarchy
- [ ] Responsive design works on mobile devices
- [ ] Focus states are visible for accessibility
- [ ] Loading states are consistent

## Maintenance

### Adding New Components

1. Use design system variables
2. Follow existing naming conventions
3. Test across all dashboard types
4. Document new patterns
5. Update this documentation

### Modifying Existing Styles

1. Check impact across all components
2. Update design system variables if needed
3. Test responsive behavior
4. Verify accessibility compliance
5. Update documentation

### Performance Optimization

1. Minimize CSS file sizes
2. Combine similar selectors
3. Remove unused styles
4. Optimize for critical rendering path
5. Monitor CSS bundle size
