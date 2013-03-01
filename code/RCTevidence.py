#coding=utf-8

import json, os

#REPORTED_EVI = os.getcwd() + '\\evidence\\evi_1.txt'
#CONDUCTED_EVI = os.getcwd() + '\\evidence\\evi_2.txt'
#PROPER_POS_EVI = os.getcwd() + '\\evidence\\evi_4_pos.txt'
#PROPER_NEG_EVI = os.getcwd() + '\\evidence\\evi_4_neg.txt'

REPORTED_EVI =  '..\\evidence\\evi_1.txt'
CONDUCTED_EVI = '..\\evidence\\evi_2.txt'
PROPER_POS_EVI = '..\\evidence\\evi_4_pos.txt'
PROPER_NEG_EVI = '..\\evidence\\evi_4_neg.txt'

def loadEvidence():
    evidence_dict = {}
    reported_evi = loadReportedEvidence()
    conducted_evi = loadConductedEvidence()
    described_evi = loadDescribedEvidence()
    properly_evi = loadProperlyEvidence()
    evidence_dict = {'reported':reported_evi,'conducted':conducted_evi,
                     'described': described_evi,'properly':properly_evi}
    return evidence_dict

def loadReportedEvidence():
    evi_list = []
    with open(REPORTED_EVI) as evi:
        for line in evi:
            evi_list.append(line.strip())
    return evi_list

def loadConductedEvidence():
    evi_list = []
    with open(CONDUCTED_EVI) as evi:
        for line in evi:
            evi_list.append(line.strip())
    return evi_list

def loadDescribedEvidence():
    '''
    freq_dict = {}
    with open(DESCRIBED_EVI) as js:
        freq_dict = json.load(js)
    return freq_dict
    '''
    pass

def loadProperlyEvidence():
    evi_dict = {'pos':[],'neg':[]}
    with open(PROPER_POS_EVI) as pos:
        pos_list = []
        for line in pos:
            pos_list.append(line.strip())
    with open(PROPER_NEG_EVI) as neg:
        neg_list = []
        for line in neg:
            neg_list.append(line.strip())
    evi_dict['pos'] = pos_list
    evi_dict['neg'] = neg_list
    return evi_dict
