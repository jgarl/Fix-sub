#!/usr/bin/env python3

import sys
import pysrt


def check_param():
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

def getnumbers(subs):
    """ return a list of the subs to not shift """
    numbers = []
    try:
        if(len(sys.argv) == 6):
            param_list = sys.argv[5][1:-1]
            if(param_list.find(":") != -1):
                splitted = param_list.split(":")
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
                    numbers.append(int(i))

            elif(param_list.find(",") != -1):
                for i in param_list.split(","):
                    if(int(i) > len(subs)):
                        numbers.append(len(subs) - 1)
                    else:
                        numbers.append(int(i) - 1)
            else:
                if(int(param_list) > len(subs)):
                    numbers.append(len(subs) - 1)
                else:
                    numbers.append(int(param_list) - 1)
    except:
        numbers = [-1]
        print("Error in last parameter")

    return numbers

def main():
    try:
        subs = pysrt.open(sys.argv[1], encoding='iso-8859-1')
        sub_numbers = getnumbers(subs)

        if((len(sub_numbers) == 0) or (sub_numbers[0] != -1)):
            for i in range(len(subs)):
                index = i
                if(len(sys.argv) == 6):
                    if(sys.argv[4] == "-e"):
                        if(i not in sub_numbers):
                            index = i
                        else:
                            continue
                    else:
                        if(i in sub_numbers):
                            index = i
                        else:
                            continue
                sub = subs[index]
                start = sub.start.to_time()
                end = sub.end.to_time()
                start_time = (start.hour*3600) + (start.minute*60) + start.second + (start.microsecond/1000000)
                end_time = (end.hour*3600) + (end.minute*60) + end.second + (end.microsecond/1000000)
                if(sys.argv[2] == "-f"):
                    start_time *= float(sys.argv[3])
                    end_time *= float(sys.argv[3])
                else:
                    start_time /= float(sys.argv[3])
                    end_time /= float(sys.argv[3])

                microseconds = (str(start_time-int(start_time))[2:])[:3]
                minutes, seconds = divmod(start_time, 60)
                hours, minutes = divmod(minutes, 60)
                sub.start = "%02d:%02d:%02d,%02d"%(int(hours), int(minutes), int(seconds), int(microseconds))
                microseconds = (str(end_time-int(end_time))[2:])[:3]
                minutes, seconds = divmod(end_time, 60)
                hours, minutes = divmod(minutes, 60)
                sub.end= "%02d:%02d:%02d,%02d"%(int(hours), int(minutes), int(seconds), int(microseconds))
            subs.save('./fixed.srt', encoding='utf-8')
            print("New file is saved in script directory as 'fixed.srt'")
    except:
        print("Error while opening the file")

if __name__ == "__main__":
    if(check_param()):
        main()
    else:
        print("Error in parameters")

