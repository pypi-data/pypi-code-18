import sancomp
import numpy as np

resp = ""
resp2= ""
resp3= ""
resp4= ""


def read_core(self):
	nucleo=[]
	elasticidade=[]
	file = open('nucleo-elasticidade.dat')
	linha=file.readline()
	while(linha):
		nucleo.append(str(linha.split("	")[0]))
		elasticidade.append(float(linha.split("	")[1]))
		linha=file.readline()

def interpolate(v,x):
	v0 = [0.8333, 0.8333, 0.8333, 0.8333, 0.8333, 0.8333]
	v25 = [1, 0.8331, 0.8295, 0.7961, 0.6308, 0]
	v50 = [1, 0.8385, 0.8228, 0.7375, 0.4404, 0]

	def y(y0,y1,x0,x1,x):
		return y0+((y1-y0)*((x-x0)/(x1-x0)))
	
	if (v > 0.25) and (v < 0.5):
		if (x>2):
			f3=1
			return f3
		elif (x<2) and (x>1):
			f1 = y(v25[1],v50[1],0.25, 0.5,v)
			f2 = y(v25[2],v50[2],0.25,0.5,v)
			f3 = y(f1,f2,2,1,x)
			return f3
		elif (x<1) and (x>0.5):
			f1 = y(v25[2],v50[2],0.25,0.5,v)
			f2 = y(v25[3],v50[3],0.25,0.5,v)
			f3 = y(f1,f2,1,0.5,x)
			return f3
		elif (x<0.5) and (x>0.25):
			f1 = y(v25[3],v50[3],0.5,0.25,v)
			f2 = y(v25[4],v50[4],0.5,0.25,v)
			f3 = y(f1,f2,0.5,0.25,x)
			return f3
		elif (x<0.25) and (x>0):
			f1 = y(v25[4],v50[4],0.25,0,v)
			f2 = y(v25[5],v50[5],0.25,0,v)
			f3 = y(f1,f2,0.25,0,x)
			return f3
	else:
		if (x>2):
			f3=1
			return f3
		elif (x<2) and (x>1):
			f1 = y(v0[1],v25[1],0.25, 0.5,v)
			f2 = y(v0[2],v25[2],0.25,0.5,v)
			f3 = y(f1,f2,2,1,x)
			return f3
		elif (x<1) and (x>0.5):
			f1 = y(v0[2],v25[2],0.25,0.5,v)
			f2 = y(v0[3],v25[3],0.25,0.5,v)
			f3 = y(f1,f2,1,0.5,x)
			return f3
		elif (x<0.5) and (x>0.25):
			f1 = y(v0[3],v25[3],0.5,0.25,v)
			f2 = y(v0[4],v25[4],0.5,0.25,v)
			f3 = y(f1,f2,0.5,0.25,x)
			return f3
		elif (x<0.25) and (x>0):
			f1 = y(v0[4],v25[4],0.25,0,v)
			f2 = y(v0[5],v25[5],0.25,0,v)
			f3 = y(f1,f2,0.25,0,x)
			return f3

def beam(self, face,face_moduli,face_poisson, core, core_moduli, face_g, face_density, core_density, face_tensile, face_compressive, face_shear):
	
	#ef = str(sancomp.face[f])
	
	laminate_cb = str(self.cb_laminate.currentText())
	core_cb = str(self.cb_core.currentText())
	beam_cb = str(self.cb_beam.currentText())
	load = float(self.load.toPlainText())
	h = float(self.h.toPlainText())
	H = float(self.H.toPlainText())
	b = float(self.b.toPlainText())
	l = float(self.l.toPlainText())
		
	for f in range(len(face)):
		if str(face[f]) == str(laminate_cb):
			ef = float(face_moduli[f])
			if f > 11:
				g = float(face_g[f])
				v = float(face_poisson[f])
				density_face = float(face_density[f])
				shear = float(face_shear[f])
				tensile = float(face_tensile[f])
				compressive = float(face_compressive[f])
			else:
				g = ef/(2*(float(face_poisson[f] +1)))
				v = float(face_poisson[f])
				density_face = float(face_density[f])
				tensile = float(face_tensile[f])
				compressive = float(face_compressive[f])
				shear = tensile*0.5
	
				
	for c in range(len(core)):
		if str(core[c]) == str(core_cb):
			ec = float(core_moduli[c])
			density_core = float(core_density[c])
	
	
	#while(sancomp.face <> laminate_cb):
	#	pass
	#self.message.setText(""+sancomp.face[])
	global resp
	global resp2
	global resp3
	global resp4
	
	
	if (beam_cb == "Simple-Simple / Point"):
			
		Mmax = (load*l)/4
		Qmax = load/2
		
		#H = H do nucleo nas formulas que deveria ser Hn entao o Hmedio ("d"), sera:
		d=(h+H)/2
		#H na verdade eh H da viga inteira entao, atualizando H para ser a altura do nucleo, fica:
		
		H = H-h
				
		Dv = (ef*((b*h**3)/6))+(ef*((b*h*d**2)/2))+(ec*((b*H**3)/12))
		
		k = (load/(2*Dv))		
		
		NormalFaceStrenght = (Mmax/Dv)*ef
		NormalCoreStrenght = (Mmax/Dv)*ec
		
				
		a = (b*(H+2*h))
		
		r = H/b
				
		Tal_f_max = (load*h*d)*ef/2*Dv
		
		Tal_c_max = k*((ef*h*d)+(ec*((H**2)/2)))
		
							
		kz = interpolate(v,r)
				
		w = ((load*l**3)/(48*Dv))+((load*l)/(kz*4*a*g))
		
		cstress = NormalFaceStrenght*(-1) 
		
		
		total_density = ((2*h*density_face)/(H*b*l)) + (((H-2*h)*density_core)/(H*b*l))
		
		
		FS_tensile = tensile/NormalFaceStrenght
		FS_shear = shear/Tal_f_max
		
		IF_tensile = FS_tensile**(-1)
		if IF_tensile <1:
			self.fs_msg.setStyleSheet('color: blue')
			IF_msg = "Project approved!"
		else:
			self.fs_msg.setStyleSheet('color: red')
			IF_msg = "Project failed!"
		
		Mmax = round(Mmax,1)
		Qmax = round(Qmax,1)
		Dv = round(Dv,1)
		NormalFaceStrenght = round(NormalFaceStrenght,1)
		NormalCoreStrenght = round(NormalCoreStrenght,1)
		Tal_f_max = round(Tal_f_max,1)
		Tal_c_max = round(Tal_c_max,1)
		w = round(w,1)
		total_density = round(total_density,1)
		
		resp = "Mmax (N.mm) = " +str(Mmax) +"\n"+"Qmax (N) = " +str(Qmax) +"\n" + "Dsandwich (MPa) = " +str(Dv) +"\n"+"Tensile Stress (MPa) = "+str(NormalFaceStrenght)+"\n"+"Compression Stress (MPa) = "+str(cstress)+"\n"+"Normal Core Stress (MPa)= "+str(NormalCoreStrenght)+"\n"+"Face Shear Stress (MPa) = "+str(Tal_f_max)+"\n"+"Core Shear Stress (MPa) = "+str(Tal_c_max)+"\n"+"Deflexion (mm) = "+str(w)+"\n"+"Sandwich Density (Kg/m^3)= "+str(total_density)+"\n"+"\n"+"Factor of Safety = "+str(FS_tensile)+"\n"
		resp4 = "Load (N) = "+str(load)+"\n"+"Face Youngs Modulus (MPa) = "+str(ef)+"\n"+"Core Youngs Modulus (MPa) = "+str(ec)+"\n"+"Tensile Strenght (MPa) = "+str(tensile)+"\n"+"Compressive Strenght (MPa) = "+str(compressive)+"\n"+"Shear Strenght (MPa) = "+str(shear)+"\n"+"Face Density (Kg/m^3) = "+str(density_face)+"\n"+"Core Density (Kg/m^3) = "+str(density_core)
		resp3 = "\n"+"\n"+"\n"+"GEOMETRY (mm)"+"\n"+"\n"+"h = "+str(h)+"\n"+"H = "+str(H)+"\n"+"b = "+str(b)+"\n"+"L = "+str(l)
		resp2 = resp4+resp3
		
		self.resultado.setText(resp)
		self.resultado_2.setText(resp2)
		self.fs_msg.setText(IF_msg)
				
	elif beam_cb == "Simple-Simple / Uniform":
		
		Mmax = (load*l**2)/8
		Qmax = (load*l)/2			
		#H = H do nucleo nas formulas que deveria ser Hn entao o Hmedio ("d"), sera:
		d=(h+H)/2
		#H na verdade eh H da viga inteira entao, atualizando H para ser a altura do nucleo, fica:
		
		H = H-h				
		Dv = (ef*((b*h**3)/6))+(ef*((b*h*d**2)/2))+(ec*((b*H**3)/12))				
		k = (load/(2*Dv))				
		NormalFaceStrenght = (Mmax/Dv)*ef
		NormalCoreStrenght = (Mmax/Dv)*ec				
		a = (b*d**2)/H		
		r = H/b				
		Tal_f_max = (load*h*d)*ef/2*Dv		
		Tal_c_max = k*((ef*h*d)+(ec*((H**2)/2)))						
		kz = interpolate(v,r)				
		w = ((5*load*l**4)/(384*Dv))+((load*l**2)/(kz*8*a*g))		
		cstress = NormalFaceStrenght*(-1)		
		total_density = ((2*h*density_face)/(H*b*l)) + (((H-2*h)*density_core)/(H*b*l))		
		FS_tensile = tensile/NormalFaceStrenght
		FS_shear = shear/Tal_f_max		
		IF_tensile = FS_tensile**(-1)
		if IF_tensile <1:
			self.fs_msg.setStyleSheet('color: blue')
			IF_msg = "Project approved!"
		else:
			self.fs_msg.setStyleSheet('color: red')
			IF_msg = "Project failed!"		
		Mmax = round(Mmax,1)
		Qmax = round(Qmax,1)
		Dv = round(Dv,1)
		NormalFaceStrenght = round(NormalFaceStrenght,1)
		NormalCoreStrenght = round(NormalCoreStrenght,1)
		Tal_f_max = round(Tal_f_max,1)
		Tal_c_max = round(Tal_c_max,1)
		w = round(w,3)
		total_density = round(total_density,1)
		
		resp = "Mmax (N.mm) = " +str(Mmax) +"\n"+"Qmax (N) = " +str(Qmax) +"\n" + "Dsandwich (MPa) = " +str(Dv) +"\n"+"Tensile Stress (MPa) = "+str(NormalFaceStrenght)+"\n"+"Compression Stress (MPa) = "+str(cstress)+"\n"+"Normal Core Stress (MPa)= "+str(NormalCoreStrenght)+"\n"+"Face Shear Stress (MPa) = "+str(Tal_f_max)+"\n"+"Core Shear Stress (MPa) = "+str(Tal_c_max)+"\n"+"Deflexion (mm) = "+str(w)+"\n"+"Sandwich Density (Kg/m^3)= "+str(total_density)+"\n"+"\n"+"Factor of Safety = "+str(FS_tensile)+"\n"
		resp4 = "Load (N) = "+str(load)+"\n"+"Face Youngs Modulus (MPa) = "+str(ef)+"\n"+"Core Youngs Modulus (MPa) = "+str(ec)+"\n"+"Tensile Strenght (MPa) = "+str(tensile)+"\n"+"Compressive Strenght (MPa) = "+str(compressive)+"\n"+"Shear Strenght (MPa) = "+str(shear)+"\n"+"Face Density (Kg/m^3) = "+str(density_face)+"\n"+"Core Density (Kg/m^3) = "+str(density_core)
		resp3 = "\n"+"\n"+"\n"+"GEOMETRY (mm)"+"\n"+"\n"+"h = "+str(h)+"\n"+"H = "+str(H)+"\n"+"b = "+str(b)+"\n"+"L = "+str(l)
		resp2 = resp4+resp3
		
		self.resultado.setText(resp)
		self.resultado_2.setText(resp2)
		self.fs_msg.setText(IF_msg)
		
	elif beam_cb == "Free-Fixed / Point":
		
		Mmax = load*l	
		Qmax = load
		
			
		#H = H do nucleo nas formulas que deveria ser Hn entao o Hmedio ("d"), sera:
		d=(h+H)/2
		#H na verdade eh H da viga inteira entao, atualizando H para ser a altura do nucleo, fica:
		
		H = H-h
				
		Dv = (ef*((b*h**3)/6))+(ef*((b*h*d**2)/2))+(ec*((b*H**3)/12))
				
		k = (load/(2*Dv))
				
				
		NormalFaceStrenght = (Mmax/Dv)*ef
		NormalCoreStrenght = (Mmax/Dv)*ec
		
				
		a = (b*d**2)/H
		
		r = H/b
				
		Tal_f_max = (load*h*d)*ef/2*Dv
		
		Tal_c_max = k*((ef*h*d)+(ec*((H**2)/2)))
		
							
		kz = interpolate(v,r)
				
		w = ((load*l**3)/(3*Dv))+((load*l)/(kz*a*g))
		
		cstress = NormalFaceStrenght*(-1)
		
		
		total_density = ((2*h*density_face)/(H*b*l)) + (((H-2*h)*density_core)/(H*b*l))
		
		
		FS_tensile = tensile/NormalFaceStrenght
		FS_shear = shear/Tal_f_max
		
		IF_tensile = FS_tensile**(-1)
		if IF_tensile <1:
			self.fs_msg.setStyleSheet('color: blue')
			IF_msg = "Project works!"
		else:
			self.fs_msg.setStyleSheet('color: red')
			IF_msg = "Project cracks!"
		
		Mmax = round(Mmax,1)
		Qmax = round(Qmax,1)
		Dv = round(Dv,1)
		NormalFaceStrenght = round(NormalFaceStrenght,1)
		NormalCoreStrenght = round(NormalCoreStrenght,1)
		Tal_f_max = round(Tal_f_max,1)
		Tal_c_max = round(Tal_c_max,1)
		w = round(w,1)
		total_density = round(total_density,1)
		
		resp = "Mmax (N.mm) = " +str(Mmax) +"\n"+"Qmax (N) = " +str(Qmax) +"\n" + "Dsandwich (MPa) = " +str(Dv) +"\n"+"Tensile Stress (MPa) = "+str(NormalFaceStrenght)+"\n"+"Compression Stress (MPa) = "+str(cstress)+"\n"+"Normal Core Stress (MPa)= "+str(NormalCoreStrenght)+"\n"+"Face Shear Stress (MPa) = "+str(Tal_f_max)+"\n"+"Core Shear Stress (MPa) = "+str(Tal_c_max)+"\n"+"Deflexion (mm) = "+str(w)+"\n"+"Sandwich Density (Kg/m^3)= "+str(total_density)+"\n"+"\n"+"Factor of Safety = "+str(FS_tensile)+"\n"
		resp4 = "Load (N) = "+str(load)+"\n"+"Face Youngs Modulus (MPa) = "+str(ef)+"\n"+"Core Youngs Modulus (MPa) = "+str(ec)+"\n"+"Tensile Strenght (MPa) = "+str(tensile)+"\n"+"Compressive Strenght (MPa) = "+str(compressive)+"\n"+"Shear Strenght (MPa) = "+str(shear)+"\n"+"Face Density (Kg/m^3) = "+str(density_face)+"\n"+"Core Density (Kg/m^3) = "+str(density_core)
		resp3 = "\n"+"\n"+"\n"+"GEOMETRY (mm)"+"\n"+"\n"+"h = "+str(h)+"\n"+"H = "+str(H)+"\n"+"b = "+str(b)+"\n"+"L = "+str(l)
		resp2 = resp4+resp3
		
		self.resultado.setText(resp)
		self.resultado_2.setText(resp2)
		self.fs_msg.setText(IF_msg)
		
	elif beam_cb == "Free-Fixed / Uniform":
		
		Mmax = (load*l**2)/2
		
		Qmax = load*l
		
			
		#H = H do nucleo nas formulas que deveria ser Hn entao o Hmedio ("d"), sera:
		d=(h+H)/2
		#H na verdade eh H da viga inteira entao, atualizando H para ser a altura do nucleo, fica:
		
		H = H-h
				
		Dv = (ef*((b*h**3)/6))+(ef*((b*h*d**2)/2))+(ec*((b*H**3)/12))
				
		k = (load/(2*Dv))
				
				
		NormalFaceStrenght = (Mmax/Dv)*ef
		NormalCoreStrenght = (Mmax/Dv)*ec
		
				
		a = (b*d**2)/H
		
		r = H/b
				
		Tal_f_max = (load*h*d)*ef/2*Dv
		
		Tal_c_max = k*((ef*h*d)+(ec*((H**2)/2)))
		
							
		kz = interpolate(v,r)
				
		w = ((load*l**4)/(8*Dv))
		
		cstress = NormalFaceStrenght*(-1)
		
		
		total_density = ((2*h*density_face)/(H*b*l)) + (((H-2*h)*density_core)/(H*b*l))
		
		
		FS_tensile = tensile/NormalFaceStrenght
		FS_shear = shear/Tal_f_max
		
		IF_tensile = FS_tensile**(-1)
		if IF_tensile <1:
			self.fs_msg.setStyleSheet('color: blue')
			IF_msg = "Project works!"
		else:
			self.fs_msg.setStyleSheet('color: red')
			IF_msg = "Project cracks!"
		
		Mmax = round(Mmax,1)
		Qmax = round(Qmax,1)
		Dv = round(Dv,1)
		NormalFaceStrenght = round(NormalFaceStrenght,1)
		NormalCoreStrenght = round(NormalCoreStrenght,1)
		Tal_f_max = round(Tal_f_max,1)
		Tal_c_max = round(Tal_c_max,1)
		w = round(w,1)
		total_density = round(total_density,1)
		
		resp = "Mmax (N.mm) = " +str(Mmax) +"\n"+"Qmax (N) = " +str(Qmax) +"\n" + "Dsandwich (MPa) = " +str(Dv) +"\n"+"Tensile Stress (MPa) = "+str(NormalFaceStrenght)+"\n"+"Compression Stress (MPa) = "+str(cstress)+"\n"+"Normal Core Stress (MPa)= "+str(NormalCoreStrenght)+"\n"+"Face Shear Stress (MPa) = "+str(Tal_f_max)+"\n"+"Core Shear Stress (MPa) = "+str(Tal_c_max)+"\n"+"Deflexion (mm) = "+str(w)+"\n"+"Sandwich Density (Kg/m^3)= "+str(total_density)+"\n"+"\n"+"Factor of Safety = "+str(FS_tensile)+"\n"
		resp4 = "Load (N) = "+str(load)+"\n"+"Face Youngs Modulus (MPa) = "+str(ef)+"\n"+"Core Youngs Modulus (MPa) = "+str(ec)+"\n"+"Tensile Strenght (MPa) = "+str(tensile)+"\n"+"Compressive Strenght (MPa) = "+str(compressive)+"\n"+"Shear Strenght (MPa) = "+str(shear)+"\n"+"Face Density (Kg/m^3) = "+str(density_face)+"\n"+"Core Density (Kg/m^3) = "+str(density_core)
		resp3 = "\n"+"\n"+"\n"+"GEOMETRY (mm)"+"\n"+"\n"+"h = "+str(h)+"\n"+"H = "+str(H)+"\n"+"b = "+str(b)+"\n"+"L = "+str(l)
		resp2 = resp4+resp3
		
		self.resultado.setText(resp)
		self.resultado_2.setText(resp2)
		self.fs_msg.setText(IF_msg)
		
	elif beam_cb == "Fixed-Fixed / Point":
		
		Mmax = (load*l)/8
		
		Qmax = load/2
		
			
		#H = H do nucleo nas formulas que deveria ser Hn entao o Hmedio ("d"), sera:
		d=(h+H)/2
		#H na verdade eh H da viga inteira entao, atualizando H para ser a altura do nucleo, fica:
		
		H = H-h
				
		Dv = (ef*((b*h**3)/6))+(ef*((b*h*d**2)/2))+(ec*((b*H**3)/12))
				
		k = (load/(2*Dv))
				
				
		NormalFaceStrenght = (Mmax/Dv)*ef
		NormalCoreStrenght = (Mmax/Dv)*ec
		
				
		a = (b*d**2)/H
		
		r = H/b
				
		Tal_f_max = (load*h*d)*ef/2*Dv
		
		Tal_c_max = k*((ef*h*d)+(ec*((H**2)/2)))
		
							
		kz = interpolate(v,r)
				
		w = ((load*l**3)/(192*Dv))+((load*l)/(kz*4*a*g))
		
		cstress = NormalFaceStrenght*(-1)
		
		
		total_density = ((2*h*density_face)/(H*b*l)) + (((H-2*h)*density_core)/(H*b*l))
		
		
		FS_tensile = tensile/NormalFaceStrenght
		FS_shear = shear/Tal_f_max
		
		IF_tensile = FS_tensile**(-1)
		if IF_tensile <1:
			self.fs_msg.setStyleSheet('color: blue')
			IF_msg = "Project works!"
		else:
			self.fs_msg.setStyleSheet('color: red')
			IF_msg = "Project cracks!"
		
		Mmax = round(Mmax,1)
		Qmax = round(Qmax,1)
		Dv = round(Dv,1)
		NormalFaceStrenght = round(NormalFaceStrenght,1)
		NormalCoreStrenght = round(NormalCoreStrenght,1)
		Tal_f_max = round(Tal_f_max,1)
		Tal_c_max = round(Tal_c_max,1)
		w = round(w,1)
		total_density = round(total_density,1)
		
		resp = "Mmax (N.mm) = " +str(Mmax) +"\n"+"Qmax (N) = " +str(Qmax) +"\n" + "Dsandwich (MPa) = " +str(Dv) +"\n"+"Tensile Stress (MPa) = "+str(NormalFaceStrenght)+"\n"+"Compression Stress (MPa) = "+str(cstress)+"\n"+"Normal Core Stress (MPa)= "+str(NormalCoreStrenght)+"\n"+"Face Shear Stress (MPa) = "+str(Tal_f_max)+"\n"+"Core Shear Stress (MPa) = "+str(Tal_c_max)+"\n"+"Deflexion (mm) = "+str(w)+"\n"+"Sandwich Density (Kg/m^3)= "+str(total_density)+"\n"+"\n"+"Factor of Safety = "+str(FS_tensile)+"\n"
		resp4 = "Load (N) = "+str(load)+"\n"+"Face Youngs Modulus (MPa) = "+str(ef)+"\n"+"Core Youngs Modulus (MPa) = "+str(ec)+"\n"+"Tensile Strenght (MPa) = "+str(tensile)+"\n"+"Compressive Strenght (MPa) = "+str(compressive)+"\n"+"Shear Strenght (MPa) = "+str(shear)+"\n"+"Face Density (Kg/m^3) = "+str(density_face)+"\n"+"Core Density (Kg/m^3) = "+str(density_core)
		resp3 = "\n"+"\n"+"\n"+"GEOMETRY (mm)"+"\n"+"\n"+"h = "+str(h)+"\n"+"H = "+str(H)+"\n"+"b = "+str(b)+"\n"+"L = "+str(l)
		resp2 = resp4+resp3
		
		self.resultado.setText(resp)
		self.resultado_2.setText(resp2)
		self.fs_msg.setText(IF_msg)
		
	elif beam_cb == "Fixed-Fixed / Uniform":
		
		Mmax = (load*l**2)/12
		
		Qmax = load*l/2
		
			
		#H = H do nucleo nas formulas que deveria ser Hn entao o Hmedio ("d"), sera:
		d=(h+H)/2
		#H na verdade eh H da viga inteira entao, atualizando H para ser a altura do nucleo, fica:
		
		H = H-h
				
		Dv = (ef*((b*h**3)/6))+(ef*((b*h*d**2)/2))+(ec*((b*H**3)/12))
				
		k = (load/(2*Dv))
				
				
		NormalFaceStrenght = (Mmax/Dv)*ef
		NormalCoreStrenght = (Mmax/Dv)*ec
		
				
		a = (b*d**2)/H
		
		r = H/b
				
		Tal_f_max = (load*h*d)*ef/2*Dv
		
		Tal_c_max = k*((ef*h*d)+(ec*((H**2)/2)))
		
							
		kz = interpolate(v,r)
				
		w = ((load*l**3)/(48*Dv))+((load*l)/(kz*4*a*g))
		
		cstress = NormalFaceStrenght*(-1)
		
		
		total_density = ((2*h*density_face)/(H*b*l)) + (((H-2*h)*density_core)/(H*b*l))
		
		
		FS_tensile = tensile/NormalFaceStrenght
		FS_shear = shear/Tal_f_max
		
		IF_tensile = FS_tensile**(-1)
		if IF_tensile <1:
			self.fs_msg.setStyleSheet('color: blue')
			IF_msg = "Project works!"
		else:
			self.fs_msg.setStyleSheet('color: red')
			IF_msg = "Project cracks!"
		
		Mmax = round(Mmax,1)
		Qmax = round(Qmax,1)
		Dv = round(Dv,1)
		NormalFaceStrenght = round(NormalFaceStrenght,1)
		NormalCoreStrenght = round(NormalCoreStrenght,1)
		Tal_f_max = round(Tal_f_max,1)
		Tal_c_max = round(Tal_c_max,1)
		w = round(w,1)
		total_density = round(total_density,1)
		
		resp = "Mmax (N.mm) = " +str(Mmax) +"\n"+"Qmax (N) = " +str(Qmax) +"\n" + "Dsandwich (MPa) = " +str(Dv) +"\n"+"Tensile Stress (MPa) = "+str(NormalFaceStrenght)+"\n"+"Compression Stress (MPa) = "+str(cstress)+"\n"+"Normal Core Stress (MPa)= "+str(NormalCoreStrenght)+"\n"+"Face Shear Stress (MPa) = "+str(Tal_f_max)+"\n"+"Core Shear Stress (MPa) = "+str(Tal_c_max)+"\n"+"Deflexion (mm) = "+str(w)+"\n"+"Sandwich Density (Kg/m^3)= "+str(total_density)+"\n"+"\n"+"Factor of Safety = "+str(FS_tensile)+"\n"
		resp4 = "Load (N) = "+str(load)+"\n"+"Face Youngs Modulus (MPa) = "+str(ef)+"\n"+"Core Youngs Modulus (MPa) = "+str(ec)+"\n"+"Tensile Strenght (MPa) = "+str(tensile)+"\n"+"Compressive Strenght (MPa) = "+str(compressive)+"\n"+"Shear Strenght (MPa) = "+str(shear)+"\n"+"Face Density (Kg/m^3) = "+str(density_face)+"\n"+"Core Density (Kg/m^3) = "+str(density_core)
		resp3 = "\n"+"\n"+"\n"+"GEOMETRY (mm)"+"\n"+"\n"+"h = "+str(h)+"\n"+"H = "+str(H)+"\n"+"b = "+str(b)+"\n"+"L = "+str(l)
		resp2 = resp4+resp3
		
		self.resultado.setText(resp)
		self.resultado_2.setText(resp2)
		self.fs_msg.setText(IF_msg)
				
	
	self.tabWidget.setCurrentIndex(2)
	

if __name__ == '__main__':
	print "***********************************************************************"
	print "***********************************************************************"
	print "This module contains all the formulations used in calculations"
	print "***********************************************************************"
	print "***********************************************************************"