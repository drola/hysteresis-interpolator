# -*- coding: utf-8 -*-
from scipy.interpolate import interp1d
import numpy as np

class HysteresisInterpolator(object):
    def _prepareArray(self, a):
        a = sorted(a, key=lambda row: row[0])
        newA = []
        curX = None
        curCnt = 0
        curAvg = 0
        for row in a:
            if(row[0]!=curX):
                if(curX != None):
                    newA.append([curX, curAvg])
                curX = row[0]
                curAvg = row[1]
                curCnt = 1
            else:
                curAvg = (curAvg*curCnt + row[1])/(curCnt+1)
                curCnt += 1
        if(curX != None):
            newA.append([curX, curAvg])
        newA = np.transpose(newA)
        return newA
        
    @staticmethod
    def fromFile(filename, xcol, ycol, skip = 0):
        data = np.loadtxt(filename, usecols=(xcol, ycol))
        return HysteresisInterpolator(data[skip:])
        
    def __init__(self, data):
        #split list of values based on gradient of X
        a = []
        b = []
        prev = None
        grad = 0
        for row in data:
            if(prev==None):
                prev = row
                continue
            grad = row[0] - prev[0]
            if(grad>0):
                b.append(prev)
            else:
                a.append(prev)
            
            prev= row
        if(grad>0):
            b.append(prev)
        elif(grad<0):
            a.append(prev)
            
        #reshape data
        a = self._prepareArray(a)
        b = self._prepareArray(b)
        
        #linear
        self.linearA = interp1d(a[0], a[1])
        self.linearB = interp1d(b[0], b[1])
        
        #cubic
        self.cubicA = interp1d(a[0], a[1], kind='cubic')
        self.cubicB = interp1d(b[0], b[1], kind='cubic')
        
        #quadratic
        self.quadraticA = interp1d(a[0], a[1], kind='quadratic')
        self.quadraticB = interp1d(b[0], b[1], kind='quadratic')
        
    def __call__(self, x, grad):
        if(grad>0):
            cubic = self.cubicB(x)
            quadratic = self.quadraticB(x)
            linear = self.linearB(x)
        else:
            cubic = self.cubicA(x)
            quadratic = self.quadraticA(x)
            linear = self.linearA(x)
            
        delta = abs(cubic-linear)
        return (linear, quadratic, cubic, delta)
        