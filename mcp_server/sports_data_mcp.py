from fastmcp import FastMCP

mcp = FastMCP("LoneStarShowdownOddsServer")

# 2. Local Mock Database (Simulating exchange order-book lines for Texas A&M vs. Texas)
SPORTS_DATA = {
    "marcel_reed_passing": {
        "stat_line": "Over/Under 235.5 Passing Yards (-110)",
        "recent_games": [221, 439, 120, 180, 237],  
        "sharp_consensus_odds": "Over 235.5 (-112)",
        "season_avg": "243.7 YPG (25 TDs / 12 INTs)",
        "injury_status": "Healthy / Probable"
    },
    "texas_am_vs_texas_spread": {
        "stat_line": "Texas A&M -2.5 (-110) / Texas +2.5 (-110)",
        "sharp_consensus_odds": "Texas A&M -2.5 (-112)",
        "public_betting_pct": "68% on Texas A&M Aggies",
        "over_under_total": "54.5 Total Points"
    },
    "texas_am_team_total": {
        "stat_line": "Over/Under 27.5 Team Points (-115)",
        "sharp_consensus_odds": "Over 27.5 (-110)",
        "notes": "A&M averaging 38.1 Points Per Game overall"
    }
}

@mcp.tool()
def query_player_props(player_or_game: str) -> str:
    """
    Searches the local order book for specific market prop lines, player statistics,
    and sharp consensus odds for Texas A&M and Texas games.
    """
    key = player_or_game.lower().strip().replace(" ", "_")
    if key in SPORTS_DATA:
        data = SPORTS_DATA[key]
        return f"Market Data for {player_or_game}:\n{data}"
    
    matched_keys = [k for k in SPORTS_DATA.keys() if key in k or k in key]
    if matched_keys:
        results = [f"Market Data for {k}:\n{SPORTS_DATA[k]}" for k in matched_keys]
        return "\n\n".join(results)
        
    return f"No market data found for query '{player_or_game}'. Available keys: {list(SPORTS_DATA.keys())}"

if __name__ == "__main__":
    mcp.run()