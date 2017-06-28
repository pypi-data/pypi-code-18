from oddsman import OddsWatcher

odds_man = OddsWatcher()

todays_race_id = odds_man.get_race_ids('0625')
print(todays_race_id)

race_id = '201702010412'
odds_dict = odds_man.get_race_odds(race_id)
print(odds_dict)
