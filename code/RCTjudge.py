#coding=utf-8

from __future__ import division
import os
     
def judgeReported(evi, content):
    for item in evi['reported']:
        flag = content.find(item)
        if flag > 0:
            return 'Y'
    for item in evi['properly']['neg']:
        flag = content.find(item)
        if flag > 0:
            return 'Y'
    return 'N'

def judgeConducted(evi, content):
    for item in evi['conducted']:
        flag = content.find(item)
        if flag > 0:
            return 'N'
    ran_flag = 'N'
    for item in evi['reported']:
        flag = content.find(item)
        if flag > 0:
            ran_flag = 'Y'
    for item in evi['properly']['neg']:
        flag = content.find(item)
        if flag > 0 and ran_flag == 'N':
            return 'N'
    return 'Y'
    
def judgeDescribedOld(paper_id, evi, content):
    score = {}
    for k in content.keys():
        score[k] = 1
        excld = ['.',',',':','#','!','(',')','"','?']
        for e in excld:
            content[k] = content[k].replace(e, '')
        for word in content[k].split():
            if word in evi.keys():
                score[k] *= evi[word]
            else:
                score[k] *= 0.1
    ranking = [(score[key], key) for key in score.keys()]
    ranking.sort()
    ranking.reverse()
    
    for kk in score.keys():
        if score[kk] > 2000:
            return 'Y'    
    return 'N'

def judgeDescribed(evi, content):
    phrase = evi['properly']['pos'] + evi['properly']['neg']
    for item in phrase:
        flag = content.find(item)
        if flag > 0:
            return 'Y'
    return 'N'
        

def judgeProperly(evi, content):
    for p in evi['neg']:
        if content.find(p) > 0:
            print 'Not done properly:\t' + p
            return 'N'
    for q in evi['pos']:
        if content.find(q) > 0:
            print 'Done properly:\t' + q
            return 'Y'
    return 'N'
    
def getJudgement(paper_id, content_string, evidence):

    result = {}
    result['reported'] = judgeReported(evidence, content_string)
    if result['reported'] == 'N':
        result['conducted'] = 'N'
        result['described'] = 'N'
        result['properly'] = 'N'
        result['result'] = 'E'
        return result
    else:
        result['conducted'] = judgeConducted(evidence, content_string)
        if result['conducted'] == 'N':
            result['described'] = 'N'
            result['properly'] = 'N'
            result['result'] = 'D'
            return result
        else:
            result['described'] = judgeDescribed(evidence, content_string)
            if result['described'] == 'N':
                result['properly'] = 'N'
                result['result'] = 'C'
                return result
            else:
                result['properly'] = judgeProperly(evidence['properly'], content_string)
                if result['properly'] == 'N':
                    result['result'] = 'B'
                else:
                    result['result'] = 'A'
                return result
