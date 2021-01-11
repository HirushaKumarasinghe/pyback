
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from xlwt import Workbook
# from pywsd.lesk import simple_lesk

import re
import nltk
import xlrd
import numpy as np


# Assigning variables
loc = "Survey1.xlsx"
numCol = 5
commentCol = 6
saveFileName = "resultsQ.xls"
wb = Workbook()

# TODO: update regex
regex_pattern = "#[\w]*"
noise_list = set(stopwords.words('english\en'))


lem = WordNetLemmatizer()
stem = PorterStemmer()


example_sent = "This is a sample sentence, showing off the stop words filtration and #hashtag to test"

# Lemmatizes word
def _lemmatize_word(input_word):
    lemmatized_word = lem.lemmatize(input_word, "v")
    return lemmatized_word


# Stems word(Verb are changed to their base format)
def _stem_word(input_word):
    stem_word = stem.stem(input_word)
    return stem_word


# Removes text pattern given in regex
def _remove_regex(input_text, regex_pattern):
    urls = re.finditer(regex_pattern, input_text)
    for i in urls:
        input_text = re.sub(i.group().strip(), '', input_text)
    return input_text


# Removes extra words (noise words/ stop words)
def _remove_noise(input_text):
    words = input_text.split()
    noise_free_words = [word for word in words if word not in noise_list]
    # Removed lemmatization to increase freedom is speech
    # lemmatized_words = [_lemmatize_word(w) for w in noise_free_words]
    noise_free_text = " ".join(noise_free_words)
    return noise_free_text


# cleans comment to give a more meaningful interpretation
def cleanComment(comment):

    lowerComment = comment.lower()
    cleanComment = lowerComment\
        .replace("would have", "would've")\
        .replace("should have", "should've")\
        .replace("could have", "could've")\
        .replace("must have", "must've")\
        .replace("are not", "aren't")\
        .replace("can not", "can't")\
        .replace("could not", "couldn't")\
        .replace("did not", "didn't")\
        .replace("do not", "don't")\
        .replace("does not", "doesn't")\
        .replace("had not", "hadn't")\
        .replace("has not", "hasn't")\
        .replace("have not", "haven't")\
        .replace("is not","isn't")\
        .replace("must not", "mustn't")\
        .replace("should not", "shouldn't")\
        .replace("was not","wasn't")\
        .replace("were not","weren't")\
        .replace("will not","won't")\
        .replace("would not","wouldn't")\

    return cleanComment


def cleanCommentX(comment):
    # Section Marker:  Superlative translator

    wb = xlrd.open_workbook('Xcel Files/ComperativeXSuperlatives.xlsx')
    supsSheet = wb.sheet_by_index(0)

    comment = comment.lower()
    wordArray = comment.split()
    supsList = []
    supsWord = ""

    while 'very' in wordArray:

        if 'very' in wordArray:
            indx = wordArray.index('very') + 1
            baseWord = wordArray[indx]
            supsWord = ""
            # print(baseWord)

            for i in range(supsSheet.nrows):
                for j in range(supsSheet.ncols):
                    supsList.append(supsSheet.cell_value(i, j))
                    if baseWord == supsSheet.cell_value(i, j).replace(" ", ""):
                        supsWord = supsSheet.cell_value(i, j + 2).replace(" ", "")
                        # print(supsWord)

            if supsWord != "":
                basePhrase = 'very ' + baseWord
                comment = comment.replace(basePhrase, supsWord)

            wordArray[wordArray.index('very')] = ""
            # print(wordArray)
            # print(comment)

    return comment


def cleanCommentZ(comment):
    # Section Marker:  Antonym translator
    # This must be done during parsing and not during cleaning, because we must assign weights to them.

    wb = xlrd.open_workbook('Xcel Files/Anotnyms.xlsx')
    antoSheet = wb.sheet_by_index(0)

    comment = comment.lower()
    wordArray = comment.split()
    antoList = []
    antoWord = ""

    while 'not' in wordArray:

        if 'not' in wordArray:
            indx = wordArray.index('not') + 1
            baseWord = wordArray[indx]
            antoWord = ""
            # print(baseWord)

            for i in range(antoSheet.nrows):
                antoList.append(antoSheet.cell_value(i, 0))
                if baseWord == antoSheet.cell_value(i, 0):
                    antoWord = antoSheet.cell_value(i, 1).replace(" ", "")


            if antoWord != "":
                basePhrase = 'not ' + baseWord
                antoWordSet = antoWord.split(',')
                # "*"  used for tagging
                comment = comment.replace(basePhrase, '*' + antoWordSet[0])

            wordArray[wordArray.index('not')] = ""

    return comment


# Gives a unique array
def unique(list1):
    x = np.array(list1)
    return np.unique(x)

# Complete cleaning function
def clean(comment):
    return cleanComment(cleanCommentZ(cleanCommentX(comment)))

# Opens a workbook (The lookup table) and writes the lookup table
def openWB(sheetName, wordlist):

    print(wordlist)
    sheet1 = wb.add_sheet(sheetName)
    for word, value in wordlist:
        testObj = word,value
        sheet1.write(wordlist.index(testObj), 0, word)
        sheet1.write(wordlist.index(testObj), 1, value)




statement = _remove_noise(_remove_regex(example_sent, regex_pattern))


# auxillary
word_tokens = word_tokenize(statement)
tagged = nltk.pos_tag(word_tokens)


# Main function to analyze the data received by the initial survey
# Procedure: Gets Excel Values, sorts the responses, gets the unique list of words used
def analyzeInitSurvey(KeyDeiverName, numCol, commentCol):
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    vallist = []
    wordlist = []


    # Get comments
    for i in range(sheet.nrows):
        vallist.append(clean(sheet.cell_value(i, commentCol)))
        tokenz = nltk.pos_tag(word_tokenize(clean(sheet.cell_value(i, commentCol))))
        for word, pos in tokenz:
            wordlist.append(word+"_"+pos)

    uniqueList = unique(wordlist)
    resultList = []

    for word in uniqueList:
        counter = 0
        respCounter = 0
        averageVal = 0
        for response in vallist:
            responseTokens = nltk.pos_tag(word_tokenize(response))
            responseList = []
            for wrd, pos in responseTokens:
                responseList.append(wrd+"_"+pos)

            if word in responseList:
                counter = counter + 1
                respCounter = respCounter + int(sheet.cell_value(vallist.index(response), numCol))
                averageVal = respCounter/counter


        robject = word, averageVal;
        resultList.append(robject)

    # Writing value to another excel sheet
    openWB(KeyDeiverName, resultList)

# Creating the lookup table
analyzeInitSurvey("Employee Development", 5, 6)
analyzeInitSurvey("Culture", 11, 12)
analyzeInitSurvey("Work-Life Balance", 17, 18)
analyzeInitSurvey("Leadership", 23, 24)
wb.save(saveFileName)

def getLookupTable(sheet) :
    wb = xlrd.open_workbook(saveFileName)
    qSheet = wb.sheet_by_name(sheet)
    # print(qSheet.cell_value(0, 0))

    qlist = []
    for i in range(qSheet.nrows):
        qlist.append(qSheet.row_values(i))

    return qlist


def isImportant(comment):
    comment = comment.lower()
    wordArray = comment.split()

    keyWordList  = []

    wb = xlrd.open_workbook('Xcel Files/EEGlossary.xlsx')
    keyWordSheet = wb.sheet_by_index(0)

    for i in range(keyWordSheet.nrows):
        keyWordList.append(keyWordSheet.cell_value(i, 0))

    for word in wordArray:
        for keyWord in keyWordList:
            keyWordX = keyWord.lower()
            if word == keyWordX:
                return True

    return  False




def predictComment(comment, kd):
    cleanedComment = clean(comment)
    print(cleanedComment)
    lookupTable = getLookupTable(kd)
    tokens = nltk.pos_tag(word_tokenize(cleanedComment))
    tokenList, valueList = [], []
    totVal, counter = 0,0
    for wrd, pos in tokens:
        if (pos in "JJ" or pos in "VB"):
            if(wrd not in noise_list):
                tokenList.append(wrd + "_" + pos)
                print(wrd)
                taggedWord = wrd + "_" + pos
                for word, val in lookupTable:
                    if taggedWord == word:
                        totVal = totVal + val
                        counter = counter + 1

    if(totVal == 0 and counter == 0):
        totVal = 3 # setting unknown statements to neutral
        counter = 1

    avgVal = totVal/counter

    print(avgVal)

    return avgVal



# predictComment("The company does not give enough recognition","Employee Development")
# predictComment("Fun culture with motivating people","Culture")
# predictComment("Workload is manageable but need more flexible hours","Work-Life Balance")
# predictComment("Strong leadership. Always cares about their employees","Leadership")
# predictComment("Weak and reckless leadership","Leadership")
predictComment("My team is not bad","Culture")
predictComment("My team is good","Culture")
predictComment("bad","Culture")
