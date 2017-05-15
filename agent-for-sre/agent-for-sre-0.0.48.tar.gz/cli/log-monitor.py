#!/usr/bin/python3
# encoding: utf-8
import re
from agent_for_sre.Conf.ConfAnalyzer import ConfAnalyzer
from agent_for_sre.Monitor.Alert import Alert
from agent_for_sre.Monitor.LogMonitor import LogMonitor
from agent_for_sre.Tools.Es import Es
from agent_for_sre.Tools.Kafka import Kafka

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", required=True, help="输入yaml文件")
	parser.add_argument("-p", "--product", required=True, help="输入产品名")
	parser.add_argument("-r", "--rolename", required=True, help="输入监控定义策略名字")
	args = parser.parse_args()
	yamlfile=args.file
	product=args.product
	rolename=args.rolename

	conf_inst=ConfAnalyzer(yamlfile)
	data=conf_inst.getDataByL3(product,"monitor","log_monitor",rolename)

	logm_inst=LogMonitor(data)
	logm_inst.runMonitor()

