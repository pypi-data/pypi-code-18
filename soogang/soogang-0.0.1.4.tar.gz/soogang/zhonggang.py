import io
import re
import xlsxwriter
import xlrd

spec_pattern = re.compile(u'(\d+(\.\d+)?)(-(\d+(\.\d+)?))?[*xX](\d+)([*xX][cC])?')

HEADER_ALIASES = {
    'category': [u'品种', u'品名'],
    'trademark': [u'牌号', u'材质'],
    'spec': [u'规格'],
    'steelwork': [u'产地', u'钢厂'],
    'price': [u'价格', u'报价', u'单价', u'挂牌价', u'过磅价', u'销售定价', u'销售价', u'含税价', '挂牌价格'],
    'price_range': ['议价幅度'],
    'skill_standard': ['技术标准'],
    'quality': ['质量等级'],
    'detail': ['资源详情'],
    'storage_number': ['仓储号', '库位号'],
    'warehouse_entry_time': ['入库时间'],

    'warehouse': [u'仓库', u'提货仓库'],

    'weight': [u'重量', u'吨位', u'吨重', u'卷重', u'件重', u'数量', u'可销量', u'可用量', u'可供量', u'可卖重量', u'开单量'],
    'package_code': [u'捆包号', u'卷号', u'板卷号'],

    'contract_code': [u'合同号', u'资源号', '钢厂资源号'],
    'comment': [u'备注', u'等级', u'卡号'],
    'measuring': ['计量方式']
}

REVERSED_HEADER_ALIAS = {}
for k, v in HEADER_ALIASES.items():
    for name in v:
        REVERSED_HEADER_ALIAS[name] = k

REQUIRED_HEADERS = {
    'category',
    'trademark',
    'spec',
}


class ResourceParser:
    def __init__(self, filename=None, file_contents=None):
        if filename:
            self.workbook = xlrd.open_workbook(filename=filename)
        else:
            self.workbook = xlrd.open_workbook(file_contents=file_contents)
        self.resources = []
        self.best_fits = []
        self.col_header_map = {}
        self.data_start = False

    def parse(self):
        for sheet in self.workbook.sheets():
            self.resources += self.parse_sheet(sheet)
            self.data_start = False

    def parse_sheet(self, sheet):
        resources = []
        for row in range(sheet.nrows):
            if not self.data_start:
                result = self.find_header_row(sheet, row)
                if result:
                    self.data_start = True
                else:
                    # 看下一行是否是header
                    continue
            else:
                resource = self.collect_resource(sheet, row)
                resources.append(resource)
        return resources

    def find_header_row(self, sheet, row):
        col_header_map = {}
        for col in range(sheet.ncols):
            v = self.cell(sheet, row, col)
            for key, names in HEADER_ALIASES.items():
                for name in names:
                    if name in ''.join(v.split()):
                        col_header_map[col] = key

        found_headers = set(col_header_map.values())

        current_fit = list(set(col_header_map.values()))

        # 必须的header头不齐全
        if not REQUIRED_HEADERS.issubset(found_headers):
            if len(current_fit) > len(self.best_fits):
                self.best_fits = current_fit
            # 不是合法的header row
            return False
        # 满足条件的header row, 设置header列的映射
        self.col_header_map = col_header_map
        return True

    def cell(self, sheet, row, col):
        return str(sheet.cell(row, col).value).strip()

    def collect_resource(self, sheet, row):
        res = {}
        for col in range(sheet.ncols):
            if col in self.col_header_map:
                key = self.col_header_map[col]
                val = self.cell(sheet, row, col)
                res[key] = val
        return res

    def export_to_standard_excel(self, filename=None):
        if not self.resources:
            missings = REQUIRED_HEADERS - set(self.best_fits)
            raise ValueError(f'资源单缺少表头 {missings}')
        f = io.BytesIO()
        if filename:
            workbook = xlsxwriter.Workbook(filename)
        else:
            workbook = xlsxwriter.Workbook(f, {'in_memory': True})
        headers = [
            '捆包号',
            '品名',
            '牌号',
            '规格',
            '产地',
            '重量',
            '提货仓库',
            '计量方式',
            '挂牌价格',
            '议价幅度',
            '技术标准',
            '质量等级',
            '资源详情',
            '仓储号',
            '入库时间',
            '钢厂资源号',
            '备注'
        ]
        worksheet = workbook.add_worksheet()
        # header_col_map = {v: k for k, v in self.col_header_map.items()}
        for i, header in enumerate(headers):
            worksheet.write(0, i, header)
        for i, resource in enumerate(self.resources):
            for j, header in enumerate(headers):
                col_name = REVERSED_HEADER_ALIAS[header]
                item = resource.get(col_name, '')
                worksheet.write(i + 1, j, item)

        workbook.close()
        if not filename:
            f.seek(0)
            return f.read()
