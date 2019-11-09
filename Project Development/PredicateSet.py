import os
import sys

# class PredicateSet:

#---------- longestTimeWaitedToProceedStaight predicate set ----------#
def longestTimeWaitedToProceedStraight_0(time):
    if time == 0:
        return True
    else:
        return False 

def longestTimeWaitedToProceedStraight_0_15(time):
    if 0 < time <= 15:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_15_30(time):
    if 15 < time <= 30:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_30_45(time):
    if 30 < time <= 45:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_45_60(time):
    if 45 < time <= 60:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_60_90(time):
    if 60 < time <= 90:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_90_120(time):
    if 90 < time <= 120:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_120_150(time):
    if 120 < time <= 150:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_150_180(time):
    if 150 < time <= 180:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_180_210(time):
    if 180 < time <= 210:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_210_240(time):
    if 210 < time <= 240:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_240_270(time):
    if 240 < time <= 270:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_270_300(time):
    if 270 < time <= 300:
        return True
    else:
        return False

def longestTimeWaitedToProceedStraight_300(time):
    if time > 300:
        return True
    else:
        return False

#---------- longestTimeWaitedToTurnLeft predicate set ----------#
def longestTimeWaitedToTurnLeft_0(time):
    if time == 0:
        return True
    else:
        return False 

def longestTimeWaitedToTurnLeft_0_15(time):
    if 0 < time <= 15:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_15_30(time):
    if 15 < time <= 30:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_30_45(time):
    if 30 < time <= 45:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_45_60(time):
    if 45 < time <= 60:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_60_90(time):
    if 60 < time <= 90:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_90_120(time):
    if 90 < time <= 120:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_120_150(time):
    if 120 < time <= 150:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_150_180(time):
    if 150 < time <= 180:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_180_210(time):
    if 180 < time <= 210:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_210_240(time):
    if 210 < time <= 240:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_240_270(time):
    if 240 < time <= 270:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_270_300(time):
    if 270 < time <= 300:
        return True
    else:
        return False

def longestTimeWaitedToTurnLeft_300(time):
    if time > 300:
        return True
    else:
        return False
predicateList = [longestTimeWaitedToProceedStraight_0, longestTimeWaitedToProceedStraight_0_15, longestTimeWaitedToProceedStraight_15_30, longestTimeWaitedToProceedStraight_30_45, longestTimeWaitedToProceedStraight_45_60, longestTimeWaitedToProceedStraight_60_90, longestTimeWaitedToProceedStraight_90_120, longestTimeWaitedToProceedStraight_120_150, longestTimeWaitedToProceedStraight_150_180, longestTimeWaitedToProceedStraight_180_210, longestTimeWaitedToProceedStraight_210_240, longestTimeWaitedToProceedStraight_240_270, longestTimeWaitedToProceedStraight_270_300, longestTimeWaitedToProceedStraight_300, longestTimeWaitedToTurnLeft_0, longestTimeWaitedToTurnLeft_0_15, longestTimeWaitedToProceedStraight_15_30, longestTimeWaitedToTurnLeft_30_45, longestTimeWaitedToProceedStraight_45_60, longestTimeWaitedToTurnLeft_60_90, longestTimeWaitedToProceedStraight_90_120, longestTimeWaitedToTurnLeft_120_150, longestTimeWaitedToProceedStraight_150_180, longestTimeWaitedToTurnLeft_180_210, longestTimeWaitedToTurnLeft_210_240, longestTimeWaitedToTurnLeft_240_270, longestTimeWaitedToTurnLeft_270_300, longestTimeWaitedToTurnLeft_300]



def run():
    print(predicateList[0](0))

    # main entry point
if __name__ == "__main__":
    run()