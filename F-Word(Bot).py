# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 19:24:25 2022

@author: anjan
"""
## Replace the asterisks used in the f-word with any random word in the
## dictionary that matches

#5. Function to detect f-word or something that resembles it from a sentence
#6. Function to count the number of f-words or its lookalike in a sentence
#3. Prepare a reply for the number of time u or k occurs showing concern
#8. Reply for number of exclamations
#9. Prepare a reply for the use of 'F-bomb'

## Tasks
## 1. Function to connect to a web dictionary service. 
## 2. Function to replace the asterisks with other letters to form a
##    meaningful word
## 4. Prepare a reply for asterisks 



import re
import numpy as np
import praw


reddit =praw.Reddit(
    user_agent="",
    client_id="",
    client_secret="",
    username="",
    password="",
    )
    

def detect_f(word):
    """
    Parameters
    ----------
    word : str
        A word which has to be checked.

    Returns
    -------
    bool
        Returns True if the word is an F-Word or any of its variants.

    """
    
    special_chars='~!@#\$%\^&\*\(\)_\+=\?'
    reg_string='f[' +special_chars+ 'uc]'+ '[' +special_chars +'uc]+' +'k'
    f_detect=re.search(reg_string,word,re.IGNORECASE)
    reg_string='f+[' +special_chars+ 'uc]'+ '[' +special_chars +'uc]+' +'k'  
    f_word=re.findall(reg_string,word,re.IGNORECASE)
    
    if bool(f_detect):
         return True, f_word[0]
    
    anomalous_words=['fuk','fucc','f-bomb','fak']
    if word.casefold() in anomalous_words:
        return True, word
    
    
    return False,None


def char_count(word,char):
    """
    Parameters
    ----------
    word : str
    char : str
        Any character.
    Returns
    -------
    The number of times a particular character occurs in a word.

    """
    
    word=list(word)
    count=0
    for i in word:
        if i==char:
            count+=1
            
    if count >0:
        return count
    return None


def char_count_list(word):
    word=word.casefold()
    word=list(word)
    chars=list('fuck!')
    
    char_count_list=[]
    chars_list=[]
    for letter in chars:
        num_chars=char_count(word, letter)
        if bool(num_chars):
            if num_chars>2:
                chars_list.append(letter)
                char_count_list.append(num_chars)
    return chars_list,char_count_list 


def char_count_list_max(text):
    text=text.split(' ')
    f_word=''
    chars=None
    char_cnt_list=None
    for word in text:
        f_word_bool,_=detect_f(word)
        if f_word_bool:
            if len(list(detect_f(word)[1]))>len(list(f_word)):
                chars,char_cnt_list=char_count_list(word)
                f_word=detect_f(word)[1]
    
    return chars,char_cnt_list 


def count_ftext(text):
    """
    Parameters
    ----------
    text : str
        A text which is to searched.

    Returns
    -------
    The number of times 'fuck' or it's variants are used.

    """
    text=text.split()
    count=0
    for word in text:
        f_bool,_=detect_f(word)
        if f_bool:
            count+=1
    if count>0:
        return count
    return None


def F_bomb_reply(text):
    text=text.split()
    for word in text:
        if word.lower()=='f-bomb':
            reply="It's okay, you can curse on the internet."
            return reply
    return None


def many_chars_reply(chars, nums):
    

    char_dict={"!":"exclamations", "u":"us", "f":"fs", "c":"cs", "k":"ks"}
    
    if len(chars)==1:
        if nums[0]>2:
            reply="At least one word has {} too many {}!".\
            format(nums[0]-1,char_dict[chars[0]])
            return reply
    elif len(chars)>1:
        i=0
        reply="At least one word has "
        while i <len(chars):
            curr_char=chars[i]
            curr_num=nums[i]
            if curr_num>2:
                reply+= "{} too many {}, ".\
                            format(curr_num-1,char_dict[curr_char])
            i+=1
       
        reply=reply.split(' ')
        reply[-2]=list(reply[-2])
        reply[-2].pop(-1)
        reply[-2]=''.join(reply[-2])
        reply.insert(-5,'and')
        reply[-1]=list(reply[-1])
        reply.pop(-1)
        reply=' '.join(reply)
        reply+="!"
        reply+="\nHere's a cat video to help calm you down. "
    
    else:
        return None
    return reply
            
        
    
    return None
  
  
def final_reply(comment):
    f_bomb_prob=np.random.uniform(0,1)
    if f_bomb_prob>0.5:
        r1=F_bomb_reply(comment)
        return r1
    num_fs=count_ftext(comment)
    
    
    
    r1="You have {} f-word(s) in your comment.".format(num_fs)

    comm_chars,comm_char_count=char_count_list_max(comment)
    
    r2=many_chars_reply(comm_chars, comm_char_count)
    if type(r1)==type(r2):
        reply=r1+'\n'+r2
    
        return reply
    
    return None
    
    
target_sub = "AdmoniTestCommunity"
subreddit = reddit.subreddit(target_sub)

# enchant dictionary

for submission in subreddit.hot(limit=10):
    print(submission.title)
    for comment in submission.comments:
        if hasattr(comment, "body"):
            #print(str(comment.body))
    # check the trigger_phrase in each comment
            if final_reply(comment.body) !=None:
  
    # extract the word from the comment

  
    # initialize the reply text
                reply_text = final_reply(comment.body)
                print(comment.body)
  
    # comment the similar words
                comment.reply(reply_text)
    
