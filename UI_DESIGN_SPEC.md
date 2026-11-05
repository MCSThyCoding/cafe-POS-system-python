# Cafe POS - UI Design Specification

**Project:** Coffee Shop Management System  
**Version:** 1.0  
**Created:** November 5, 2026

---

## Table of Contents
1. [Design System](#design-system)
2. [Component Library](#component-library)
3. [Screen Specifications](#screen-specifications)
4. [User Flows](#user-flows)
5. [Interactive States](#interactive-states)
6. [Responsive Design](#responsive-design)

---

## Design System

### Color Palette

#### Primary Colors
- **Brand:** `#c97b2e` (Coffee Gold)
- **Brand Dark:** `#a8651f` (Darker Coffee)
- **Brand Text:** `#7c3f12` (Coffee Brown)

#### Background Colors
- **Cream:** `#fff8e6` (Light Cream)
- **Sand:** `#fdf0cf` (Warm Sand)
- **Background:** `#f8fafc` (Light Gray)
- **Card:** `#ffffff` (White)

#### Text Colors
- **Ink:** `#1f2937` (Primary Text)
- **Muted:** `#6b7280` (Secondary Text)
- **Line:** `#e5e7eb` (Borders)

#### Status Colors
- **Green:** `#16a34a` (Success)
- **Red:** `#dc2626` (Error)
- **Blue:** `#2563eb` (Info)
- **Purple:** `#9333ea` (Accent)

#### Additional
- **Success Light:** `#22c55e`
- **Warning:** `#f59e0b`
- **Demo Box Background:** `#fffbe8`
- **Demo Box Border:** `#fcefbf`
- **Demo Box Text:** `#8a4b12`

---

### Typography

#### Font Family
- **Primary:** Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif
- **Monospace:** ui-monospace, Menlo, monospace

#### Font Sizes
- **Logo:** 28px
- **Page Title (H1):** 26px
- **Section Title (H2):** 26px
- **Card Title (H3):** 17px
- **Modal Title (H3):** 22px
- **Label:** 14px (medium weight)
- **Body Text:** 14px
- **Small Text:** 13px
- **Muted Text:** 14px
- **Stat Value:** 24px (bold)
- **Stat Label:** 13px
- **Navigation:** 14px
- **Role Badge:** 11px
- **Button:** 14px (semibold)
- **Button Small:** 13px
- **Pill/Tag:** 12px
- **Table Header:** 13px
- **Table Cell:** 14px
- **Product Name:** 14px (medium)
- **Product Price:** 14px (bold)
- **Product Stock:** 11px
- **Emoji/Product Icon:** 34px
- **Modal Success Icon:** 48px
- **Modal Amount:** 28px (bold)
- **Toast:** 14px

#### Font Weights
- **Normal:** 400
- **Medium:** 500
- **Semibold:** 600
- **Bold:** 700

---

### Spacing System

#### Padding
- **Card:** 20px
- **Login Card:** 32px
- **Modal Box:** 32px
- **Button:** 10px 16px
- **Button Small:** 6px 12px
- **Input:** 11px 12px
- **Input Large:** 12px 14px
- **Chip:** 8px 16px
- **Product Card:** 14px
- **Cart Line:** 10px 12px
- **Table Header:** 12px 16px
- **Table Cell:** 12px 16px
- **Page:** 24px 24px 48px
- **Sidebar:** 24px 16px
- **Alert:** 12px 16px
- **Demo Box:** 12px
- **Toast:** 12px 20px

#### Margins
- **Grid Gap:** 16px
- **Chip Gap:** 8px
- **Product Grid Gap:** 14px
- **Cart Line Gap:** 8px
- **Qty Button Gap:** 8px
- **Payment Button Gap:** 10px
- **Date Bar Gap:** 12px
- **Sidebar Border Top:** 16px
- **Page Head Margin Bottom:** 20px
- **Page Head Gap:** 12px
- **Card Title Margin Bottom:** 14px
- **Stat Value Margin Top:** 4px
- **Product Name Margin Top:** 8px
- **Product Price Margin Top:** 2px
- **Product Stock Margin Top:** 4px
- **Total Row Margin Top:** 12px
- **Total Row Padding Top:** 14px
- **Cart Line Margin Bottom:** 8px
- **Payment Margin:** 14px 0 10px
- **Modal Title Margin:** 8px 0 4px
- **Modal Label Margin Top:** 16px
- **Modal Button Margin Top:** 22px
- **Demo Box Margin Top:** 20px
- **Demo Box Paragraph Margin:** 6px 0 0
- **Error Margin:** 10px 0 0
- **Login Button Margin Top:** 18px
- **Login Muted Margin:** 4px 0 20px
- **Label Margin:** 14px 0 6px
- **Login Card Logo Margin:** 0 auto 12px
- **Search Margin Bottom:** 16px
- **Alert Margin Bottom:** 20px
- **Table Card Margin Top:** 20px

---

### Border Radius
- **Login Card:** 16px
- **Logo Badge:** 14px
- **Button:** 8px
- **Input:** 8px
- **Input Large:** 10px
- **Card:** 12px
- **Nav Item:** 10px
- **Chip:** 8px
- **Product Card:** 12px
- **Tag/Pill:** 999px (fully rounded)
- **Qty Button:** 50% (circular)
- **Cart Line:** 10px
- **Modal Box:** 16px
- **Alert:** 10px
- **Toast:** 10px
- **Stat Icon:** 8px

---

### Shadows
- **Login Card:** `0 20px 40px rgba(0,0,0,0.08)`
- **Product Card Hover:** `0 6px 16px rgba(0,0,0,0.08)`
- **Card:** `0 1px 2px rgba(0,0,0,0.03)`

---

### Transitions
- **Product Card:** Transform 0.08s, Box-shadow 0.15s

---

## Component Library

### Buttons

#### Primary Button
- **Background:** Brand color `#c97b2e`
- **Text:** White
- **Border:** None
- **Border Radius:** 8px
- **Padding:** 10px 16px
- **Font Weight:** 600
- **Font Size:** 14px
- **Hover:** Brand Dark `#a8651f`
- **Disabled:** Opacity 0.5, cursor not-allowed

#### Block Button
- Same as Primary Button
- **Width:** 100%

#### Small Button
- **Padding:** 6px 12px
- **Font Size:** 13px
- Rest same as Primary Button

#### Link Button
- **Background:** None
- **Border:** None
- **Color:** Red `#dc2626`
- **Padding:** 0
- **Font Size:** 13px
- **Margin Top:** 8px
- **Text Align:** Left

#### Payment Buttons
- **Default Background:** `#f1f5f9`
- **Active Background:** Green `#16a34a`
- **Active Text:** White
- **Border:** None
- **Border Radius:** 8px
- **Padding:** 12px
- **Font Weight:** 500
- **Grid:** 2 columns, 10px gap

#### Chip/Category Button
- **Default Background:** `#f1f5f9`
- **Active Background:** Brand `#c97b2e`
- **Active Text:** White
- **Border:** None
- **Border Radius:** 8px
- **Padding:** 8px 16px
- **Font Size:** 14px

#### Quantity Buttons
- **Background:** Sand `#fdf0cf`
- **Border:** None
- **Border Radius:** 50% (circular)
- **Width:** 28px
- **Height:** 28px
- **Font Weight:** 700

#### Delete Button
- **Background:** None
- **Color:** Red `#dc2626`
- **Icon:** 🗑

---

### Input Fields

#### Standard Input
- **Width:** 100%
- **Padding:** 11px 12px
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 8px
- **Font:** Inherit
- **Focus:** 2px solid Brand, border transparent

#### Search Input
- **Width:** 100%
- **Padding:** 12px 14px
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 10px
- **Font:** Inherit
- **Focus:** 2px solid Brand, border transparent
- **Placeholder:** 🔍 Search products...

#### Date/Month/Year Input
- **Padding:** 8px 10px
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 8px
- **Font:** Inherit
- **Focus:** 2px solid Brand, border transparent

#### Select Dropdown
- **Padding:** 8px 10px
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 8px
- **Font:** Inherit
- **Background:** White
- **Cursor:** Pointer

---

### Cards

#### Standard Card
- **Background:** White
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 12px
- **Padding:** 20px
- **Shadow:** `0 1px 2px rgba(0,0,0,0.03)`
- **Title (H3):** 17px, margin-bottom 14px

#### Stat Card
- **Layout:** Flex, space-between, center
- **Background:** White
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 12px
- **Padding:** 20px
- **Shadow:** `0 1px 2px rgba(0,0,0,0.03)`
- **Value:** 24px, bold, margin-top 4px
- **Label:** 13px, muted color
- **Icon Container:** 38x38px, rounded 8px, centered

#### Login Card
- **Width:** 100%, max 420px
- **Background:** White
- **Border Radius:** 16px
- **Padding:** 32px
- **Shadow:** `0 20px 40px rgba(0,0,0,0.08)`
- **Text Align:** Center

#### Table Card
- **Background:** White
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 12px
- **Padding:** 0
- **Overflow:** Auto (horizontal)
- **Title Padding:** 20px 20px 0

#### Date Bar Card
- **Layout:** Flex, align center, gap 12px
- **Background:** White
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 12px
- **Padding:** 20px

---

### Navigation

#### Sidebar
- **Width:** 240px
- **Height:** 100vh (sticky)
- **Background:** Cream `#fff8e6`
- **Border Right:** 1px solid `#f3e6c3`
- **Padding:** 24px 16px
- **Layout:** Flex column

#### Brand
- **Font Size:** 20px
- **Font Weight:** 700
- **Color:** Brand Text `#7c3f12`
- **Margin Bottom:** 28px
- **Padding Left:** 8px
- **Icon:** ☕

#### Nav Item
- **Layout:** Flex, gap 10px, center
- **Background:** None
- **Border:** 2px solid transparent
- **Border Radius:** 10px
- **Padding:** 10px 12px
- **Text Align:** Left
- **Color:** Ink `#1f2937`
- **Font Size:** 14px
- **Icon:** Emoji before text
- **Hover:** Sand background
- **Active:** Sand background

#### User Info (Whoami)
- **Border Top:** 1px solid `#f0e2bc`
- **Padding Top:** 16px
- **Layout:** Flex column, gap 2px
- **Font Size:** 12px
- **Name:** 14px, medium weight
- **Role:** Brand color, capitalize, 11px

---

### Product Card

#### Layout
- **Grid:** Auto-fill, min 170px, gap 14px
- **Background:** White
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 12px
- **Padding:** 14px
- **Text Align:** Left
- **Position:** Relative

#### Elements
- **Category Tag:** Absolute, top 14px, right 12px, Sand background, Brand Text color, rounded 999px, 11px, padding 3px 9px
- **Emoji:** 34px
- **Name:** 14px, medium, margin-top 8px
- **Price:** Brand color, bold, margin-top 2px
- **Stock:** 11px, muted, margin-top 4px
- **Low Stock:** Red color

#### States
- **Hover:** Translate Y -2px, shadow `0 6px 16px rgba(0,0,0,0.08)`
- **Disabled (Out of Stock):** Opacity 0.5, cursor not-allowed

---

### Cart

#### Cart Card
- **Position:** Sticky, top 24px
- **Background:** White
- **Border:** 1px solid Line `#e5e7eb`
- **Border Radius:** 12px
- **Padding:** 20px

#### Cart Pill
- **Background:** Sand `#fdf0cf`
- **Color:** Brand Text `#7c3f12`
- **Padding:** 8px 14px
- **Border Radius:** 10px
- **Font Weight:** 600
- **Font Size:** 14px

#### Cart Line
- **Layout:** Flex, space-between, gap 8px
- **Background:** Background `#f8fafc`
- **Border Radius:** 10px
- **Padding:** 10px 12px
- **Margin Bottom:** 8px

#### Cart Empty State
- **Text Align:** Center
- **Color:** Muted
- **Padding:** 30px 0
- **Icon:** 40px, opacity 0.5

#### Total Row
- **Layout:** Flex, space-between, center
- **Border Top:** 1px solid Line
- **Margin Top:** 12px
- **Padding Top:** 14px
- **Font Size:** 18px
- **Color:** Muted
- **Amount:** Brand Text, 22px, bold

---

### Tables

#### Standard Table
- **Width:** 100%
- **Border Collapse:** Collapse
- **Font Size:** 14px

#### Table Header
- **Text Align:** Left
- **Color:** Muted
- **Font Weight:** 500
- **Font Size:** 13px
- **Padding:** 12px 16px
- **Background:** `#fafbfc`

#### Table Cell
- **Padding:** 12px 16px
- **Border Top:** 1px solid `#f1f5f9`

#### Price Cell
- **Color:** Green `#16a34a`
- **Font Weight:** 600

#### Pill
- **Background:** `#f1f5f9`
- **Border Radius:** 999px
- **Padding:** 2px 10px
- **Font Size:** 12px

#### Stock Status Dot
- **Display:** Inline-block
- **Width:** 9px
- **Height:** 9px
- **Border Radius:** 50%
- **Margin Right:** 6px
- **Good:** `#22c55e`
- **Low:** `#f59e0b`
- **Out:** Red `#dc2626`

---

### Alerts

#### Alert Box
- **Background:** `#fff4e5`
- **Border:** 1px solid `#fcd9a8`
- **Color:** `#8a4b12`
- **Padding:** 12px 16px
- **Border Radius:** 10px
- **Margin Bottom:** 20px
- **Font Size:** 14px
- **Icon:** ⚠

#### Error Message
- **Color:** Red `#dc2626`
- **Font Size:** 13px
- **Margin:** 10px 0 0

---

### Modal

#### Modal Overlay
- **Position:** Fixed, inset 0
- **Background:** `rgba(15,23,42,0.5)`
- **Layout:** Grid, place-items center
- **Z-Index:** 20
- **Padding:** 16px

#### Modal Box
- **Background:** White
- **Border Radius:** 16px
- **Padding:** 32px
- **Width:** 100%, max 380px
- **Text Align:** Center

#### Modal Elements
- **Success Icon:** 48px, Green
- **Title:** 22px, margin 8px 0 4px
- **Label:** Muted, 13px, margin-top 16px
- **Amount:** Green, 28px, bold
- **Button:** Primary, margin-top 22px

---

### Toast Notification

#### Toast
- **Position:** Fixed, bottom 24px, left 50%, translate X -50%
- **Background:** `#111827`
- **Color:** White
- **Padding:** 12px 20px
- **Border Radius:** 10px
- **Z-Index:** 30
- **Font Size:** 14px

#### Error Toast
- **Background:** Red `#dc2626`

---

### Demo Box

#### Demo Credentials Box
- **Background:** `#fffbe8`
- **Border:** 1px solid `#fcefbf`
- **Color:** `#8a4b12`
- **Padding:** 12px
- **Border Radius:** 8px
- **Font Size:** 12px
- **Margin Top:** 20px
- **Text Align:** Left

---

### Logo Badge

#### Logo
- **Width:** 56px
- **Height:** 56px
- **Background:** Brand `#c97b2e`
- **Border Radius:** 14px
- **Layout:** Grid, place-items center
- **Font Size:** 28px
- **Margin:** 0 auto 12px

---

### Charts

#### Chart Container
- **Position:** Relative
- **Height:** 260px

---

## Screen Specifications

### 1. Login Screen

#### Layout
- **Background:** Linear gradient (135deg, `#fffaf0`, `#fdebd0`)
- **Container:** Grid, place-items center, min-height 100vh, padding 16px
- **Card:** Centered, max-width 420px

#### Elements (Top to Bottom)
1. **Logo Badge:** 56x56px, Brand background, centered, emoji ☕
2. **Title:** "Cafe POS", 26px, centered
3. **Subtitle:** "Coffee Shop Management System", 14px, muted, centered, margin 4px 0 20px
4. **Username Label:** 14px, medium, margin 14px 0 6px
5. **Username Input:** Full width, placeholder "Enter your username", autofocus
6. **Password Label:** 14px, medium, margin 14px 0 6px
7. **Password Input:** Full width, type password, placeholder "Enter your password"
8. **Error Message:** Hidden by default, red, 13px, margin 10px 0 0
9. **Login Button:** Primary, block, "Login →", margin-top 18px
10. **Demo Box:** Margin-top 20px, credentials for Admin and Cashier

#### States
- **Loading:** Button disabled
- **Error:** Error message visible, shake animation
- **Success:** Redirect to dashboard

---

### 2. Main App Shell

#### Layout
- **Container:** Flex, min-height 100vh
- **Sidebar:** Left, 240px, sticky
- **Page Content:** Right, flex-1

#### Sidebar Elements (Top to Bottom)
1. **Brand:** "☕ Cafe POS", 20px, bold, margin-bottom 28px
2. **Navigation:** Flex column, gap 4px, flex-1
   - Point of Sale (☕)
   - Dashboard (▦)
   - Inventory (📦)
   - Reports (📊) - Admin only
3. **User Info:** Border-top, padding-top 16px
   - "Logged in as" (small)
   - User Name (strong)
   - Role (badge)
   - Logout button (link style)

#### Page Content
- **Padding:** 24px 24px 48px
- **Header:** Page title + action buttons

---

### 3. Point of Sale Screen

#### Layout
- **Grid:** 2 columns, gap 20px
- **Left:** Product grid (flex-1)
- **Right:** Cart (340px, sticky)

#### Left Column Elements
1. **Page Header:** "Point of Sale" + Cart pill (🛒 X items)
2. **Category Chips:** Flex, gap 8px, wrap
   - All (default active)
   - Coffee
   - Cold Drinks
   - Food
   - Tea
3. **Product Grid:** Auto-fill, min 170px, gap 14px
   - Product cards with emoji, name, price, stock

#### Right Column (Cart)
1. **Header:** "🛒 Current Order"
2. **Cart Items:** List of cart lines
3. **Empty State:** Cart icon + "Cart is empty"
4. **Total Row:** "Total:" + Amount
5. **Payment Method:** 2 buttons (Cash, Card)
6. **Complete Button:** Primary, block

#### Cart Line Structure
- Product name + price
- Quantity controls (−, qty, +, delete)

---

### 4. Dashboard Screen

#### Layout
- **Alert:** Low stock warning (if applicable)
- **Stats Grid:** 4 columns
- **Charts Grid:** 2 columns
- **Recent Orders Table:** Full width

#### Elements
1. **Page Header:** "Dashboard"
2. **Alert:** "⚠ Low stock: Product names" (if low stock items exist)
3. **Stats Grid (4 columns):**
   - Today's Revenue (Green, $ icon)
   - Today's Orders (Blue, 🛒 icon)
   - Average Order (Purple, ↗ icon)
   - Total Products (Brand, 📦 icon)
4. **Charts Grid (2 columns):**
   - Sales by Category (Pie chart)
   - Top Selling Products (Bar chart)
5. **Recent Orders Table:**
   - Columns: Order ID, Customer, Total, Payment, Time
   - Up to 8 recent orders

---

### 5. Inventory Screen

#### Layout
- **Page Header:** "Inventory Management"
- **Search Bar:** Full width
- **Table:** Full width, scrollable

#### Elements
1. **Page Header:** "Inventory Management"
2. **Search Input:** "🔍 Search products..."
3. **Table:**
   - Columns: Product, Category, Stock Level, Quantity, Price, Actions (Admin only)
   - Stock Level: Dot (good/low/out) + label
   - Actions: "+ Add 10" button (Admin only)

#### States
- **Filter:** Real-time search by name or category
- **Restock:** Button adds 10 units, updates table

---

### 6. Reports Screen (Admin Only)

#### Layout
- **Page Header:** Title + Export button
- **Date Bar:** Period selector + Date input
- **Stats Grid:** 4 columns
- **Charts Grid:** 2 columns
- **Profit Analysis Table:** Full width
- **Category Reports Table:** Full width

#### Elements
1. **Page Header:** "Reports & Analytics" + "⬇ Export Report" button
2. **Date Bar:**
   - Period dropdown (Daily/Monthly/Yearly)
   - Date/Month/Year picker (changes based on period)
3. **Stats Grid (4 columns):**
   - Total Revenue (Green)
   - Total Cost (Red)
   - Profit (Green)
   - Total Orders (Blue)
4. **Charts Grid (2 columns):**
   - Revenue Trend (Line chart)
   - Profit by Product (Bar chart)
5. **Profit Analysis Table:**
   - Columns: Product, Category, Units, Revenue, Cost, Profit, Margin, Advice
   - Advice color-coded (green=Promote, red=Review)
6. **Category Reports Table:**
   - Columns: Category, Revenue, Profit

#### Date Picker Types
- **Daily:** Date picker (YYYY-MM-DD)
- **Monthly:** Month picker (YYYY-MM)
- **Yearly:** Year picker (YYYY)

---

## User Flows

### 1. Login Flow
```
1. User opens app
2. Sees login screen
3. Enters username and password
4. Clicks "Login →"
5. System validates credentials
6. If valid → Redirect to Dashboard/POS
7. If invalid → Show error message
```

### 2. POS Flow
```
1. User navigates to Point of Sale
2. Selects category filter (optional)
3. Clicks product to add to cart
4. Adjusts quantity (+/- buttons)
5. Selects payment method (Cash/Card)
6. Clicks "Complete Order"
7. Modal appears with order confirmation
8. Click "New Order" to reset
```

### 3. Dashboard Flow
```
1. User navigates to Dashboard
2. Views today's stats (revenue, orders, etc.)
3. Views sales by category chart
4. Views top products chart
5. Views recent orders table
6. Checks low stock alert (if any)
```

### 4. Inventory Flow (Admin)
```
1. Admin navigates to Inventory
2. Views all products with stock levels
3. Searches for specific product (optional)
4. Clicks "+ Add 10" to restock
5. Stock updates immediately
```

### 5. Reports Flow (Admin)
```
1. Admin navigates to Reports
2. Selects period type (Daily/Monthly/Yearly)
3. Selects date/month/year
4. Views stats and charts
5. Views profit analysis table
6. Views category reports
7. Clicks "Export Report" to download
```

### 6. Logout Flow
```
1. User clicks "Logout" in sidebar
2. System clears session
3. Redirects to login screen
```

---

## Interactive States

### Button States
- **Default:** Normal appearance
- **Hover:** Background darkens (brand-dark)
- **Active:** Click feedback
- **Disabled:** Opacity 0.5, cursor not-allowed
- **Loading:** Spinner or loading text

### Input States
- **Default:** Border Line color
- **Focus:** 2px solid Brand outline, border transparent
- **Error:** Red border (optional)
- **Disabled:** Gray background

### Card States
- **Default:** Normal shadow
- **Hover:** Enhanced shadow (product cards)
- **Disabled:** Opacity 0.5 (out of stock)

### Navigation States
- **Default:** Transparent border
- **Hover:** Sand background
- **Active:** Sand background + visual indicator

### Payment Button States
- **Default:** Light gray background
- **Selected:** Green background, white text

### Table Row States
- **Default:** Normal appearance
- **Hover:** Light background tint (optional)

---

## Responsive Design

### Desktop (> 1000px)
- **Stats Grid:** 4 columns
- **Charts Grid:** 2 columns
- **POS:** 2 columns (products + cart)
- **Sidebar:** Fixed, 240px

### Tablet (700px - 1000px)
- **Stats Grid:** 2 columns
- **Charts Grid:** 1 column
- **POS:** 1 column (cart below products)
- **Sidebar:** Fixed, 240px

### Mobile (< 700px)
- **App Layout:** Column (sidebar on top)
- **Sidebar:** Full width, height auto, padding 12px
- **Navigation:** Row, wrap
- **Brand:** Margin-bottom 10px
- **User Info:** Name/role hidden
- **Page Padding:** 16px
- **Stats Grid:** 2 columns or 1 column depending on space

---

## Iconography

### Emojis Used
- **Logo:** ☕
- **Point of Sale:** ☕
- **Dashboard:** ▦
- **Inventory:** 📦
- **Reports:** 📊
- **Cart:** 🛒
- **Orders:** 🛒
- **Logout:** ⎋
- **Search:** 🔍
- **Alert:** ⚠
- **Delete:** 🗑
- **Success:** ✔

### Product Emojis
- **Coffee:** ☕
- **Milk:** 🥛
- **Chocolate:** 🍫
- **Ice:** 🧊
- **Drink:** 🥤
- **Lemon:** 🍋
- **Croissant:** 🥐
- **Muffin:** 🧁
- **Sandwich:** 🥪
- **Cookie:** 🍪
- **Tea:** 🍵
- **Teapot:** 🫖
- **Leaf:** 🍃
- **Bubble Tea:** 🧋

---

## Accessibility

### Color Contrast
- Ensure text meets WCAG AA standards
- Muted text should still be readable
- Error messages should be high contrast

### Focus States
- All interactive elements should have visible focus states
- Use 2px outline for keyboard navigation

### ARIA Labels
- Buttons should have descriptive labels
- Form inputs should have associated labels
- Modal should have aria-modal attribute

### Keyboard Navigation
- Tab order should be logical
- Enter/Space to activate buttons
- Escape to close modals

---

## Notes for Figma Implementation

1. **Create Components First:**
   - Build the design system (colors, typography, spacing)
   - Create reusable components (buttons, cards, inputs)
   - Use auto-layout for responsive components

2. **Use Variables:**
   - Color variables for easy theming
   - Spacing variables for consistency
   - Typography scale

3. **Create Screens:**
   - Start with login screen
   - Build app shell (sidebar + content)
   - Create each page as a separate frame
   - Use components for consistency

4. **Interactive Elements:**
   - Create hover states for all buttons
   - Create focus states for inputs
   - Create disabled states
   - Create loading states

5. **Responsive Design:**
   - Use constraints for responsive layouts
   - Create variants for different screen sizes
   - Test on mobile, tablet, desktop

6. **Export Assets:**
   - Export icons as SVG
   - Export charts as PNG/SVG
   - Ensure correct scale for retina displays

---

## Additional Resources

### Files Reference
- **Styles:** `/static/style.css`
- **HTML Structure:** `/static/index.html`
- **JavaScript Logic:** `/static/app.js`
- **Backend API:** `/app.py`

### Key Features
- JWT Authentication
- Role-based access (Admin, Cashier)
- Real-time inventory tracking
- Chart.js for data visualization
- Responsive design
- Export functionality

---

**End of UI Design Specification**
