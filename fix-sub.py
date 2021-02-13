#!/usr/bin/env python3

import sys
import pysrt


def checkParam():
    """ check if the parameters are correct """

    flag = True
    if((len(sys.argv) < 4) or (len(sys.argv) == 5) or (len(sys.argv) > 6)):
        flag = False
    elif(sys.argv[1][-4:] != ".srt"):
        flag = False
    elif(not((sys.argv[2] == "-f") or (sys.argv[2] == "-b"))):
        flag = False
    elif(len(sys.argv) == 6):
        if(not((sys.argv[4] == "-e") or (sys.argv[4] == "-i"))):
            flag = False
    else:
        try:
           conv = float(sys.argv[3])
        except:
            flag = False

    return flag

def getList(subs):
    """ return a list of the subs to not shift """
    _list = []
    try:
        if(len(sys.argv) == 6):
            paramList = sys.argv[5][1:-1]
            if(paramList.find(":") != -1):
                splitted = paramList.split(":")
                start = 0
                end = len(subs) - 1

                if(splitted[0] != ""):
                    start = int(splitted[0]) - 1
                if(splitted[1] != ""):
                    if(int(splitted[1]) > len(subs)):
                        end = len(subs) - 1
                    else:
                        end = int(splitted[1]) - 1

                for i in range(start, end + 1):
                    _list.append(int(i))

            elif(paramList.find(",") != -1):
                for i in paramList.split(","):
                    if(int(i) > len(subs)):
                        _list.append(len(subs) - 1)
                    else:
                        _list.append(int(i) - 1)
            else:
                if(int(paramList) > len(subs)):
                    _list.append(len(subs) - 1)
                else:
                    _list.append(int(paramList) - 1)
    except:
        _list = [-1]
        print("Error in last parameter")

    return _list

def main():
    try:
        subs = pysrt.open(sys.argv[1], encoding='iso-8859-1')
        subNumbers = getList(subs)

        if((len(subNumbers) == 0) or (subNumbers[0] != -1)):
            for i in range(len(subs)):
                index = i
                if(len(sys.argv) == 6):
                    if(sys.argv[4] == "-e"):
                        if(i not in subNumbers):
                            index = i
                        else:
                            continue
                    else:
                        if(i in subNumbers):
                            index = i
                        else:
                            continue
                sub = subs[index]
                start = sub.start.to_time()
                end = sub.end.to_time()
                startTime = (start.hour*3600) + (start.minute*60) + start.second + (start.microsecond/1000000)
                endTime = (end.hour*3600) + (end.minute*60) + end.second + (end.microsecond/1000000)
                if(sys.argv[2] == "-f"):
                    startTime *= float(sys.argv[3])
                    endTime *= float(sys.argv[3])
                else:
                    startTime /= float(sys.argv[3])
                    endTime /= float(sys.argv[3])

                microseconds = (str(startTime-int(startTime))[2:])[:3]
                minutes, seconds = divmod(startTime, 60)
                hours, minutes = divmod(minutes, 60)
                sub.start = "%02d:%02d:%02d,%02d"%(int(hours), int(minutes), int(seconds), int(microseconds))
                microseconds = (str(endTime-int(endTime))[2:])[:3]
                minutes, seconds = divmod(endTime, 60)
                hours, minutes = divmod(minutes, 60)
                sub.end= "%02d:%02d:%02d,%02d"%(int(hours), int(minutes), int(seconds), int(microseconds))
            subs.save('./fixed.srt', encoding='utf-8')
            print("New file is saved in script directory as 'fixed.srt'")
    except:
        print("Error while opening the file")

if __name__ == "__main__":
    if(checkParam()):
        main()
    else:
        print("Error in parameters")

