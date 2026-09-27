#!/usr/bin/env python3
"""Refresh factual site fields from Sleeper while preserving Oracle editorial copy."""
import argparse
import json
from collections import defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://api.sleeper.app/v1"
LEAGUE_ID = "1389709456710848512"
ALIASES = {
    "NachoOracle": "The Oracle", "missyannphay": "Missy",
    "HTrainALLDAY": "Heather", "maggieh15": "Maggie",
    "TripleOD": "Steph", "snailsgofigure": "Ag", "Agonizer": "Ag",
    "Aunttrish": "Trish", "GoingStreaking": "Tiff",
    "Lbradshaw": "Leslie", "aijaskye": "Aija",
}


def fetch(path):
    request = Request(BASE + path, headers={"User-Agent": "LosersLoungeSite/1.0"})
    with urlopen(request, timeout=35) as response:
        return json.load(response)


def manager_for(roster, users):
    user = users.get(str(roster.get("owner_id")), {})
    display = str(user.get("display_name") or "")
    return ALIASES.get(display, display or f"Roster {roster['roster_id']}")


def build(existing, state, rosters, users_list, matchups):
    if not isinstance(rosters, list) or not isinstance(matchups, list):
        raise ValueError("Sleeper returned unexpected roster or matchup data")
    users = {str(u.get("user_id")): u for u in users_list}
    roster_by_id = {int(r["roster_id"]): r for r in rosters}
    previous = {x["manager"]: x for x in existing.get("standings", [])}
    standings = []
    for roster in rosters:
        settings = roster.get("settings") or {}
        manager = manager_for(roster, users)
        old = previous.get(manager, {})
        wins = int(settings.get("wins") or 0)
        losses = int(settings.get("losses") or 0)
        ties = int(settings.get("ties") or 0)
        points_for = float(settings.get("fpts") or 0) + float(settings.get("fpts_decimal") or 0) / 100
        team = (users.get(str(roster.get("owner_id")), {}).get("metadata") or {}).get("team_name")
        standings.append({
            "manager": manager, "team": team or old.get("team") or manager,
            "record": f"{wins}-{losses}" + (f"-{ties}" if ties else ""),
            "note": old.get("note", "") if old.get("record") == f"{wins}-{losses}" + (f"-{ties}" if ties else "") else "",
            "_wins": wins, "_ties": ties,
            "_points_for": points_for,
        })
    standings.sort(key=lambda x: (-x["_wins"], -x["_ties"], -x["_points_for"], x["manager"]))
    for index, item in enumerate(standings, 1):
        item["rank"] = index
        for key in ("_wins", "_ties", "_points_for"):
            del item[key]

    groups = defaultdict(list)
    for item in matchups:
        groups[item.get("matchup_id")].append(item)
    pairs = []
    for group in groups.values():
        if len(group) != 2:
            continue  # A bye or incomplete matchup should not fabricate an opponent.
        a, b = sorted(group, key=lambda x: int(x["roster_id"]))
        ar = roster_by_id.get(int(a["roster_id"]))
        br = roster_by_id.get(int(b["roster_id"]))
        if not ar or not br:
            continue
        pairs.append({
            "a": manager_for(ar, users), "a_score": round(float(a.get("points") or 0), 2),
            "b": manager_for(br, users), "b_score": round(float(b.get("points") or 0), 2),
        })
    pairs.sort(key=lambda x: (x["a"], x["b"]))
    if len(rosters) != 10 or len(pairs) != 5:
        raise ValueError(f"Expected 10 teams and 5 matchups; got {len(rosters)} and {len(pairs)}")

    week = int(state.get("week") or 0)
    if not 1 <= week <= 18:
        raise ValueError(f"Sleeper returned unexpected NFL week: {week}")
    result = dict(existing)
    result["standings"] = standings
    result["live"] = {"label": f"Week {week} Snapshot", "matchups": pairs}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="league_data.json")
    parser.add_argument("--league-id", default=LEAGUE_ID)
    args = parser.parse_args()
    path = Path(args.data)
    existing = json.loads(path.read_text(encoding="utf-8"))
    state = fetch("/state/nfl")
    week = int(state.get("week") or 0)
    rosters = fetch(f"/league/{args.league_id}/rosters")
    users = fetch(f"/league/{args.league_id}/users")
    matchups = fetch(f"/league/{args.league_id}/matchups/{week}")
    updated = build(existing, state, rosters, users, matchups)
    path.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated Week {week}: {len(updated['standings'])} teams, {len(updated['live']['matchups'])} matchups")


if __name__ == "__main__":
    main()
