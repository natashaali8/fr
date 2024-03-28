import requests
import random,string,re
from bs4 import BeautifulSoup as parser
import aiohttp,asyncio
from urllib.parse import unquote
class Polls:
	def get_list(self,session,cookie,qid):
		with session.get(f"https://mbasic.facebook.com/questions.php?question_id={qid}",cookies={'cookie':cookie}) as response:
			options_id,link=None,None
			html           = parser(response.text,'html.parser')
			try:
				link       = "https://mbasic.facebook.com"+str(html.find('div',{'id':f'text{qid}'}).findAll('a')[-1:][0]['href']).replace('start=5','start=0').replace('num_options=5','num_options=1000')
				options_id = re.search(f'option_ids=(.*?)&',unquote(response.text)).group(1).split(',')
			except:options_id,link=None,None
			jsond     = {'status':'ok','data':[]}
			if link == None:
				try:
					htmlx = parser(response.text,'html.parser').find('div',{'id':f'text{qid}'}).findAll('div')
					options_id = re.findall('id="(\d+)"',str(htmlx))
					for oid in options_id:
						html2  = parser(response.text,'html.parser').find('div',{'id':oid})
						name   = html2.find('div').get('title')
						votes  = html2.findAll('div')[-1:][0].text
						jsond['data'].append({'oid':oid,'name':name,'votes':votes})
					return jsond
				except:return{'status':'bad'}
			else:
				try:
					with session.get(link,cookies={'cookie':cookie}) as response2:
						for oid in options_id:
							html2 = parser(response2.text,'html.parser').find('div',{'id':oid})
							name  = html2.find('div').get('title')
							votes = html2.findAll('div')[-1:][0].text
							jsond['data'].append({'oid':oid,'name':name,'votes':votes})
						return jsond
				except:return{'status':'bad'}
	def get_options_names(self,cookie,qid):
		with requests.Session() as session:
			session.headers.update({"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","cookie":cookie,"accept-language": "en-US,en;q=0.9","save-data": "on","user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36","sec-ch-ua": "\"Google Chrome\";v=\"112\", \"Chromium\";v=\"112\", \"Not=A?Brand\";v=\"24\"","sec-ch-ua-mobile": "?1","sec-ch-ua-platform": "\"Android\"","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","referrerPolicy": "strict-origin-when-cross-origin"})
			data = self.get_list(session,cookie,qid)
			return data
	async def fetch_data(self,session,cookie,pid,qid,oid):
		async with session.get(f'https://web.facebook.com/{qid}') as responses:
			session.headers.update({'referrer':f'{responses.url}'})
			response = await responses.text()
			jazoest=None;lsd=None;fb_dtsg=None
			try:
				jazoest=re.search("jazoest=(.*?)\"",response).group(1)
				lsd=re.search('\["LSD"\,\[\]\,\{"token":"(.*?)"\}',response).group(1)
				fb_dtsg=re.search('\["DTSGInitialData"\,\[\]\,\{"token":"(.*?)"\}',response).group(1)
			except:return {'status':'bad'}
			variable = {"input":{"is_tracking_encrypted":"true","option_id":oid,"question_id":qid,"tracking":[""],"actor_id":pid,"client_mutation_id":"1"},"scale":"1.5","__relay_internal__pv__IsWorkUserrelayprovider":"false"}
			return {
				'status':'ok',
				'lsd':lsd,
				'data':{
				'av':pid,
				'doc_id':'6673973972641117',
				'dpr':'1.5',
				'fb_api_caller_class':'RelayModern',
				'fb_api_req_friendly_name':'useCometPollAddVoteMutation',
				'fb_dtsg':fb_dtsg,
				'jazoest':jazoest,
				'qpl_active_flow_ids':'431626709',
				'fb_api_analytics_tags':'["qpl_active_flow_ids=431626709"]"',
				'lsd':lsd,
				'server_timestamps':'true',
				'variables':f'{variable}'}
			}
	async def vote(self,cookie,pid,qid,oid):
		async with aiohttp.ClientSession() as session:
			session.headers.update({"accept": "*/*","accept-language": "en-US,en;q=0.9","content-type": "application/x-www-form-urlencoded","dpr": "1.38125","save-data": "on","cookie":cookie,"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36","sec-ch-ua": "\"Google Chrome\";v=\"118\", \"Chromium\";v=\"118\", \"Not=A?Brand\";v=\"24\"","sec-ch-ua-mobile": "?0","sec-ch-ua-platform": "\"Windows\"","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","viewport-width": "523","x-asbd-id": "129477"})
			data = await self.fetch_data(session,cookie,pid,qid,oid)
			if data['status']=='bad':return {'status':'bad'}
			session.headers.update({"x-fb-friendly-name": "useCometPollAddVoteMutation"})
			session.headers.update({"x-fb-lsd": data['lsd']})
			session.headers.update({"referrerPolicy": "strict-origin-when-cross-origin"})
			async with session.post("https://web.facebook.com/api/graphql/",data=data['data']) as responses:
				response = await responses.text()
				if '"viewer_has_voted":true' in response:return {'status':'ok','pid':pid,'qid':qid,'target':oid}
				else:return {'status':'no','pid':pid,'qid':qid,'target':oid}
				
				
				
				
	
