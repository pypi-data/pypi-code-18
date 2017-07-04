import os

class HTML:

	path     = ""
	bodyCode = ""
	htmlCode = r'<!DOCTYPE html><Html><Head><Title>CodeInfo</Title></Head><Body>'+bodyCode+'</Body></Html>'

	def setPath(self,path):
		self.path = path

	
	def h(self,text,color,bgcolor):
		code = (r'<h2 style="color:{0}; background:{1}; text-align:center; font-weight:BOLD;">'+str(text)+'</h3>').format(color,bgcolor)
		self.bodyCode = self.bodyCode + code	


	def p(self,text,color,bgcolor):
		code = (r'<p style="color:{0}; background:{1}; font-weight:BOLD;">'+str(text)+'</p>').format(color,bgcolor)
		self.bodyCode = self.bodyCode + code


	def img(self,src):		
		code = (r'<iframe src="{0}" width="100%" height="400px"></iframe>'.format(src))
		self.bodyCode = self.bodyCode + code

	
	def table(self,theadDataList,tbodyDataList,rowCount,color,bgcolor,theight):

		colData = ""
		tbodyData = ""

		for item in theadDataList:
			colData = colData + str((r'<td style="background:{1}; color:{0}; text-align:center;">{2}</td>').format(color,bgcolor,item))

		theadData = r'<tr>{0}</tr>'.format(colData)


		for i in range(rowCount):
			colData = ""
			for item in tbodyDataList[i]:
				colData = colData + str((r'<td style="background:{1}; color:{0}; text-align:center;">{2}</td>').format(color,bgcolor,item))

			tbodyData = tbodyData + r'<tr>{0}</tr>'.format(colData)

			
		code = (r'<Table style="width:100%; height:{2};  border: 5px solid rgb(50,55,84);"><thead>{0}</thead><tbody>{1}</tbody></Table>').format(theadData,tbodyData,theight) 
		self.bodyCode = self.bodyCode + code



	def makeFile(self):
		
		self.path = os.path.join(self.path,'codeinfo.html')

		with open(self.path,'w') as f:
			f.write(self.bodyCode)		