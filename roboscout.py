import csv
import copy
import numpy

def avg(l):
  s = 0.0
  for o in l:
    s = s + o
  return s / len(l)

def getData():
  data = []
  with open('scoreboard.csv', 'rU') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if row['Red Score'] != '':
        data.append(row)
  return data

def teamToMatch(data):
  teams = {}
  teamNames = ['Red 1', 'Red 2', 'Blue 1', 'Blue 2']
  for row in data:
    for n in teamNames:
      if row[n] not in teams:
        teams[row[n]] = []
      r = copy.copy(row)
      if n.find('Red') == 0:
        r['team'] = 'Red'
      else:
        r['team'] = 'Blue'
      r['position'] = n
      teams[row[n]].append(r)
  return teams

def teamToMatchScores(teams):
  ms = {}
  for team, matches in teams.iteritems():
    ms[team] = [float(r[r['team']+' Score']) for r in matches]
  return ms

def get_partners(matches):
  r = []
  for match in matches:
    num = int(match['position'][-1])
    teammate = match['team'] + ' ' + str(num%2 +1)
    r.append(match[teammate])
  return r

def mapd(f, d):
  """
    Variant of map() that applies a function to each value
    and associates it with the same key as the original dict
  """
  r = {}
  for k, v in d.iteritems():
    r[k] = f(v)
  return r

def zipd(k, v):
  """
    Create a dictionary from two lists, one keys, one values.
  """
  return dict(zip(k, v))

def mapzip(f, l):
  """
    Similar to mapd, but f is passed the key as a part of list l
    instead of a dictionary value
  """
  return zipd(l, map(f, l))

def display(opar, oar):
  import operator
  rank = sorted(opar.items(), key=operator.itemgetter(1))
  rank.reverse()

  for team, r in rank:
    s= team + " opar:" + str(opar[team]) + " oar:" + str(oar[team])
    print s

if __name__ == '__main__':
  m = teamToMatch(getData())
  teams = m.keys()

  tm = teamToMatchScores(m)
  tp = mapd(get_partners, m)
  ta = mapd(lambda a: avg(a), tm) # average of all the team's matches
  # the average of each team's alliance partners' averages
  # map(ta.get, tms) gets each alliance partner's average 
  tpa = mapd(lambda tms: avg(map(ta.get, tms)), tp)
 
  # Difference between a team's average and their alliance partner's
  mod = mapzip(lambda t: round(ta[t]-tpa[t],3), teams)
  # Expected output of the team given their average and modifier
  expo = mapzip(lambda t: round((ta[t]+mod[t])/2,3), teams)
  
  avgexpo = avg(expo.values())
  opar = mapd(lambda o: round(o/avgexpo,1), expo)
  
  # standard deviation of each round's expected individual output
  # based on the individual round score and the team's modifier
  stdev = mapzip(lambda t: numpy.std(
    map(lambda match: round((match + mod[t])/2, 3),tm[t])), teams)
  # Percent deviation, taking the standard deviation divided by the 
  # expected output
  pdev = mapzip(lambda t: round(stdev[t] / expo[t], 3), teams)
  # Percent deviation times OPAR gives the possible variance in OPAR
  # from round-to-round
  oar = mapzip(lambda t: round(opar[t] * pdev[t], 1), teams)
  display(opar, oar)

  
