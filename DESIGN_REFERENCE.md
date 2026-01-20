# 🎨 AgriSmart Design Reference Guide

## Quick Style Reference

### **Primary Colors**
```
Dark Green Navbar:    #228B22
Primary Green:        #4CAF50
Forest Green:         #388E3C
Light Green:          #C8E6C9
```

### **Page-Specific Colors**
```
Login/Register:       Green (#228B22 → #388E3C)
Crop Prediction:      Green (#4CAF50 → #388E3C)
Fertilizer:           Orange (#FFC107 → #F57F17)
Irrigation:           Blue (#0D6EFD → #0A54CC)
Dashboard:            Green (#228B22 → #1e7e1e)
```

---

## Component Styles Quick Reference

### **Cards**
```css
.card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 15px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.15);
}
```

### **Buttons**
```css
.btn {
    border-radius: 12px;
    padding: 12px 30px;
    font-weight: 700;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.btn-success {
    background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
}
```

### **Form Controls**
```css
.form-control, .form-select {
    border-radius: 12px;
    border: 2px solid rgba(76, 175, 80, 0.2);
    background: rgba(255, 255, 255, 0.95);
}

.form-control:focus {
    border-color: #4CAF50;
    box-shadow: 0 0 0 0.2rem rgba(76, 175, 80, 0.25);
}
```

### **Section Headers**
```css
.section-header {
    background: linear-gradient(135deg, color1, color2),
                url('image.jpg') center/cover no-repeat;
    background-attachment: fixed;
    padding: 40px 0;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
}
```

---

## Typography Scale

| Element | Font Size | Font Weight | Use Case |
|---------|-----------|-------------|----------|
| h1 | 2-3rem | 700 | Page titles |
| h2 | 1.8rem | 700 | Section headers |
| h4 | 1.2rem | 600 | Card titles |
| p (lead) | 1.4rem | 400 | Intro text |
| label | 1rem | 600 | Form labels |
| small | 0.9rem | 400 | Helper text |

---

## Spacing Standards

| Spacing | Size | Usage |
|---------|------|-------|
| xs | 8px | Icon spacing |
| sm | 12px | Form padding |
| md | 20px | Card padding |
| lg | 30px | Section spacing |
| xl | 40px | Major sections |

---

## Shadow System

```css
/* Subtle */
box-shadow: 0 4px 12px rgba(0,0,0,0.1);

/* Medium */
box-shadow: 0 8px 16px rgba(0,0,0,0.15);

/* Elevated */
box-shadow: 0 15px 35px rgba(0,0,0,0.2);

/* Hover */
box-shadow: 0 20px 40px rgba(76, 175, 80, 0.25);
```

---

## Animation Reference

### **Hover Effects**
```css
/* Card Lift */
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.15);
}

/* Button Scale */
.btn:hover {
    transform: scale(1.08);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

/* Nav Link Underline */
.nav-link::after:hover {
    width: 100%;
}
```

### **Timing**
```
Standard transition: 0.3s ease
Animations: 1s ease-in-out
```

---

## Background Image Implementation

### **Hero Section**
```css
.hero-section {
    background: linear-gradient(135deg, rgba(34, 139, 34, 0.85) 0%, rgba(76, 175, 80, 0.8) 100%), 
                url('../images/a.jpg') center/cover no-repeat;
    background-attachment: fixed;
}
```

### **Login/Register**
{% raw %}
```css
.login-section {
    background: linear-gradient(135deg, rgba(76, 175, 80, 0.85) 0%, rgba(56, 142, 60, 0.8) 100%), 
                url('{{ url_for("static", filename="images/3.jpeg") }}') center/cover no-repeat;
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
```
{% endraw %}

---

## Glass-Morphism Pattern

### **Basic Card**
```css
.glass-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 15px;
}
```

### **With Gradient**
```css
.gradient-glass {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(220, 237, 200, 0.4) 100%);
    backdrop-filter: blur(10px);
    border-radius: 20px;
}
```

---

## Gradient Patterns

### **Hero Gradients**
```css
/* Green */
linear-gradient(135deg, #228B22 0%, #1e7e1e 100%)

/* Orange */
linear-gradient(135deg, #FFC107 0%, #F57F17 100%)

/* Blue */
linear-gradient(135deg, #0D6EFD 0%, #0A54CC 100%)
```

### **Overlay Patterns**
```css
/* Semi-transparent overlay */
rgba(76, 175, 80, 0.85)

/* Light overlay */
rgba(255, 255, 255, 0.95)

/* Dark overlay */
rgba(0, 0, 0, 0.3)
```

---

## Responsive Breakpoints

### **Mobile (max-width: 768px)**
```css
/* Disable parallax */
background-attachment: scroll;

/* Reduce font sizes */
.hero-section h1 { font-size: 2rem; }

/* Adjust card radius */
.card { border-radius: 12px; }
```

### **Tablet (768px - 1024px)**
```css
/* Standard styling maintained */
```

### **Desktop (1024px+)**
```css
/* Full parallax enabled */
background-attachment: fixed;

/* Full animations enabled */
```

---

## Icon Standards

### **Usage**
- Font Awesome 6.4 icons throughout
- Icon size: `fa-4x` for prominent, `fa-2x` for normal
- Color: Inherit from text or use `text-success`

### **Common Icons**
```
Navigation:    fas fa-tachometer-alt
Crop:         fas fa-brain
Fertilizer:   fas fa-flask
Irrigation:   fas fa-tint
Settings:     fas fa-cogs
User:         fas fa-user
```

---

## Form Styling Guide

### **Input Field**
```html
<div class="mb-3">
    <label for="field" class="form-label">
        <i class="fas fa-icon"></i> Label Text
    </label>
    <input type="text" class="form-control" id="field" name="field" placeholder="Helpful text">
    <small class="text-muted">Helper text</small>
</div>
```

### **Select Field**
```html
<div class="mb-3">
    <label for="select" class="form-label">
        <i class="fas fa-icon"></i> Select Option
    </label>
    <select class="form-select" id="select" name="select" required>
        <option value="">Select...</option>
        <option value="1">Option 1</option>
    </select>
</div>
```

---

## Footer Structure

```html
<footer class="text-white text-center py-5">
    <div class="container">
        <div class="row">
            <div class="col-md-4">
                <h6><i class="fas fa-icon text-success"></i> Section</h6>
                <p class="text-muted">Content</p>
            </div>
        </div>
        <hr class="bg-success opacity-50">
        <p>&copy; 2024 AgriSmart</p>
    </div>
</footer>
```

---

## Navigation Bar

{% raw %}
```html
<nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container">
        <a class="navbar-brand" href="{{ url_for('index') }}">
            <i class="fas fa-leaf"></i> AgriSmart
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link" href="#">Link</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

---

## Common CSS Classes

| Class | Purpose |
|-------|---------|
| `.card` | Content containers |
| `.btn btn-success` | Primary action |
| `.form-control` | Input fields |
| `.hero-section` | Full-screen headers |
| `.feature-card` | Feature showcases |
| `.stat-card` | Statistics display |
| `.nav-link` | Navigation items |

---

## Testing Checklist

- [ ] All backgrounds load properly
- [ ] Hover effects work smoothly
- [ ] Mobile responsive layouts
- [ ] Form focus states visible
- [ ] Text contrast is sufficient
- [ ] Animations are smooth
- [ ] Images display correctly
- [ ] Links are clickable
- [ ] Footer displays correctly
- [ ] Navigation works on mobile

---

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Gradients | ✅ | ✅ | ✅ | ✅ |
| Backdrop Filter | ✅ | ✅ | ✅ | ✅ |
| Transform | ✅ | ✅ | ✅ | ✅ |
| Box-shadow | ✅ | ✅ | ✅ | ✅ |

---

## Quick Copy-Paste Code Snippets

### **New Section Header**
{% raw %}
```html
<div class="section-header" style="background: linear-gradient(135deg, rgba(76, 175, 80, 0.85) 0%, rgba(56, 142, 60, 0.8) 100%), url('{{ url_for(\"static\", filename=\"images/a.jpg\") }}') center/cover no-repeat; background-attachment: fixed; padding: 40px 0; color: white;">
    <div class="container">
        <h1 class="mb-0" style="text-shadow: 2px 2px 4px rgba(0,0,0,0.4);">Section Title</h1>
        <p class="text-white-50">Subtitle</p>
    </div>
</div>
```
{% endraw %}

### **Feature Card**
```html
<div class="card feature-card h-100">
    <div class="card-body text-center p-4">
        <i class="fas fa-icon fa-4x text-success mb-3"></i>
        <h4>Title</h4>
        <p>Description</p>
    </div>
</div>
```

---

**Keep this guide handy for styling consistency! 🎨**
