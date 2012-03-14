import re
import math

cats = ['politics', 'baseball', 'space']

# feature extraction
def getwords(doc):
  splitter=re.compile('\\W*')
  #print doc
  # Split the words by non-alpha characters
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
  # Return the unique set of words only
  return dict([(w,1) for w in words])

# Hold the list of category counts per feature. e.g. {'news' : {'politics' : '2', 'baseball' : 3, 'space' : 7}}
featuresCats={}

# Counts of documents in each category, needed to compute probabilities
catCount={}
    
# Helper Fuctions

# Everytime we see a feature belong to a specific category, increase the counter
def incrementFeature(feature, category):
    featuresCats.setdefault(feature, {})
    featuresCats[feature].setdefault(category, 0)
    featuresCats[feature][category] += 1

# Everytime we see an example from a specific category, increase that counter.
def incrementCategory(category):
    catCount.setdefault(category, 0)
    catCount[category] += 1

# Return the number of times a specific feature occured in a specific category
def featureCount(feature, category):
    if feature in featuresCats and category in featuresCats[feature]:
        return float(featuresCats[feature][category])
    return 0.0

# return the number of examples we have in a specific category.
def categoryCount(category):
    if category in catCount:
        return float(catCount[category])
    return 0.0

# How many total examples did we see?
def totalCount():
    return sum(catCount.values())

# What are the categories we've seen?
def categories():
    return catCount.keys()
 

# 


# Import a single document into the trainer 
def train(item,category):
    # Split the documen into its features
    features=getwords(item)
    
    # Increment the count for every feature with this category
    for f in features:
        incrementFeature(f,category)
    
    # Increment the count for this category
    incrementCategory(category)

# Compute the (conditional) probability a single feature came from a single category 
def featureProb(feature, category):
    if categoryCount(category)==0: return 0
    
    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    return featureCount(feature,category)/categoryCount(category)


# Don't be so drastic. Smooth out the probabilites using a reasonable assumption.
# Then take the average between our assumption and the conditional probability
def weightedProb(feature,category,weight=1.0,assumedProb=0.5):
    # Calculate current probability
    basicProb=featureProb(feature,category)

    # Count the number of times this feature has appeared in
    # all categories
    totals=sum([featureCount(feature,cat) for cat in categories()])

    # Calculate the weighted average
    newProb=((weight*assumedProb)+(totals*basicProb))/(weight+totals)
    return newProb




# Compute the (conditional) probability that an entire document came from a given category
def docprob(item,category):
    features=getwords(item)   

    # Multiply the probabilities of all the features together
    # add up the logs instead!
    # p = 1
    total = 0
    for f in features: 
        #p*=weightedProb(f,category)
        total += math.log(weightedProb(f, category))
    
    return total

# Compute the 'probability'.  P(doc | category) * P(category)
# Remember this is not quite the probability P(category | doc), but it will work for us.
def prob(item,category):
    catprob = categoryCount(category) / totalCount()
    conditional = docprob(item,category)
    return conditional + math.log(catprob)

# We'll only use this section if we have time to explain.
thresholds = {}  
def setthreshold(category,t):
    thresholds[category]=t
    
def getthreshold(category):
    if category not in thresholds: return 1.0
    return thresholds[category]
  
# CLASSIFY!
def classify(item,default=None):
    probs={}
    # Find the category with the highest probability
    max=-10000000
    for category in categories():
      probs[category]=prob(item,category)
      if probs[category] > max: 
        max = probs[category]
        best = category
    # Make sure the probability exceeds threshold*next best.
    # Only explain this if we have time!
    print probs 
    for cat in probs:
      if cat==best: continue
      if probs[cat]*getthreshold(best)>probs[best]: return default
    
    return best


def train_news() :
    # are featureCats and catCount empty?
    featuresCats = {}
    catCount = {}
    
    training_text = open('train.txt', 'r')
    training_cat = open('train_category.txt', 'r')

    for text in training_text:
        category = training_cat.readline().strip()
        print text
        print category
        train(text,category)

def test_news() :
    
    test_text = open('test.txt', 'r')
    test_cat = open('test_category.txt', 'r')
    total = 0
    total_right = 0
    for text in test_text:
        true_category = test_cat.readline().strip()
        classified = classify(text)
        if true_category == classified:
            print "RIGHT!"
            total_right += 1
        else:
            print "WRONG", classified, true_category
        total += 1

    print "%d right, %d total = %.2f percent accurate" % (total_right, total, total_right / float(total))


