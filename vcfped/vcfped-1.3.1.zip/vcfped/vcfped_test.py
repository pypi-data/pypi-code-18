import os
import os.path
import sys
import vcfped
# TODO: check -v parameter, if variables are among *available* variables.
# TODO: include pairwise thresholds in output

trueG = ["Male", "Male", "Female"]
trueP = ["Parent-child", "Parent-child"]
trueT = ["Regular trio"]

basic_command = "python ../vcfped.py ../testfiles/trioHG002_22X.vcf -o test "

def setup():
    if not os.path.exists("TEMP"): 
        os.mkdir("TEMP")
    os.chdir("TEMP")
    
def cleanup():
    if not os.getcwd().endswith("TEMP"): return
    os.chdir("..")
    for f in os.listdir("TEMP"):
        os.remove("TEMP/" + f)
    os.rmdir("TEMP")

def testG():
    with open("test.gender", 'r') as inf:
        g = [line.strip().split('\t')[7] for line in inf][1:]
    if g != trueG: 
        raise RuntimeError("Gender test failed!\nExpected: %s\nGot: %s" %(trueG, g))
    
def testP():
    with open("test.pair", 'r') as inf:
        p = [line.strip().split('\t')[9] for line in inf][1:]
    if p != trueP: 
        raise RuntimeError("Pairwise test failed!\nExpected: %s\nGot: %s" %(trueP, p))
        
def testT():
    with open("test.trio", 'r') as inf:
        t = [line.strip().split('\t')[10] for line in inf][1:]
    if t != trueT: 
        raise RuntimeError("Trio test failed!\nExpected: %s\nGot: %s" %(trueT, t))
    
def test(parameters):
    print parameters
    w = os.system(basic_command + parameters)
    if not '-ped' in parameters: 
        testG(); testP(); testT()
    
setup()
try:
    #tt = vcfped.vcfped("../testfiles/trioHG002_22X.vcf", pedfile="../testfiles/trio.ped")
    #if not tt: sys.exit()
    #test("")
    #test("-ped ../testfiles/trio.ped")

    with open("testped.ped", 'w') as p:
        p.write("1\tHG002\tHG003\tHG004\t1\n1\tHG003\t0\t0\t1\n1\tHG004\t0\t0\t2\n1\tHG004\t0\t0\t2")
    #test("-ped testped.ped")

    test("-ped ../testfiles/trio.ped -v AD -male 0 -t1 95")
    test("-ped ../testfiles/trio.ped -v AD -male 0 -t1 95 --all")
    #test("-v QUAL")
    #test("-v DP GQ")
    #test("-e 1000")
except Exception as e:
    print e
    sys.exit()
        

print "All test passed"

cleanup()




    