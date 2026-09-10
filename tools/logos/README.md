# ATLAS carousel card standard — v0.2.0 Test Build 5

The active system carousel card contract is:

- **480 × 360 pixels**
- **actual PNG encoding** for every file in `_inc/systems/logos-atlas/`
- full-canvas card occupancy; transparent rounded corners are fine
- no additional theme-side scaling property inside `systemcarousel`

Test Build 4 normalized every card to this geometry. Test Build 5 keeps that contract and converts the newer manually replaced cards from 480×320/mixed PNG-WebP content into true 480×360 PNGs.

Audit the active directory with:

```bash
python3 tools/logos/atlas-logo-audit.py
```

`atlas-logo-normalize.py` remains available for manually normalizing a directory of replacement cards. It crops meaningful alpha content and stretches the result to the 480×360 carousel canvas, matching the Test Build 4 normalization behavior.

Experimental alternatives live in `_inc/systems/logos-atlas-alt/` and are not referenced by the active theme.
