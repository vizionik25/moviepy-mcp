/**
 * VideoEditor-MCP A/B Testing Engine
 * Manages headline and CTA variations defined in ab_content.md
 */

const VARIANTS = {
    A: {
        id: 'A',
        focus: 'ROI',
        headline: 'Cut Your Video Engineering Costs by 85% with VideoEditor-MCP',
        subheadline: 'Stop building video tools from scratch. Ship pro-grade editing features today.',
        cta: 'Deploy to Docker Now',
        ctaSub: 'Get started in 60 seconds.'
    },
    B: {
        id: 'B',
        focus: 'Time-saving',
        headline: 'Deploy a Professional Video Editing Engine in Under 5 Minutes',
        subheadline: 'Zero FFmpeg struggle. Just one API call to trim, crop, and composite.',
        cta: 'Build My Video App',
        ctaSub: 'Free and Open Source.'
    },
    C: {
        id: 'C',
        focus: 'Risk-reversal',
        headline: 'The Production-Ready Video API That Never Fails Your AI Agents',
        subheadline: 'Battle-tested MoviePy v2.2 stability wrapped in a high-performance FastAPI layer.',
        cta: 'Claim Your Repository',
        ctaSub: 'Stop wasting engineering hours today.'
    }
};

function getActiveVariant() {
    const saved = localStorage.getItem('ve_mcp_variant');
    if (saved && VARIANTS[saved]) return VARIANTS[saved];

    const keys = Object.keys(VARIANTS);
    const random = keys[Math.floor(Math.random() * keys.length)];
    localStorage.setItem('ve_mcp_variant', random);
    return VARIANTS[random];
}

function applyVariant() {
    const variant = getActiveVariant();
    
    const elements = {
        'hero-headline': variant.headline,
        'hero-subheadline': variant.subheadline,
        'main-cta-text': variant.cta,
        'main-cta-subtext': variant.ctaSub
    };

    for (const [id, content] of Object.entries(elements)) {
        const el = document.getElementById(id);
        if (el) {
            el.innerText = content;
        }
    }

    console.log(`[AB TEST] Variant ${variant.id} (${variant.focus}) applied.`);
}

// Initial application
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyVariant);
} else {
    applyVariant();
}
