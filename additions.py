import pandas as pd

def main():
  response = input('What message would you like to add to the pool? ')
  if len(response) == 0:
    print('No message entered. Exiting program.')
    return
  message = response
  print('Does this look okay? (y/n): ')
  print(message)
  response = input()
  while len(response) == 0 or (response[0] != 'y' and response[0] != 'n'):
    print('Invalid response. Please enter y or n.')
    response = input('Would you like to use this message? (y/n): ')
  if response[0] == 'n':
    main()
    return
  while type(response) != int:
    response = input('How many days should this message last? (default is 30): ')
    if len(response) == 0:
      response = 30
    try:
      response = int(response)
    except ValueError:
      print('Invalid response. Please enter a number.')
  addEntry(message, response)
  print('MESSAGE ADDED')
  response = input('Would you like to add another message? (y/n): ')
  while len(response) == 0 or (response[0] != 'y' and response[0] != 'n'):
    print('Invalid response. Please enter y or n.')
    response = input('Would you like to add another message? (y/n): ')
  if response[0] == 'y':
    main()

def addEntry(message, days):
  df = pd.read_csv('data/messages.csv')
  if message in df['Message'].values:
    raise ValueError('Message already exists in the pool')
  newRow = pd.DataFrame([[message, days, False, '']], columns=df.columns)
  print(newRow)
  df = pd.concat([df,newRow])
  df.to_csv('data/messages.csv', index=False)


if __name__ == '__main__':
  main()
