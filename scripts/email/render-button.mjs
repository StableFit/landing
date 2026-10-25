// Renders a pill button PNG: gradient #5037C8 -> #825BFC, white Urbanist 17/600, 464x44 @ scale.
import sharp from "sharp";
const [label, out, scaleArg] = process.argv.slice(2);
const scale = Number(scaleArg ?? 2);
const W = 464, H = 44;
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5037C8"/><stop offset="1" stop-color="#825BFC"/></linearGradient></defs>
<rect x="0" y="0" width="${W}" height="${H}" rx="22" ry="22" fill="url(#g)"/>
<text x="${W/2}" y="${H/2}" text-anchor="middle" dominant-baseline="central" font-family="Urbanist" font-weight="600" font-size="17" fill="#FFFFFF">${esc(label)}</text>
</svg>`;
await sharp(Buffer.from(svg), { density: 72 * scale }).png().toFile(out);
const m = await sharp(out).metadata(); console.log("ok", out, m.width, m.height);
