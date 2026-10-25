# Email button images

Gmail (Android / iOS) inverts live text in dark mode, so the CTA buttons in
lifecycle emails are PNGs: gradient #5037C8 -> #825BFC, white Urbanist 17/600,
464x44 pt, rendered at 3x. One file per label, named by slug (see
`supabase/functions/_shared/email/templates.ts`, `buttonImage(...)`).

    cd scripts/email
    npm i sharp
    FONTCONFIG_FILE=$PWD/fonts.conf node render-button.mjs "Відкрити StableFit Pro" ../../assets/email/buttons/open-pro-uk@3x.png 3

Also: `assets/email/icon@2x.png` / `icon@3x.png` (logo mark only; the word
«StableFit» is live text so mail clients recolour it with the theme).
