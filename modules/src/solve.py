import random


def solve(input):
        ss=str(input)
        s=""
        flag=0
        for i in ss:
            if (i=='p' or i=='l'or i=='u'or i=='s'):
                if flag==0:
                         s=s+"+"
                         flag=1
            else:
                s=s+i
                flag=0
        prev=0
        prev_operator='+'
        val=0
        res=0
        for i in s:
                if i>='0' and i<='9':
                        val=val*10+int(i)
                else :
                        if prev_operator=='+':
                                res=(res+val)
                        elif prev_operator=='-':
                                res=(res-val)
                        elif prev_operator=='*':
                                res=(res*val)
                        elif prev_operator=='/':
                                res=(res/val)
                        prev_operator=i
                        val=0
        if prev_operator=='+':
                res=(res+val)
        elif prev_operator=='-':
                res=(res-val)
        elif prev_operator=='*':
                res=(res*val)
        elif prev_operator=='/':
                res=(res/val)        
        return str(res)

def process(input, entities=None):
           
    output = {
        'input': input,
        'output': solve(input),
        'success': True
    }
    return solve(input)



