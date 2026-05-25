# Notice

This file records the current license and attribution posture for DeskPulse.
It is intentionally separate from the setup-focused README.

## Repository License Status

DeskPulse currently has no top-level open-source license for the combined
codebase.

Do not assume MIT, Apache, GPL, or other open-source permissions for the full
repository. The upstream repository did not include an explicit LICENSE file at
the divergence point, and this fork includes upstream-derived code and assets.

This repository remains a public GitHub fork, which preserves the visible
relationship to the upstream project. GitHub's public-repository terms allow
viewing and forking through GitHub, but that is not the same as a general
open-source license for reuse, distribution, or relicensing outside those
platform mechanics.

References:

- GitHub Docs, licensing a repository: https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- GitHub Terms of Service: https://docs.github.com/terms-of-service

## Upstream Attribution

DeskPulse started as a fork of:

https://github.com/HermannBjorgvin/Clawdmeter

The fork diverged from upstream commit:

```text
6b5314ef28898896f91f4a9bd6784da8746dbc49
```

See [UPSTREAM.md](UPSTREAM.md) for the project direction and divergence notes.

## Third-Party Assets And Components

- Clawd pixel animations: sourced from https://claudepix.vercel.app and
  credited in the firmware UI to `@amaanbuilds`. Reuse terms were not clarified
  in this repository; verify before redistributing or reusing separately.
- Anthropic/Claude styling and assets: this repository includes Anthropic brand
  styling, the Clawd mascot artwork, and proprietary font assets such as Styrene
  B and Tiempos Text. Do not assume these assets are open source.
- Lucide icons: Bluetooth and battery icons are derived from Lucide assets.
  Lucide is published under the ISC license, with some icons derived from
  Feather under MIT terms. Keep Lucide and Feather attribution if those assets
  are reused separately. See https://lucide.dev and
  https://github.com/lucide-icons/lucide/blob/main/LICENSE.
- DejaVu Sans Mono: bundled as `assets/DejaVuSansMono.ttf` and compiled into
  firmware bitmap fonts. Verify the upstream DejaVu font license before
  redistributing the font asset separately.

## Future Licensing Path

A clean open-source license can be added only after the rights for the combined
codebase and bundled assets are clarified. Until then, keep this NOTICE file and
avoid presenting the repository as fully open source.
