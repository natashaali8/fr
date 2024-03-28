import aiohttp,asyncio,re,brotli
import time
class DumpPages:
	async def fetchdata(self,session,cookie,idx):
		url=f'https://web.facebook.com/pages'
		headers={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'en-US,en;q=0.9',
		'dpr':'1.5',
		'save-data':'on',
		'sec-ch-prefers-color-scheme':'dark',
		'sec-ch-ua':'"Not)A;Brand";v="24", "Chromium";v="116"',
		'sec-ch-ua-full-version-list':'"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5845.54"',
		'sec-ch-ua-mobile':'?0',
		'sec-ch-ua-model':'""',
		'sec-ch-ua-platform':'"Linux"',
		'sec-ch-ua-platform-version':'""',
		'Sec-Fetch-Dest':'document',
		'Sec-Fetch-Mode':'navigate',
		'Sec-Fetch-Site':'same-origin',
		'Sec-Fetch-User':'?1',
		'cookie':cookie,
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
		'viewport-width':'891'}
		async with session.get(url,headers=headers) as responses:
			response = await responses.text()
			jazoest = None
			fb_dtsg = None
			lsd = None
			try:
				jazoest=re.search('jazoest=(.*?)"',response).group(1)
				lsd=re.search('\["LSD",\[\],\{"token":"(.*?)"',response).group(1)
				fb_dtsg=re.search('\["DTSGInitialData",\[\],{"token":"(.*?)"}',response).group(1)
			except AttributeError:
				return {
					'status':'bad',
					'cookie':'bad',
					'description':'invalid cookie or expired'
				}
			return {
				'data':{
				'av':idx,
				'doc_id':'6287151654667869',
				'dpr':'1.5',
				'fb_api_caller_class':'RelayModern',
				'fb_api_req_friendly_name':'CometSettingsDropdownTriggerQuery',
				'fb_dtsg':fb_dtsg,
				'jazoest':jazoest,
				'lsd':lsd,
				'qpl_active_flow_ids':'931594241',
				'server_timestamps':'true',
				'variables':'{"pageManagementNuxId":8191,"profileSwitcherNuxId":8150,"coreAppAdminProfileSwitcherNuxId":8189,"profileSwitcherAdminEducationNuxId":9348,"showNewToast":true}'
				},
				'lsd':lsd,
				'cookie':'ok',
				'status':'ok'
			}
	async def get_pages(self,cookie,idx):
		async with aiohttp.ClientSession() as session:
			data = await self.fetchdata(session,cookie,idx)
			if data['cookie']=='bad':
				return {
					'status':'bad',
					'cookie':'bad',
					'description':'Invalid cookie or Invalid post Id'
				}
			headers = {
			'Accept':'*/*',
			'Accept-Encoding':'gzip, deflate, br',
			'Accept-Language':'en-US,en;q=0.9',
			'Content-Type':'application/x-www-form-urlencoded',
			'dpr':'1.51861',
			'Origin':'https://web.facebook.com',
			'Referer':f'https://web.facebook.com/pages',
			'save-data':'on',
			'cookie':cookie,
			'sec-ch-prefers-color-scheme':'dark',
			'sec-ch-ua':'"Not)A;Brand";v="24", "Chromium";v="116"',
			'sec-ch-ua-full-version-list':'"Not)A;Brand";v="24.0.0.0", "Chromium";v="116.0.5845.54"',
			'sec-ch-ua-mobile':'?0',
			'sec-ch-ua-model':'""',
			'sec-ch-ua-platform':'"Linux"',
			'sec-ch-ua-platform-version':'""',
			'Sec-Fetch-Dest':'empty',
			'Sec-Fetch-Mode':'cors',
			'Sec-Fetch-Site':'same-origin',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
			'viewport-width':'891',
			'X-ASBD-ID':'129477',
			'X-FB-Friendly-Name':'CometSettingsDropdownTriggerQuery',
			'X-FB-LSD':data['lsd']
			}
			async with session.post('https://www.facebook.com/api/graphql/',headers=headers,data=data['data']) as responses2:
				pageList = []
				response2 = await responses2.text()
				if responses2.status==200:
					pages=re.findall('profile":{"id":"(.*?)"',response2)
					for page in pages:
						pageList.append(page)
					if len(pageList)==0:
						return {'status':'no'}
					else:
						return {'status':'ok','data':pageList},200
				else:
					return {'status':'no'}
		
