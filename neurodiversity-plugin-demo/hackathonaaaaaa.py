# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 21:01:55 2021

@author: zhang
"""

from bs4 import BeautifulSoup
import urllib.request
import nltk
from nltk.corpus import stopwords
  
response = urllib.request.urlopen('http://php.net/')
html = response.read()
soup = BeautifulSoup(html,"html5lib")
text = soup.get_text(strip=True)
tokens = text.split()
clean_tokens = list()
sr = stopwords.words('english')
for token in tokens:
    if not token in sr:
        clean_tokens.append(token)
freq = nltk.FreqDist(clean_tokens)
for key,val in freq.items():
    print (str(key) + ':' + str(val))
    

freq.plot(20,cumulative=False)
 
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
 
mytext1 = '''
An account of the early history of scanning electron microscopy has been presented by McMullan.[2][3] Although Max Knoll produced a photo with a 50 mm object-field-width showing channeling contrast by the use of an electron beam scanner,[4] it was Manfred von Ardenne who in 1937 invented[5] a microscope with high resolution by scanning a very small raster with a demagnified and finely focused electron beam. Ardenne applied scanning of the electron beam in an attempt to surpass the resolution of the transmission electron microscope (TEM), as well as to mitigate substantial problems with chromatic aberration inherent to real imaging in the TEM. He further discussed the various detection modes, possibilities and theory of SEM,[6] together with the construction of the first high resolution SEM.[7] Further work was reported by Zworykin's group,[8] followed by the Cambridge groups in the 1950s and early 1960s[9][10][11][12] headed by Charles Oatley, all of which finally led to the marketing of the first commercial instrument by Cambridge Scientific Instrument Company as the "Stereoscan" in 1965, which was delivered to DuPont.

Principles and capacities

Schottky-emitter electron source

Electron–matter interaction volume and types of signal generated
The signals used by an SEM to produce an image result from interactions of the electron beam with atoms at various depths within the sample. Various types of signals are produced including secondary electrons (SE), reflected or back-scattered electrons (BSE), characteristic X-rays and light (cathodoluminescence) (CL), absorbed current (specimen current) and transmitted electrons. Secondary electron detectors are standard equipment in all SEMs, but it is rare for a single machine to have detectors for all other possible signals.

Secondary electrons have very low energies on the order of 50 eV, which limits their mean free path in solid matter. Consequently, SEs can only escape from the top few nanometers of the surface of a sample. The signal from secondary electrons tends to be highly localized at the point of impact of the primary electron beam, making it possible to collect images of the sample surface with a resolution of below 1 nm. Back-scattered electrons (BSE) are beam electrons that are reflected from the sample by elastic scattering. Since they have much higher energy than SEs, they emerge from deeper locations within the specimen and, consequently, the resolution of BSE images is less than SE images. However, BSE are often used in analytical SEM, along with the spectra made from the characteristic X-rays, because the intensity of the BSE signal is strongly related to the atomic number (Z) of the specimen. BSE images can provide information about the distribution, but not the identity, of different elements in the sample. In samples predominantly composed of light elements, such as biological specimens, BSE imaging can image colloidal gold immuno-labels of 5 or 10 nm diameter, which would otherwise be difficult or impossible to detect in secondary electron images.[13] Characteristic X-rays are emitted when the electron beam removes an inner shell electron from the sample, causing a higher-energy electron to fill the shell and release energy. The energy or wavelength of these characteristic X-rays can be measured by Energy-dispersive X-ray spectroscopy or Wavelength-dispersive X-ray spectroscopy and used to identify and measure the abundance of elements in the sample and map their distribution.

Due to the very narrow electron beam, SEM micrographs have a large depth of field yielding a characteristic three-dimensional appearance useful for understanding the surface structure of a sample.[14] This is exemplified by the micrograph of pollen shown above. A wide range of magnifications is possible, from about 10 times (about equivalent to that of a powerful hand-lens) to more than 500,000 times, about 250 times the magnification limit of the best light microscopes.

Sample preparation

A spider sputter-coated in gold, having been prepared for viewing with an SEM

Low-voltage micrograph (300 V) of distribution of adhesive droplets on a Post-it note. No conductive coating was applied: such a coating would alter this fragile specimen.
SEM samples have to be small enough to fit on the specimen stage, and may need special preparation to increase their electrical conductivity and to stabilize them, so that they can withstand the high vacuum conditions and the high energy beam of electrons. Samples are generally mounted rigidly on a specimen holder or stub using a conductive adhesive. SEM is used extensively for defect analysis of semiconductor wafers, and manufacturers make instruments that can examine any part of a 300 mm semiconductor wafer. Many instruments have chambers that can tilt an object of that size to 45° and provide continuous 360° rotation.

Nonconductive specimens collect charge when scanned by the electron beam, and especially in secondary electron imaging mode, this causes scanning faults and other image artifacts. For conventional imaging in the SEM, specimens must be electrically conductive, at least at the surface, and electrically grounded to prevent the accumulation of electrostatic charge. Metal objects require little special preparation for SEM except for cleaning and conductively mounting to a specimen stub. Non-conducting materials are usually coated with an ultrathin coating of electrically conducting material, deposited on the sample either by low-vacuum sputter coating or by high-vacuum evaporation. Conductive materials in current use for specimen coating include gold, gold/palladium alloy, platinum, iridium, tungsten, chromium, osmium,[13] and graphite. Coating with heavy metals may increase signal/noise ratio for samples of low atomic number (Z). The improvement arises because secondary electron emission for high-Z materials is enhanced.

An alternative to coating for some biological samples is to increase the bulk conductivity of the material by impregnation with osmium using variants of the OTO staining method (O-osmium tetroxide, T-thiocarbohydrazide, O-osmium).[15][16]

Nonconducting specimens may be imaged without coating using an environmental SEM (ESEM) or low-voltage mode of SEM operation. In ESEM instruments the specimen is placed in a relatively high-pressure chamber and the electron optical column is differentially pumped to keep vacuum adequately[clarification needed] low at the electron gun. The high-pressure region around the sample in the ESEM neutralizes charge and provides an amplification of the secondary electron signal.[citation needed] Low-voltage SEM is typically conducted in an instrument with a field emission guns (FEG) which is capable of producing high primary electron brightness and small spot size even at low accelerating potentials. To prevent charging of non-conductive specimens, operating conditions must be adjusted such that the incoming beam current is equal to sum of outgoing secondary and backscattered electron currents, a condition that is most often met at accelerating voltages of 0.3–4 kV.[citation needed]

Embedding in a resin with further polishing to a mirror-like finish can be used for both biological and materials specimens when imaging in backscattered electrons or when doing quantitative X-ray microanalysis.

The main preparation techniques are not required in the environmental SEM outlined below, but some biological specimens can benefit from fixation.

Biological samples
For SEM, a specimen is normally required to be completely dry, since the specimen chamber is at high vacuum. Hard, dry materials such as wood, bone, feathers, dried insects, or shells (including egg shells[17]) can be examined with little further treatment, but living cells and tissues and whole, soft-bodied organisms require chemical fixation to preserve and stabilize their structure.

Fixation is usually performed by incubation in a solution of a buffered chemical fixative, such as glutaraldehyde, sometimes in combination with formaldehyde[18][19][20] and other fixatives,[21] and optionally followed by postfixation with osmium tetroxide.[18] The fixed tissue is then dehydrated. Because air-drying causes collapse and shrinkage, this is commonly achieved by replacement of water in the cells with organic solvents such as ethanol or acetone, and replacement of these solvents in turn with a transitional fluid such as liquid carbon dioxide by critical point drying.[22] The carbon dioxide is finally removed while in a supercritical state, so that no gas–liquid interface is present within the sample during drying.

The dry specimen is usually mounted on a specimen stub using an adhesive such as epoxy resin or electrically conductive double-sided adhesive tape, and sputter-coated with gold or gold/palladium alloy before examination in the microscope. Samples may be sectioned (with a microtome) if information about the organism's internal ultrastructure is to be exposed for imaging.

If the SEM is equipped with a cold stage for cryo microscopy, cryofixation may be used and low-temperature scanning electron microscopy performed on the cryogenically fixed specimens.[18] Cryo-fixed specimens may be cryo-fractured under vacuum in a special apparatus to reveal internal structure, sputter-coated and transferred onto the SEM cryo-stage while still frozen.[23] Low-temperature scanning electron microscopy (LT-SEM) is also applicable to the imaging of temperature-sensitive materials such as ice[24][25] and fats.[26]

Freeze-fracturing, freeze-etch or freeze-and-break is a preparation method particularly useful for examining lipid membranes and their incorporated proteins in "face on" view. The preparation method reveals the proteins embedded in the lipid bilayer."

'''
word = word_tokenize(mytext1)

print(word)
print(len(word))

words_no_punc = []
for w in word:
    if w.isalpha():
        words_no_punc.append(w.lower())
        
print(words_no_punc)
print(len(words_no_punc))

from nltk.corpus import stopwords
stopwords = stopwords.words('english')
clean_words = []

for w in words_no_punc:
    if w not in stopwords:
        clean_words.append(w)

print(clean_words)
print(len(clean_words))

from nltk.probability import FreqDist
fdist = FreqDist(clean_words)
data1 = fdist.most_common(25)
print(data1)
import matplotlib.pyplot as plt
fdist.plot(25)

######################wordcloud##########################
def Convert(tup, di):
    di = dict(tup)
    return di
   
tups = data1
dict_data1 = {}
converted_dict = Convert(tups, dict_data1)

from wordcloud import WordCloud

wc1 = WordCloud(width=2000,height=1200,font_path='/font/msyh.ttc',background_color='white').generate_from_frequencies(converted_dict)
fig = plt.figure(1)
plt.imshow(wc1)
plt.axis('off')
plt.show

######################uselessthinggggg####################
from nltk.stem import SnowballStemmer

snowball = SnowballStemmer('english')
word_list = clean_words


#################TF-IDF###################################
mytext = '''
An account of the early history of scanning electron microscopy has been presented by McMullan.[2][3] Although Max Knoll produced a photo with a 50 mm object-field-width showing channeling contrast by the use of an electron beam scanner,[4] it was Manfred von Ardenne who in 1937 invented[5] a microscope with high resolution by scanning a very small raster with a demagnified and finely focused electron beam. Ardenne applied scanning of the electron beam in an attempt to surpass the resolution of the transmission electron microscope (TEM), as well as to mitigate substantial problems with chromatic aberration inherent to real imaging in the TEM. He further discussed the various detection modes, possibilities and theory of SEM,[6] together with the construction of the first high resolution SEM.[7] Further work was reported by Zworykin's group,[8] followed by the Cambridge groups in the 1950s and early 1960s[9][10][11][12] headed by Charles Oatley, all of which finally led to the marketing of the first commercial instrument by Cambridge Scientific Instrument Company as the "Stereoscan" in 1965, which was delivered to DuPont.

'''
sentence = sent_tokenize(mytext)

import enchant
from nltk.corpus import stopwords
new_sentences = []
d = enchant.Dict("en_US")
sw = stopwords.words("english")
def clean_text(var):
    import re
    tmp = re.sub("[^A-z]+", ' ', var).strip().lower()
    tmp = [word for word in tmp.split() if d.check(word)]
    tmp = [word for word in tmp if word not in sw]
    tmp = ' '.join(tmp)
    return tmp
def stemming_algo(var):
    from nltk.stem import PorterStemmer
    ps = PorterStemmer() 
    tmp = var.split()
    tmp = [ps.stem(word) for word in tmp]
    tmp = ' '.join(tmp)
    return tmp
for sent in sentence:
    sample_text = clean_text(sent)
    sample_text = stemming_algo(sample_text)
    new_sentences.append(sample_text)
#print(new_sentences)
cv = CountVectorizer()
B_O_W = cv.fit_transform(new_sentences).toarray()
#print(cv.fixed_vocabulary_)
#print(B_O_W)

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
transformer = TfidfTransformer()
vectorizer=CountVectorizer()

tfidf = transformer.fit_transform(vectorizer.fit_transform(new_sentences))
words = vectorizer.get_feature_names() 
weight = tfidf.toarray()
print(words)
print(weight)


feature_TFIDF = {}
for i in range(len(weight)):
    for j in range(len(words)):
        # print(feature[j], weight[i][j])
        if words[j] not in feature_TFIDF:
            feature_TFIDF[words[j]] = weight[i][j]
        else:
            feature_TFIDF[words[j]] = max(feature_TFIDF[words[j]], weight[i][j])

print('first 10：')
featureList = sorted(feature_TFIDF.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
small_dict = {}
for i in range(1, 10 if len(featureList) > 10 else len(featureList)):
    small_dict[featureList[i][0]]= featureList[i][1]
#print(small_dict)
######################Thisiswordcloud2!!!!##########################

wc2 = WordCloud(width=2000,height=1200,font_path='/font/msyh.ttc',background_color='white').generate_from_frequencies(small_dict)
fig = plt.figure(2)
plt.imshow(wc2)
plt.axis('off')
plt.show



######worldnet
#from nltk.corpus import wordnet
  
#syn = wordnet.synsets("pain")
#print(syn[0].definition())
#print(syn[0].examples())

#####Get synonyms
#synonyms = []
#for syn in wordnet.synsets('Computer'):
#    for lemma in syn.lemmas():
#        synonyms.append(lemma.name())
#print(synonyms)

#from nltk.stem import PorterStemmer
  
#stemmer = PorterStemmer()
#print(stemmer.stem('working'))
#print(stemmer.stem('worked'))