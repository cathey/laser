# -*- coding: utf-8 -*-
"""
Neuri - Mirrors & laser problem

Created on Sat Jul  7 20:04:05 2018

@author: Cathey Wang
"""


"""
A single case
"""
class Case:
    # constructor, create variables
    def __init__(self, R, C):
        self.R = R  # row count
        self.C = C  # column count
        self.mirrors_horizontal = {rows:[] for rows in range(1,R+1)}
        self.mirrors_vertical = {cols:[] for cols in range(1,C+1)}
        self.laser1horizontal = {rows:[] for rows in range(1,R+1)}
        self.laser1vertical = {cols:[] for cols in range(1,C+1)}
        self.intersect = {cols:[] for cols in range(1,C+1)}
        
    # add mirror
    def add_mirror(self, r, c, mirror_type):
        self.mirrors_horizontal[r].append([c, mirror_type])
        self.mirrors_vertical[c].append([r, mirror_type])
        
    # sort mirrors
    def sort_mirrors(self):
        for r in range(1,self.R+1):
            self.mirrors_horizontal[r].sort()
        for c in range(1,self.C+1):
            self.mirrors_vertical[c].sort()
    
    # binary search in hashtable, find idx of the closest mirror, -1 if don't exist
    def binary_search_mirrors(self, idx, mirrors, direction):
        first = 0
        last = len(mirrors)-1
        if last == -1:
            return -1
        found = 0
        if direction == +1:     # right/down, find smallest larger than idx
            while first<=last and found == 0:
                midpoint = (first + last)//2
                if idx == mirrors[midpoint][0]:
                    found = 1
                    successor = midpoint+1
                    if successor >= len(mirrors) or successor < 0:
                        successor = -1
                elif idx > mirrors[midpoint][0]:
                    first = midpoint+1
                else:
                    last = midpoint-1
            if found == 0 and first > last:
                successor = first
        else:   # left/up, find largest smaller than idx
            while first<=last and found == 0:
                midpoint = (first + last)//2
                if idx == mirrors[midpoint][0]:
                    found = 1
                    successor = midpoint-1
                    if successor >= len(mirrors) or successor < 0:
                        successor = -1
                elif idx > mirrors[midpoint][0]:
                    first = midpoint+1
                else:
                    last = midpoint-1
            if found == 0 and first > last:
                successor = last
        return successor
    
    # walk laser 1 through case, save path to laser1horizontal & laser1vertical
    # return 0 if found exit, 1 if not
    def laser1go(self):
        # r, c, direction: 0 - right, 1 - up, 2 - left, 3 - down
        curr_state = [1, 0, 0]
        while 1:    # keep looping, will return when end
            if curr_state[2] == 0:  # going right
                # look in mirrors_horizontal to find smallest col > curr_state[1]
                c_mirror = self.binary_search_mirrors(curr_state[1], self.mirrors_horizontal[curr_state[0]], 1)
                if c_mirror == -1:  # not found
                    if curr_state[0] == self.R:
                        return 0
                    c_mirror = self.C+1
                    # save laser path
                    self.laser1horizontal[curr_state[0]].append([curr_state[1], c_mirror])
                    return 1
                else:
                    direction = self.mirrors_horizontal[curr_state[0]][c_mirror][1]*2+1
                    c_mirror = self.mirrors_horizontal[curr_state[0]][c_mirror][0]
                    # save laser path
                    self.laser1horizontal[curr_state[0]].append([curr_state[1], c_mirror])
                    # update state
                    curr_state = [curr_state[0], c_mirror, direction]
            elif curr_state[2] == 1:    # going up
                # look in mirrors_vertical to find largest row < curr_state[0]
                r_mirror = self.binary_search_mirrors(curr_state[0], self.mirrors_vertical[curr_state[1]], 0)
                if r_mirror == -1:  # not found
                    r_mirror = 0
                    # save laser path
                    self.laser1vertical[curr_state[1]].append([r_mirror, curr_state[0]])
                    return 1
                else:
                    direction = self.mirrors_vertical[curr_state[1]][r_mirror][1]*2
                    r_mirror = self.mirrors_vertical[curr_state[1]][r_mirror][0]
                    # save laser path
                    self.laser1vertical[curr_state[1]].append([r_mirror, curr_state[0]])
                    # update state
                    curr_state = [r_mirror, curr_state[1], direction]
            elif curr_state[2] == 2:    # going left
                # look in mirrors_horizontal to find largest col < curr_state[1]
                c_mirror = self.binary_search_mirrors(curr_state[1], self.mirrors_horizontal[curr_state[0]], 0)
                if c_mirror == -1:  # not found
                    c_mirror = 0
                    # save laser path
                    self.laser1horizontal[curr_state[0]].append([c_mirror, curr_state[1]])
                    return 1
                else:
                    direction = 3-self.mirrors_horizontal[curr_state[0]][c_mirror][1]*2
                    c_mirror = self.mirrors_horizontal[curr_state[0]][c_mirror][0]
                    # save laser path
                    self.laser1horizontal[curr_state[0]].append([c_mirror, curr_state[1]])
                    # update state
                    curr_state = [curr_state[0], c_mirror, direction]
            elif curr_state[2] == 3:    # going down
                # look in mirrors_vertical to find smallest row > curr_state[0]
                r_mirror = self.binary_search_mirrors(curr_state[0], self.mirrors_vertical[curr_state[1]], 1)
                if r_mirror == -1:  # not found
                    r_mirror = self.R+1
                    # save laser path
                    self.laser1vertical[curr_state[1]].append([curr_state[0], r_mirror])
                    return 1
                else:
                    direction = 2-self.mirrors_vertical[curr_state[1]][r_mirror][1]*2
                    r_mirror = self.mirrors_vertical[curr_state[1]][r_mirror][0]
                    # save laser path
                    self.laser1vertical[curr_state[1]].append([curr_state[0], r_mirror])
                    # update state
                    curr_state = [r_mirror, curr_state[1], direction]
            
    # sort laser 1 paths
    def sort_paths(self):
        for r in range(1,self.R+1):
            self.laser1horizontal[r].sort()
        for c in range(1,self.C+1):
            self.laser1vertical[c].sort()
    
    # binary search in hashtable, find out if idx is between any of the ranges in pathranges
    def binary_search_intersect(self, idx, pathranges):
        first = 0
        last = len(pathranges)-1
        found = 0
	
        while first<=last and not found:
            midpoint = (first + last)//2
            if pathranges[midpoint][0] < idx and pathranges[midpoint][1] > idx:
                found = 1
            else:
                if idx < pathranges[midpoint][0]:
                    last = midpoint-1
                elif idx > pathranges[midpoint][1]:
                    first = midpoint+1
                else:   # at end points
                    return 0
        return found
    
    # walk laser 2 through case, save intersections with laser 1
    # return # of intersections
    def laser2go(self):
        k = 0
        # r, c, direction: 0 - right, 1 - up, 2 - left, 3 - down, 4 - done
        curr_state = [self.R, self.C+1, 2]
        while curr_state[2] != 4:
            if curr_state[2] == 0:  # going right
                # look in mirrors_horizontal to find smallest col > curr_state[1]
                c_mirror = self.binary_search_mirrors(curr_state[1], self.mirrors_horizontal[curr_state[0]], 1)
                if c_mirror == -1:  # not found
                    direction = 4
                    c_mirror = self.C+1
                else:
                    direction = self.mirrors_horizontal[curr_state[0]][c_mirror][1]*2+1
                    c_mirror = self.mirrors_horizontal[curr_state[0]][c_mirror][0]
                # look up laser1vertical for intersections
                for c in range(curr_state[1]+1, c_mirror):
                    rows = self.laser1vertical[c]
                    if self.binary_search_intersect(curr_state[0], rows):
                        self.intersect[c].append(curr_state[0])
                        k += 1
                # update state
                curr_state = [curr_state[0], c_mirror, direction]
            elif curr_state[2] == 1:    # going up
                # look in mirrors_vertical to find largest row < curr_state[0]
                r_mirror = self.binary_search_mirrors(curr_state[0], self.mirrors_vertical[curr_state[1]], 0)
                if r_mirror == -1:  # not found
                    direction = 4
                    r_mirror = 0
                else:
                    direction = self.mirrors_vertical[curr_state[1]][r_mirror][1]*2
                    r_mirror = self.mirrors_vertical[curr_state[1]][r_mirror][0]
                # look up laser1horizontal for intersections
                for r in range(r_mirror+1, curr_state[0]):
                    cols = self.laser1horizontal[r]
                    if self.binary_search_intersect(curr_state[1], cols):
                        self.intersect[curr_state[1]].append(r)
                        k += 1
                # update state
                curr_state = [r_mirror, curr_state[1], direction]
            elif curr_state[2] == 2:    # going left
                # look in mirrors_horizontal to find largest col < curr_state[1]
                c_mirror = self.binary_search_mirrors(curr_state[1], self.mirrors_horizontal[curr_state[0]], 0)
                if c_mirror == -1:  # not found
                    direction = 4
                    c_mirror = 0
                else:
                    direction = 3-self.mirrors_horizontal[curr_state[0]][c_mirror][1]*2
                    c_mirror = self.mirrors_horizontal[curr_state[0]][c_mirror][0]
                # look up laser1vertical for intersections
                for c in range(c_mirror+1, curr_state[1]):
                    rows = self.laser1vertical[c]
                    if self.binary_search_intersect(curr_state[0], rows):
                        self.intersect[c].append(curr_state[0])
                        k += 1
                # update state
                curr_state = [curr_state[0], c_mirror, direction]
            elif curr_state[2] == 3:    # going down
                # look in mirrors_vertical to find smallest row > curr_state[0]
                r_mirror = self.binary_search_mirrors(curr_state[0], self.mirrors_vertical[curr_state[1]], 1)
                if r_mirror == -1:  # not found
                    direction = 4
                    r_mirror = self.R+1
                else:
                    direction = 2-self.mirrors_vertical[curr_state[1]][r_mirror][1]*2
                    r_mirror = self.mirrors_vertical[curr_state[1]][r_mirror][0]
                # look up laser1horizontal for intersections
                for r in range(curr_state[0]+1, r_mirror):
                    cols = self.laser1horizontal[r]
                    if self.binary_search_intersect(curr_state[1], cols):
                        self.intersect[curr_state[1]].append(r)
                        k += 1
                # update state
                curr_state = [r_mirror, curr_state[1], direction]
        return k
    
    # find smallest (r, c) by lexicographical order
    def smallest_rc(self):
        for c in range(1, self.C+1):
            col = self.intersect[c]
            if len(col) > 0:
                col.sort()
                return col[0], c
    
    # analyze the case:
    # 0 if no need for mirror
    # k, r, c if need one mirror: k - #possibilities; r, c - row & col of lowest position
    # impossible if no possible solution
    def analyze(self):
        if self.laser1go() == 0:
            return "0"
        # else, run laser 2, find intersections with laser 1
        self.sort_paths()
        k = self.laser2go()
        if k == 0:
            return "impossible"
        # have intersections, find the smallest one
        r, c = self.smallest_rc()
        return str(k)+" "+str(r)+" "+str(c)


if __name__ == "__main__":
    # read cases
    filename = 'sample.txt'
    f = open(filename, "r")
    CaseList = []   # list of cases
    case = None     # current case
    for line in f:
        tokens = line.split()
        if len(tokens) == 4:    # new case
            if case != None:
                case.sort_mirrors()
                CaseList.append(case)
            R = int(tokens[0])
            C = int(tokens[1])
            M = int(tokens[2])
            N = int(tokens[3])
            m = 0
            case = Case(R, C)
        elif len(tokens) == 2:
            r = int(tokens[0])
            c = int(tokens[1])
            if m < M:
                case.add_mirror(r, c, 0)   # 0 for / mirror
                m += 1
            else:
                case.add_mirror(r, c, 1)   # 1 for \ mirror
    case.sort_mirrors()
    CaseList.append(case)
    
    # analyze each case
    for i in range(len(CaseList)):
        case = CaseList[i]
        result = case.analyze() 
        print("Case " + str(i) + ": " + result)