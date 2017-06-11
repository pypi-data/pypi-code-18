_author_ = "Hongjian Tang"


tab_num = 0
text_output = [""]
config_sheet = None


def init_tab_num(par):
      global tab_num
      if tab_num is None:
            tab_num = par

def init_config_sheet(par):
      global config_sheet
      if config_sheet is None:
            config_sheet = par

def init_text_output( ):
      global text_output

# 
def new_print(par, file):
      par=str(par)
      global tab_num
      global text_output
      text_tab="    "
      for x in range(0, tab_num):
            file.write(text_tab)
      file.write(par)
      if not (par[len(par)-1] == "{" or par[len(par)-1] == ","):
            file.write(",\n")
      else:
            file.write("\n")

      text_output.append(par)
      for x in range(0, len(par)):
            if par[x] == "{":
                  tab_num = tab_num+1
            if par[x] == "}":
                  tab_num = tab_num-1
      
def get_price(par):
      global config_sheet
      par = str(par)
      function_output = 0
      # 查找对应物品的 价格      
      for n in range(1,config_sheet.max_row):
            if config_sheet.cell(row=n,column=4).value == par:
                  function_output = config_sheet.cell(row=n,column=5).value 
      return function_output
      
      
def get_server_name(par):
      global config_sheet
      par = str(par)
      function_output = 0
      # 查找对应物品的 后端名称      
      for n in range(1,config_sheet.max_row):
            if config_sheet.cell(row=n,column=4).value == par:
                  function_output = config_sheet.cell(row=n,column=6).value 
      return function_output
      
def get_client_name(par):
      global config_sheet
      par = str(par)
      function_output = 0
      # 查找对应物品的 前端名称      
      for n in range(1,config_sheet.max_row):
            if config_sheet.cell(row=n,column=4).value == par:
                  function_output = config_sheet.cell(row=n,column=2).value 
      return function_output

def get_server_reward(item_name, item_num):
      global config_sheet
      item_name = str(item_name)
      function_output = 0
      # 查找对应物品的 前端名称      
      for n in range(1,config_sheet.max_row):
            if config_sheet.cell(row=n,column=4).value == item_name:
                  function_output = str(config_sheet.cell(row=n,column=2).value) + "=" + str(item_num)
      return function_output

def get_vertical_client_reward(cell, space_count, name_col, num_col):
      while cell.offset(row=i, column=0) is not None:
            return 0