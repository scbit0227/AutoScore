#coding=utf-8

import os, time, sys, re
import chardet
import json
import Upload_Parse
import RCTjudge, RCTeval, RCTevidence

SENTENCE_DATA_DIR = '..\\paper_PDF'

def getMetadata(FILE_DIR): 
    metas, blocks = Upload_Parse.main(FILE_DIR)
    
    if len(metas) == 0 or len(blocks) == 0:
        return None
      
    paper_info = {}
    paper_info['Title'] = metas['Title']
    if metas.has_key('Abstract'):
        paper_info['Abstract'] = metas['Abstract']
    else:
        paper_info['Abstract'] = ""
    
    block_num = len(blocks)
    #print block_num
    try:       
        for i in range(block_num):
            if len(blocks[i].values()[0]) > 0:
                content = blocks[i].values()[0][0].lower()
                if len(content) <= 30:
                    #print i, content
                    #find METHODS index
                    METHODS_index = content.find("method")
                    if METHODS_index > -1 and i > 10:
                        METHODS_index = i
                        break
        for i in range(block_num):
            if len(blocks[i].values()[0]) > 0:
                content = blocks[i].values()[0][0].lower()
                if len(content) <= 30:
                    #find RESULTS index
                    RESULT_index = content.find("result")
                    #if RESULT_index > -1 and i >= 15:
                    if RESULT_index > -1 and i > METHODS_index:
                        RESULT_index = i
                        break
        for i in range(block_num):
            if len(blocks[i].values()[0]) > 0:
                content = blocks[i].values()[0][0].lower()
                if len(content) <= 30:
                    #find DISCUSSION index
                    DISCUSSION_index = content.find("discussion")
                    if DISCUSSION_index > -1 and i >= block_num * 0.5:
                        DISCUSSION_index = i
                        break       
                          
        method_string = ""
        print METHODS_index, RESULT_index, DISCUSSION_index
        LOG_FILE.write("METHOD_INDEX:   " + str(METHODS_index) + " RESULT_INDEX:  " + str(RESULT_index) + " DISCUSSION_INDEX:   " + str(DISCUSSION_index) + "\n")
        if METHODS_index > -1:
            if RESULT_index > -1:
                for i in range(METHODS_index, RESULT_index):
                    if len(blocks[i].values()[0]) > 0:
                        method_string += blocks[i].values()[0][0].lower() + " "
            elif DISCUSSION_index > -1:
                for i in range(METHODS_index, DISCUSSION_index):
                    if len(blocks[i].values()[0]) > 0:
                        method_string += blocks[i].values()[0][0].lower() + " "
            else:
                for i in range(METHODS_index, block_num):
                    if len(blocks[i].values()[0]) > 0:
                        method_string += blocks[i].values()[0][0].lower() + " "
        else:
            if RESULT_index > -1:
                for i in range(0, RESULT_index):
                    if len(blocks[i].values()[0]) > 0:
                        method_string += blocks[i].values()[0][0].lower() + " "
            elif DISCUSSION_index > -1:          
                for i in range(0, DISCUSSION_index):
                    if len(blocks[i].values()[0]) > 0:
                        method_string += blocks[i].values()[0][0].lower() + " "
            else:
                for i in range(0, block_num):
                    if len(blocks[i].values()[0]) > 0:
                        method_string += blocks[i].values()[0][0].lower() + " "
        method_string = re.sub(r'-\s','',method_string)
        paper_info['Method'] = method_string
    except:
        s = sys.exc_info()
        #print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
        LOG_FILE.write("Error '%s' happened on line %d in function getMetadata\n" % (s[1],s[2].tb_lineno))
        
    return paper_info
    
    
def main():
    try:
        print '===============Program starts:==============\n'
        start = time.clock()
        all_result = {}
        evidence = RCTevidence.loadEvidence()    
        for p, d, f in os.walk(SENTENCE_DATA_DIR):
            for filename in f:
                path = os.path.join(p, filename)
                paper_id = filename.split('.')[0]
                if filename.endswith('.pdf'):
                    print filename
                    LOG_FILE.write(filename + '\n')
                    try:
                        paper_info = getMetadata(path)
                        if paper_info is None:
                            LOG_FILE.write(path.split('\\')[-1] + 'teambeam failure\n')
                            continue
                        method_string = paper_info['Method'].encode("utf-8")
                        if len(method_string) > 0:
                            info_file = open(os.path.join("..\\paper_info\\",paper_id), 'w')
                            info_file.write(method_string)
                            info_file.close()
                            all_result[paper_id] = {}
                            single_result = RCTjudge.getJudgement(paper_id, method_string, evidence)
                            all_result[paper_id] = single_result
                            print single_result
                        else:
                            LOG_FILE.write(path.split('\\')[-1] + ' extract method error\n')
                    except:
                        s = sys.exc_info()
                        print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
                        LOG_FILE.write("UNKWOWN ERROR OCUCURS\n")
                        continue
                else:
                    print 'Error: File is not a PDF!'
                    continue
            time.sleep(3)
        with open('all_result.json','w+') as js:
            json.dump(all_result, js, indent = 2)
              
        end = time.clock()
        print '=========================================='
        print 'Time used (s):\t' + str(end - start)
        print str(len(all_result)) + ' results returned'
        
    except:
        s = sys.exc_info()
        print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
        LOG_FILE.write("Error '%s' happened on line %d in function main\n" % (s[1],s[2].tb_lineno))


if __name__ == '__main__':
    LOG_FILE = open('log.txt','w+')
    main()
    raw_input('Press ENTER key to exit\n')   
    LOG_FILE.close()
    exit()       
            
