from flask import Flask,request,render_template
import asyncio
from Dumps import DumpPages
from facebookPolls import Polls
ts=1
app=Flask(__name__)
def approvals():
	return open('approvals.txt','r').read()
@app.route('/',methods=['GET'])
def home():
	return render_template('index.html')
@app.route('/getpages2',methods=['GET','POST'])
def getpages2():
	if request.args.get('cookie') and request.args.get('id') and request.args.get('token'):
		cookie = request.args.get('cookie')
		idx = request.args.get('id')
		token = request.args.get('token')
		if len(token)==32 and token in approvals():
			fb = DumpPages()
			return asyncio.run(fb.get_pages(cookie,idx))
		else:return {'status':'403','description':'Access denied!'},403
	else:return {'status':'403','description':'Access denied!'},403

@app.route('/pollnames',methods=['GET','POST'])
def pollnames():
	if request.args.get('cookie') and request.args.get('token') and request.args.get('qid'):
		cookie       = request.args.get('cookie')
		qid          = request.args.get('qid')
		token        = request.args.get('token')
		if len(token)==32 and token in approvals():
			fb       = Polls()
			return fb.get_options_names(cookie,qid)
		else:return {'status':'403','description':'Access denied!'},403
	else:return {'status':'403','description':'Access denied!'},403

@app.route('/vote',methods=['GET','POST'])
def vote():
	if request.args.get('cookie') and request.args.get('pid') and request.args.get('qid') and request.args.get('oid') and request.args.get('token'):
		cookie       = request.args.get('cookie')
		qid          = request.args.get('qid')
		token        = request.args.get('token')
		pid          = request.args.get('pid')
		oid          = request.args.get('oid')
		if len(token)==32 and token in approvals():
			fb       = Polls()
			return asyncio.run(fb.vote(cookie,pid,qid,oid))
		else:return {'status':'403','description':'Access denied!'},403
	else:return {'status':'403','description':'Access denied!'},403
if __name__ == '__main__':
	app.run(debug=False)
