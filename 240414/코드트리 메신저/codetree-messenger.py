import heapq

N, Q = map(int, input().split())

list_100 = list(map(int, input().split())) # len: 2*N + 1

class chat():
    def __init__(self, i, p, d):
        self.i = i
        self.p = p # Num or -1
        self.d = d # Num or -1
        self.n = True
        self.c = set() # .add, .remove => O(1)

chat_list = [0] * (N+1) # len -> N => 0 ~ N

# Node 0
chat_list[0] = chat(0, -1, -1)

# TODO: Node가 순서대로 안 들어오는 경우?
for i in range(1, N+1): # Node 1 ~ N 
    chat_list[i] = chat(i, list_100[i], list_100[i+N])
for i in range(1, N+1):
    chat_list[list_100[i]].c.add(i)

def print_chat(): # 모든 채팅방 정보 확인
    global chat_list
    for i in chat_list:
        print(i.i, i.p, i.d, i.n, i.c)
    print()

def noti(i):
    global chat_list
    if chat_list[i].n:
        chat_list[i].n = False
    else:
        chat_list[i].n = True

def power(i, d):
    global chat_list
    chat_list[i].d = d

def swap(i, j):
    global chat_list
    i_p = chat_list[i].p
    j_p = chat_list[j].p
    chat_list[i].p, chat_list[j].p = j_p, i_p
    chat_list[i_p].c.remove(i)
    chat_list[i_p].c.add(j)
    chat_list[j_p].c.remove(j)
    chat_list[j_p].c.add(i)

def DFS(i, depth=1):
    global chat_list
    global cnt
    for c in chat_list[i].c:
        if chat_list[c].n:
            if chat_list[c].d >= depth:
                cnt += 1
            depth_tmp = depth + 1
            DFS(c, depth_tmp)
            
for _ in range(Q-1):
    i_list = list(map(int, input().split()))
    q = i_list[0]
    if q == 200:
        noti(i_list[1])
    elif q == 300:
        power(i_list[1], i_list[2])
    elif q == 400:
        swap(i_list[1], i_list[2])
    elif q == 500:
        cnt = 0
        DFS(i_list[1])
        print(cnt)