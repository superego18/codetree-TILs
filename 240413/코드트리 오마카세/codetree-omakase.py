from collections import defaultdict

L, Q = map(int, input().split())

sushi = defaultdict(dict)
man = defaultdict(list)
photo = []

query = []


for _ in range(1,Q+1):
    args = [int(x) if x.isdigit() else x for x in input().split()]
    query.append((args[1], args[0]))
    if args[0] == 100:
        sushi[args[3]][args[1]] = args[2]
    elif args[0] == 200:
        man[args[3]] = [args[1], args[2], args[4]]
    else:
        photo.append(args[1])

for m in man:
    t_man = 0
    for s_t, s_x in sushi[m].items():
        s_t_old = s_t
        if man[m][0] > s_t:
            s_t = man[m][0]
            s_x = (s_x+(s_t-s_t_old))%L
        if s_x == man[m][1]:
            t_need = 0
        elif s_x < man[m][1]:
            t_need = man[m][1] - s_x
        else:
            t_need = L - s_x + man[m][1]

        query.append((t_need+s_t, 111))

        if t_need+s_t > t_man:
            t_man = t_need+s_t

    query.append((t_man, 222))

query.sort(key=lambda q: (q[0], q[1]))

people_num, sushi_num = 0, 0
for q in query:
    if q[1] == 100:  # 초밥 추가
        sushi_num += 1
    elif q[1] == 111:  # 초밥 제거
        sushi_num -= 1
    elif q[1] == 200:  # 사람 추가
        people_num += 1
    elif q[1] == 222:  # 사람 제거
        people_num -= 1
    else:  # 사진 촬영시 답을 출력하면 됩니다.
        print(people_num, sushi_num)