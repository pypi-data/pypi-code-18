import argparse
import sys

APP_DESC="""
命令:ptail1
"""

print(APP_DESC)
if len(sys.argv) == 1:
    sys.argv.append('--help')
parser = argparse.ArgumentParser()
parser.add_argument('-f',action="store_true",help='实时更新')
parser.add_argument('-n','-N',type=int,default=10,help='输出最后几行')
parser.add_argument('file',)
args = parser.parse_args()

print(args.file)
print(args.n)
print(args.f)

def ptail():
    with open(args.file, 'rt') as f:
        data = f.readlines()
        for x in data[0 - args.n:]:
            print(x, end='')

# if __name__ == "__main__":
#     ptail()
















# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         print('illegal!')
#     elif len(sys.argv) == 2:
#         ptail1(parone=sys.argv[1], parthree=10)
#     elif len(sys.argv) == 3:
#         ptail1(parone=sys.argv[1], partwo=sys.argv[2])
#     elif len(sys.argv) == 4:
#         if sys.argv[2] == '-N' or '-n':
#             ptail1(parone=sys.argv[1], parthree=int(sys.argv[3]))