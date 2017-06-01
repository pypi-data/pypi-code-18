#!c:\bin\python27\python.exe
import sys
import pdfminer
import re

if pdfminer.__version__<'2013':
    VERSION = 1
    from pdfminer.pdfparser import PDFDocument, PDFParser
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
    from pdfminer.pdfdevice import PDFDevice, TagExtractor
    from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
    from pdfminer.cmapdb import CMapDB
    from pdfminer.layout import LAParams,LTContainer,LTText,LTTextBox,LTFigure,LTTextLineHorizontal
else:
    VERSION = 2
    from pdfminer.cmapdb import CMapDB
    from pdfminer.layout import LAParams,LTContainer,LTText,LTTextBox,LTFigure,LTTextLineHorizontal
    from pdfminer.pdfinterp import PDFResourceManager
    from pdfminer.converter import TextConverter
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfinterp import PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfpage import PDFTextExtractionNotAllowed

MARGIN = 0.3
MIN_MARGIN = 3

class Position:
    def __init__(self,x,y,w,h):
        self.x,self.y,self.w,self.h = x,y,w,h

    def __str__(self):
        return " x,y = ( %.0f, %.0f ) w,h = ( %.0f, %.0f )"%(self.x,self.y,self.w,self.h)

    __repr__=__str__;
        
    
    def center(self):
        return self.x+self.w/2, self.y + self.h/2

    def same_y(self,o):
        margin = max(MARGIN*self.h,MIN_MARGIN)
        result = ((self.y - margin) <= (o.y) and (o.y+o.h) <= (self.y+self.h+margin)) or \
            ((self.y - margin) >= (o.y) and (o.y+o.h) >= (self.y+self.h+margin))
        return result

    def __cmp__(self,o):
        if self.same_y(o):
            return cmp(self.x,o.x)
        return cmp(o.y,self.y) #smaller are at the bottom

class TextAnalyzer(TextConverter):
    def __init__(self,*args,**kwargs):
        TextConverter.__init__(self,*args,**kwargs)
        self.result = {}
        self.text = ''

    def write_text(self,text):
        self.text+=text

    def render(self,item):
        if isinstance(item,LTFigure):
             return
        if isinstance(item, LTContainer):
            for child in item:
                self.render(child)
        if isinstance(item, LTTextLineHorizontal):
            self.result.setdefault(self.pageno,[]).append((item.get_text(),
                                                           Position( item.x0,item.y1,item.width,item.height)))
        #elif isinstance(item, LTText):
        #    print item.get_text()
    
    def receive_layout(self, ltpage):
        if self.showpageno:
            self.write_text('Page %s\n' % ltpage.pageid)
        self.render(ltpage)
        #self.write_text('\f')
        return


def read_pdf(f,*pages_numbers):
    result = read_pdf_with_loc(f,*pages_numbers)
    return [i for (i,j) in result]

if VERSION == 1:
    def read_pdf_with_loc(f,*pages_numbers):
        caching = True
        codec = 'utf-8'
        rsrcmgr = PDFResourceManager(caching=caching)
        laparams = LAParams()
        laparams.all_texts = False
        device = TextAnalyzer(rsrcmgr, sys.stdout, codec=codec,laparams = laparams)
        process_pdf(rsrcmgr, device, f, pages_numbers or None,
                    caching=caching, check_extractable=True)
        device.close()
        for pagenumber in sorted(device.result):
            yield device.result[pagenumber]
else:
    def read_pdf_with_loc(fp,*page_numbers):
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        if not document.is_extractable:
                raise PDFTextExtractionNotAllowed
        rsrcmgr = PDFResourceManager()
        # Create a PDF device object.
        #device = PDFDevice(rsrcmgr)
        codec = 'utf-8'
        laparams = LAParams()
        laparams.all_texts = False
        device = TextAnalyzer(rsrcmgr, sys.stdout, codec=codec,laparams = laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
        device.close()
        for pagenumber in sorted(device.result):
            yield device.result[pagenumber]
    


def pdf_split_lines(page):
    for text,pos in page:
        if not text: continue
        lines = text.splitlines()
        if len(lines)>1: print '!!!OK!!!'
        new_h = pos.h/len(lines)
        for i,l in enumerate(lines):
            yield l,Position(pos.x,pos.y-i*new_h,pos.w,new_h)

class Line(object):
    def __init__(self,*el):
        self.l = []
        if el:
            self.add(*el)

    def add(self,text,pos):
        if text[-1]=='\n':
            text=text[:-1]
        spt = re.split('(  +)',text)
        charw = pos.w/len(text)
        self.l.append((pos,spt[0]))
        cumx = pos.x + len(spt[0])*charw
        for spaces,t in zip(spt[1::2],spt[2::2]):
            if not t.strip():
                continue
            cumx += len(spaces)*charw
            self.l.append((Position(cumx,pos.y,pos.w*len(t),pos.h),t))
            cumx += len(t)*charw
        

    def __getitem__(self,i):
        return self.l[i][1]

    def __len__(self):
        return len(self.l)

    def get_pos(self,i):
        return self.l[i][0]
    
    def sort(self):
        self.l.sort(key = lambda x:x[0].x)

    def as_list(self):
        return [i[1] for i in self.l]

    def get_result(self,with_pos):
        if with_pos:
            return self
        else:
            return self.as_list()

    def get_near_x(self,x,tol=10):
        for pos,text in self.l:
            if abs(pos.x-x)<=tol:
                return pos,text
        return None,None

    def __repr__(self):
        return "<line %s>"%([[i[0].x,i[1]] for i in self.l])

def reading_order(page,with_pos=False):
    line = Line()
    prev = None
    for text,pos in sorted(page,key=lambda x:x[1]):
        if prev and pos.same_y(prev):
            line.add(text,pos)
        else:
            line.sort()
            yield line.get_result(with_pos)
            line = Line(text,pos)
        prev = pos
    

if __name__ == '__main__':
    print 'start'
#print page.extractText()
    import sys 
    filename = sys.argv[1]
    for page in read_pdf_with_loc(open(filename,'rb')):
        print
        print '-'*10
        for line in reading_order(page):
            print line
                    
