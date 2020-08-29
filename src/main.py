# readfile "rf()" function
def rf(filename):
    return open(filename, "r").read()

# import external files
exec(rf("translate.py"))
exec(rf("parse.py"))
exec(rf("fileServer.py"))

# main body

# arg1 defines live server port
# main calling point of program
startServer(8000)