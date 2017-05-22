# 输入输出各种颜色的字体
from colors import color_msg
# 打印版本详情信息
from infos import printinfos
# 引入robot类
from robot import Robot


def main():
    printinfos()
    userName = input(color_msg('green', '👉   请输入您的姓名：'))
    robot = Robot(userName)
    chatString = input(color_msg('red', '👉   请输入您想说的的话（输入为空自动结束）：'))
    while chatString != '':
        print(color_msg('blue', '💁   ' + robot.Chatting(chatString)))
        chatString = input(color_msg('red', '👉   请输入您想说的的话（输入为空自动结束）：'))

main()
