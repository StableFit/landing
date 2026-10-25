// Renders a messenger share pill PNG for lifecycle emails: brand colour, white
// icon (simple-icons, CC0) and white Urbanist 17/600 name, 228x44 @ scale
// (two in a row inside the 464 pt card). Pixels, so Gmail dark mode cannot
// recolour the label.
//   node render-share-button.mjs telegram ../../assets/email/buttons/share-telegram@3x.png 3
import sharp from "sharp";
import * as si from "simple-icons";
const [kind, out, scaleArg] = process.argv.slice(2);
const scale = Number(scaleArg ?? 3);
// Slightly darker than the logo colours so the white label reads well.
const BRANDS = {
  telegram: { icon: si.siTelegram, color: "#229ED9", label: "Telegram" },
  whatsapp: { icon: si.siWhatsapp, color: "#1DAA61", label: "WhatsApp" },
};
const b = BRANDS[kind];
if (!b) throw new Error(`unknown kind ${kind}`);
const W = 228, H = 44, ICON = 20, GAP = 8;
// Label width estimate for centring icon + text as one group (Urbanist 17/600).
const textW = b.label.length * 9.4;
const x0 = (W - (ICON + GAP + textW)) / 2;
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<rect x="0" y="0" width="${W}" height="${H}" rx="22" ry="22" fill="${b.color}"/>
<g transform="translate(${x0} ${(H - ICON) / 2}) scale(${ICON / 24})"><path d="${b.icon.path}" fill="#FFFFFF"/></g>
<text x="${x0 + ICON + GAP}" y="${H / 2}" dominant-baseline="central" font-family="Urbanist" font-weight="600" font-size="17" fill="#FFFFFF">${b.label}</text>
</svg>`;
await sharp(Buffer.from(svg), { density: 72 * scale }).png().toFile(out);
const m = await sharp(out).metadata(); console.log("ok", out, m.width, m.height);
