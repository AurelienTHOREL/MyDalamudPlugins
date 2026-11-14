# MyDalamudPlugins

A custom Dalamud plugin repository.

## Add the repository

1. In game, open `/xlsettings` and go to **Experimental**.
2. Under **Custom Plugin Repositories**, add:

   ```
   https://raw.githubusercontent.com/AurelienTHOREL/MyDalamudPlugins/master/pluginmaster.json
   ```

3. Tick **Enabled**, then save.
4. Open `/xlplugins` and install the plugins below.

## Plugins

| Plugin | What it does | Requires |
|--------|--------------|----------|
| **FightSolver** | Reads the current boss fight from BossMod Reborn and draws where each party member should stand. | [BossMod Reborn](https://github.com/FFXIV-CombatReborn/BossmodReborn) |

FightSolver is built against a specific BossMod Reborn release. If BossMod Reborn has updated
since the FightSolver build you installed, FightSolver shows a mismatch alert in chat until a
new build is published here.

## How this repository is updated

- Each plugin lives in `plugins/<InternalName>/latest.zip`, with its `<InternalName>.json`
  manifest at the root of the zip.
- FightSolver's own CI commits a new `latest.zip` here for every release tag.
- Every push to `master` runs `.github/workflows/regenerate.yml`, which rebuilds
  `pluginmaster.json` from the zips with `generate_pluginmaster.py` and commits it.
