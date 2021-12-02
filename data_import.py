import numpy as np
from sportsreference.nfl.teams import Teams

teams = Teams(2018)
detroit = teams('DET')
test = [p.height for p in detroit.roster.players]