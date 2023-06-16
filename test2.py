import numpy as np 
import pandas as pd

def find_nearest(array,value):
    idx = pd.Series(np.abs(array-value)).idxmin()
    return idx, array[idx]

def test_chow1(ctx):
    assert ctx.answer1!='___', "Please enter a valid answer"


def test_findnearest(ctx):  ### test name is the same after #testEd () 
    x = ctx.x_true
    funtest = ctx.find_nearest(x, 2.2)
    true = find_nearest(x,  2.2)
    assert funtest==true, 'Something is wrong, recheck your function code' 


def test_shape(ctx):  ### test name is the same after #testEd () 
    val = ctx.x_train
    #print(testdf)
    assert  val.shape[0]==120, 'Train set is not 60%'
#    assert  np.allclose(testdf.shape[1], 4, atol=0.0), 'Expected 4 columns. Use pd.read_csv(filename, index_col=0)'

def test_nums(ctx):  ### test name is the same after #testEd () 
    val = ctx.k_list
    #print(testdf)
    assert  val.shape[0]==70, 'Check k_list again, it should be 70 integers ranging from 1 to 70'