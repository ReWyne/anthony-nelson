import argparse
import random
import re
import string

def main(): #one method of allowing function declarations after your main code body
  parser = argparse.ArgumentParser(description='Generate some passwords. Example usage: "python PASS.py -b --separator _ --pCount 7"')
  parser.add_argument('--pCount', metavar='N', type=int, nargs='?', help='number of passwords generated', default=3)
  parser.add_argument('--wCount', metavar='W', type=int, nargs='?', help='number of words per password', default=5)
  parser.add_argument('-s', action='store_true', help='Uses words from your secret dictionary much more frequently. Use if you\'re confident in your secret words.')
  parser.add_argument('-b', action='store_true', help='Add the usual boring things that moronic sites require you to do with passwords. Also adds a whopping 3 bits of entropy!')
  parser.add_argument('--separator', nargs='?', default=".", type=str, help="Specify the separator used between words in your password.")
  parser.add_argument('--noreuse', action='store_true', help="Generate exactly one password for each word in your secret dictionary.")
  parser.add_argument('--randomsecrets', action='store_true', help="Generate a 5-8 character random string instead of using a word from secretwords.txt")
  parser.add_argument('--simple', action='store_true', help="Ignore non-letters in secret dictionary")
  parser.add_argument('--lol', action='store_true', help="Allow all characters in public dictionary")

  args = parser.parse_args()

  #if you want to change the names of the dictionaries the program reads, do so here
  with open("dict.txt", "r") as inf:
    dWords = inf.readlines()
  with open("secretwords.txt", "r") as inf:
    sWords = inf.readlines()

  #if you want to put conditions on which of your public dictionary words are used, do so here
  maxLen = 8
  minLen = 3

  #format the lines read from our dictionaries nicely, cutting out whitespace, commas, etc.
  maxLen += 1
  if args.lol:
    dWords = [item.strip() for item in dWords if len(item) > minLen and len(item) <= maxLen]
  else:
    dWords = [re.sub(r'[^a-zA-Z]+','', item) for item in dWords if len(item) > minLen and len(item) <= maxLen]

  if args.simple:
    sWords = [re.sub(r'[^a-zA-Z]+','', item) for item in sWords if len(item) > 1]
  else:
    sWords = [item.strip() for item in sWords if len(item) > 1]

  #lightly season dict words with secret words, for mind games
  dWords.extend(sWords)

  #select our words for the password
  with open("PASSWORDS.txt", "w") as outf:
    if(args.noreuse):
      pCount = len(sWords)
    else:
      pCount = args.pCount
    secRand = random.SystemRandom()
    for i in range(0,pCount):
      words = []
      if(args.s):
        num = secRand.randint(1,args.wCount) #number of secret words
      else:
        num = 1
      for j in range(0,num):
        if(args.randomsecrets):
          words.append(randomString(secRand))
        elif(args.noreuse):
          words.append(sWords[i])
        else:
          words.append(secRand.choice(sWords))
      for j in range(0,args.wCount-num):
        words.append(secRand.choice(dWords))
      secRand.shuffle(words)

      #format our password to specifications
      output = (args.separator.join(words))
      if(args.b):
        output = output[0].upper() + output[1:] + "->" + str(secRand.randint(0,9))
      outf.write(output+'\n')
      print(output)

def randomString(gen = random.SystemRandom()):
  numChars = gen.randint(5,8)
  charset = string.ascii_letters + "0123456789" + "!@#$%^&*?-_+="
  output = ""
  for i in range(0,numChars-2):
    output += gen.choice(charset)
  #guarantee that we have not all lowercase letters
  output += gen.choice(string.ascii_uppercase)
  output += gen.choice("0123456789!@#$%^&*?-_+=")
  #and mix well
  ''.join(gen.sample(output,len(output)))
  return output

main()
