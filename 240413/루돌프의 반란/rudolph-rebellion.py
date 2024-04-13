from collections import defaultdict, deque
import copy

N, M, P, C, D = map(int, input().split())
num_snt = P
Map = [[0]*(N+1) for _ in range(N+1)]
Rr, Rc = map(int, input().split())
Map[Rr][Rc] = 999

class santa():
    def __init__(self, Pn, Sr, Sc):
        self.Pn = Pn
        self.Sr = Sr
        self.Sc = Sc
        self.scr = 0
        self.live = True # True, False, -2, -1

snt_lst = [0] * (P+1)

def print_map(Map):
    global N
    for i in range(1, N+1):
        print(Map[i][1:])
    print()

def dst(r1, c1, r2, c2):
    return (r1-r2)**2 + (c1-c2)**2

def move(who, r, c, dr, dc, dr_, dc_, crash=False):
    global N, snt_lst, Map, C, Rr, Rc, num_snt

    if crash==False:
        Map[r][c] = 0

    if not (0 < r+dr <= N) or not (0 < c+dc <= N): # 나갔을 때
        if 0 < who < 999: # 산타일 때
            snt_lst[who].live = False
            num_snt -= 1
            if num_snt == 0:
                return

    elif Map[r+dr][c+dc] == 0: # 안 나가고, 안 부딪힐 때
        Map[r+dr][c+dc] = who
        if 0 < who < 999: # 산타일 때
            snt_lst[who].Sr, snt_lst[who].Sc = r+dr, c+dc
        else:
            Rr, Rc = r+dr, c+dc

    else: # 안 나가고, 부딪힐 때
        new = Map[r+dr][c+dc]

        if new == 999: # 부딪힌 게 루돌프
            snt_lst[who].scr += D
            snt_lst[who].live = -2
            move(who, r+dr, c+dc, -dr*D, -dc*C, -dr_, -dc_, True)
        
        else: # 부딪힌 게 산타
            Map[r+dr][c+dc] = who
            if who == 999: # 온 애가 루돌프
                Rr, Rc = r+dr, c+dc
                snt_lst[new].scr += C
                snt_lst[new].live = -2
                move(new, r+dr, c+dc, dr*C, dc*C, dr_, dc_, True)
            elif 0 < who < 999: # 온 애가 산타
                snt_lst[who].Sr, snt_lst[who].Sc = r+dr, c+dc
                move(new, r+dr, c+dc, dr_, dc_, dr_, dc_, True)


for _ in range(P):
    Pn, Sr, Sc = map(int, input().split())
    snt_lst[Pn] = santa(Pn, Sr, Sc)
    Map[Sr][Sc] = Pn

r_dr = (1, 1, 1, 0, 0, -1, -1, -1)
r_dc = (1, 0, -1, 1, -1, 1, 0, -1)

s_dr = (0, 1, 0, -1)
s_dc = (-1, 0, 1, 0)

bool_print = False

for _ in range(M):
    Map_new = copy.deepcopy(Map)

    q = deque([])
    q.append((Rr, Rc))

    cnt_bool = True
    meet = []

    Map_new[Rr][Rc] = -1
    min_dst = -999

    while q:
        nr, nc = q.popleft()
        if Map_new[nr][nc] < min_dst:
            continue  
        for _ in range(8):
            n2r = nr+r_dr[_]
            n2c = nc+r_dc[_]
            if 0 < n2r <= N and 0 < n2c <= N:
                if 0 < Map_new[n2r][n2c] < 999: # 여기에 가장 가까운 산타 있음
                    if Map_new[nr][nc]-1 >= min_dst:
                        min_dst = Map_new[nr][nc]-1
                        meet.append((n2r, n2c))
                        Map_new[n2r][n2c] = Map_new[nr][nc]-1
                        cnt_bool = False
                        break
                elif cnt_bool == True and Map_new[n2r][n2c] == 0:
                    q.append((n2r, n2c))
                    Map_new[n2r][n2c] = Map_new[nr][nc]-1
    r_max = 0
    c_max = 0
    for m in meet:
        if m[0] > r_max:
            r_max = m[0]
            c_max = m[1]
        elif m[0] == r_max:
            if m[1] > c_max:
                c_max = m[1] 
    # crash
    dst_min = 999
    for _ in range(8):
        n2r = Rr+r_dr[_]
        n2c = Rc+r_dc[_]
        if dst(n2r, n2c, r_max, c_max) < dst_min:
            dst_min = dst(n2r, n2c, r_max, c_max)
            di = _

    move(999, Rr, Rc, r_dr[di], r_dc[di], r_dr[di], r_dc[di], False)
    if num_snt == 0:
        bool_print=True
        for i, st in enumerate(snt_lst[1:]):
            if i != P:
                print(st.scr, end=' ')
            else:
                print(st.scr)
    else:
        for st in snt_lst[1:]:
            di_tmp = False
            if st.live == True:
                dst2 = dst(Rr, Rc, st.Sr, st.Sc)
                for _ in range(4):
                    if 0 < st.Sr+s_dr[_] <= N and 0 < st.Sc+s_dc[_] <= N:
                        if Map[st.Sr+s_dr[_]][st.Sc+s_dc[_]] == 0 or Map[st.Sr+s_dr[_]][st.Sc+s_dc[_]] == 999:
                            dst_tmp = dst(Rr, Rc, st.Sr+s_dr[_], st.Sc+s_dc[_])
                            if dst_tmp <= dst2: # 나가는 경우 고려 x
                                di_tmp = _+1
                                dst2 = dst_tmp
                if di_tmp:
                    move(st.Pn, st.Sr, st.Sc, s_dr[di_tmp-1], s_dc[di_tmp-1], s_dr[di_tmp-1], s_dc[di_tmp-1], False)
                    if num_snt == 0:
                        bool_print=True
                        for i, st in enumerate(snt_lst[1:]):
                            if i != P:
                                print(st.scr, end=' ')
                            else:
                                print(st.scr)
                        break
            elif st.live == -2:
                st.live = -1
            elif st.live == -1:
                st.live = True
    for st in snt_lst[1:]:
        if st.live != False:
            st.scr += 1
            
if bool_print==False:
    for i, st in enumerate(snt_lst[1:]):
        if i != P:
            print(st.scr, end=' ')
        else:
            print(st.scr)