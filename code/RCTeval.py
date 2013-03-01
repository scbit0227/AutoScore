#coding=utf-8

from __future__ import division
import json
    
def calcMetrics(by_sys, by_gs, correct):
    precision = correct / by_sys
    recall = correct / by_gs
    f_score = 2 * precision * recall / (precision + recall)
    return (round(precision,4), round(recall,4), round(f_score,4))

def getEvaluationResult(output, truth):
    
    judgement_level = {'A':{'right': [],'wrong': []},
                       'B':{'right': [],'wrong': []},
                       'C':{'right': [],'wrong': []},
                       'D':{'right': [],'wrong': []},
                       'E':{'right': [],'wrong': []}}
    detail_level = {'reported':{'right': [],'wrong': []},
                    'conducted':{'right': [],'wrong': []},
                    'described':{'right': [],'wrong': []},
                    'properly':{'right': [],'wrong': []},
                    'result':{'right': [],'wrong': []}}
    levels = ['reported','conducted','described','properly','result']
    appraisal = ['A','B','C','D','E']
    for k in output.keys():
        for kk in levels:
            if output[k][kk] == truth[k][kk]:
                detail_level[kk]['right'].append(k)
            else:
                detail_level[kk]['wrong'].append(k)
        
        if output[k]['result'] == truth[k]['result']:
            judgement_level[truth[k]['result']]['right'].append(k)
        else:
            judgement_level[truth[k]['result']]['wrong'].append((k, output[k]['result']))

    rate = {'reported':(),'conducted':(),'described':(),'properly':(),'result':()}
    for k in rate.keys():
        correct = len(detail_level[k]['right'])
        by_sys = len(output)
        by_gs = len(truth)
        rate[k] = calcMetrics(by_sys, by_gs, correct)
        print k,rate[k]
    
    
    with open('eval_judge.json','w+') as js1:
        json.dump(judgement_level, js1, indent = 2)
    with open('eval_level.json', 'w+') as js2:
        json.dump(detail_level, js2, indent = 2)
       
    return judgement_level, detail_level
    
