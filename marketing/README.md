# VideoEditor-MCP Standalone Marketing Suite

This directory contains the self-contained marketing assets for VideoEditor-MCP. It is designed to be served independently of the main application.

## 📁 Directory Structure
- `index.html`: Main landing page (Tailwind CSS + Lucide Icons).
- `ab-engine.js`: A/B testing logic for headlines and CTAs.
- `styles.css`: Custom styling and animations.
- `*.md`: Source copy and campaign strategy files.

## 🚀 How to Use
1. **Open in Browser**: Simply open `index.html` in any modern web browser.
2. **Serve with HTTP**: Use a simple server like `python -m http.server` or Live Server (VS Code) inside this directory.
3. **A/B Testing**:
   - The site automatically assigns a variant (A, B, or C) and saves it to `localStorage` under the key `ve_mcp_variant`.
   - To force a specific variant for testing, run this in the browser console:
     ```javascript
     localStorage.setItem('ve_mcp_variant', 'A'); // Options: 'A', 'B', 'C'
     location.reload();
     ```

## 🛠 Features
- **Responsive Design**: Mobile-first layout using Tailwind.
- **Modern UI**: Glassmorphism effects and dark mode aesthetic.
- **Dynamic Content**: A/B variants for headlines, subheadlines, and CTAs to optimize conversion.
- **Zero Build Step**: No `npm install` required. All dependencies are handled via CDN.

## 📊 Conversion Tracking
Placeholders for event tracking are included in `ab-engine.js`. See `outcomes.md` for target metrics.
