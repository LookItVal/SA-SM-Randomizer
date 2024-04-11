import numpy as np
import pandas as pd
import datetime

DEFAULT_COUNT = 10

def main():
  print('SELECTING MESSAGE FROM THE POOL')
  message = getMessage()
  print('MESSAGE SELECTED: ', message)
  response = input('Would you like to use this message? (y/n): ')
  while len(response) == 0 or (response[0] != 'y' and response[0] != 'n'):
    print('Invalid response. Please enter y or n.')
    response = input('Would you like to use this message? (y/n): ')
  if response[0] == 'y':
    setActiveMessage(message)
    print('MESSAGE SET')
  else:
    main()
    return
  
def getMessage():
  df = pd.read_csv('data/messages.csv')
  df = df[df['Active'] == False]
  messages = []
  for index, row in df.iterrows():
    message = np.full(row['Days Left'], row['Message'])
    if index == 0:
      messages = message
    else:
      messages = np.concatenate((messages, message))
  return np.random.choice(messages)

def getActiveMessage():
  df = pd.read_csv('data/messages.csv')
  df = df[df['Active'] == True]
  if df.empty:
    return None
  if df.shape[0] > 1:
    raise ValueError('Multiple active messages found')
  return df.values[0]

def setActiveMessage(message):
  df = pd.read_csv('data/messages.csv')
  active = getActiveMessage()
  if active is not None:
    currentDate = datetime.datetime.now().date()
    activeDate = datetime.datetime.strptime(active[3], '%Y-%m-%d').date()
    daysDifference = (activeDate - currentDate).days
    newCount = active[1] + daysDifference
    while newCount <= 0:
      newCount += DEFAULT_COUNT
    df.loc[df['Message'] == active[0], 'Days Left'] = newCount
    df.loc[df['Message'] == active[0], 'Active'] = False
    df.loc[df['Message'] == active[0], 'Date Set'] = ''
  df.loc[df['Message'] == message, 'Date Set'] = str(currentDate)
  df.loc[df['Message'] == message, 'Active'] = True
  df.to_csv('data/messages.csv', index=False)


if __name__ == '__main__':
  main()

