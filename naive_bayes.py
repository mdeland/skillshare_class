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
    return

# Everytime we see an example from a specific category, increase that counter.
def incrementCategory(category):
    return

# Return the number of times a specific feature occured in a specific category
def featureCount(feature, category):
    return 0.0

# return the number of examples we have in a specific category.
def categoryCount(category):
    return 0.0

# How many total examples did we see?
def totalCount():
    return 0

# What are the categories we've seen?
def categories():
    return [] 


# Import a single document into the trainer 
def train(item,category):
    return

# Compute the (conditional) probability a single feature came from a single category 
def featureProb(feature, category):
    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    return 0

# Don't be so drastic. Smooth out the probabilites using a reasonable assumption.
# Then take the average between our assumption and the conditional probability
def weightedProb(feature,category,weight=1.0,assumedProb=0.5):
    return 0


# Compute the (conditional) probability that an entire document came from a given category
def docprob(item,category):
    return 0 

# Compute the 'probability'.  P(doc | category) * P(category)
# Remember this is not quite the probability P(category | doc), but it will work for us.
def prob(item,category):
    return 0

# We'll only use this section if we have time to explain.
thresholds = {}  
def setthreshold(category,t):
    return

def getthreshold(category):
    return 0

# CLASSIFY!
# given a new document, return a category
def classify(item,default=None):
    return "" 



# Train Funcion
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

# Test Function
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


