import re
import datefinder  # yyyy-mm-dd
from datetime import date as libdate
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
# dictionary for months to month-number
mon_dict = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
			'may': '05', 'jun': '06', 'jul': '07', 'june': '06', 'july': '07', 'aug': '08',
			'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}

# check if date is valid


def valid(matched_date):
	''' validate month,year and date '''
	[year, month, date] = matched_date
	today = list(str(libdate.today()).split('-'))
	try:
		if ((int(year) <= int(today[0]) and int(year) >= 1900) and (int(month) <= 12 and int(month) > 0) and
				(int(date) <= 31 and int(date) > 0)):
			return True
	except:
		return False

	return False

# regex based extraction


def date_forms(strn):
	''' Extract different possible date forms from input text'''
	strn = strn.lower()

	# different regular expression for different formats
	mon = 'jan|feb|mar|apr|may|jun|jul|june|july|aug|sep|oct|nov|dec'
	regex_str = [r'\b(?:' + mon + ').\d\d.\d\d',
				 r'\b(?:' + mon + ').\d\d.\d\d\d\d',
				 r'\b(?:' + mon + ').\d.\d\d\d\d',
				 r'\b(?:' + mon + ').\d.\d\d',
				 r'\d\d.\b(?:' + mon + ').\d\d\d\d',
				 r'\d\d.\b(?:' + mon + ').\d\d',
				 r'\d.\b(?:' + mon + ').\d\d\d\d',
				 r'\d.\b(?:' + mon + ').\d\d',
				 r'\b(?:' + mon + ').\d\d..\d\d\d\d',
				 r'\d\d.\d\d.\d\d\d\d',
				 r'\d\d.\d\d.\d\d',
				 r'\d\d.\d.\d\d\d\d',
				 r'\d\d.\d.\d\d',
				 r'\d.\d\d.\d\d\d\d',
				 r'\d.\d.\d\d\d\d',
				 r'\d.\d\d.\d\d',
				 r'\d.\d.\d\d',
				 ]
	# separate matched text in month,year and date and check for validity
	for regex in range(len(regex_str)):
		repn = regex_str[regex]
		date_v = re.findall(repn, strn)
		if date_v != []:
			if regex < 4:
				for dv in date_v:
					if dv[:3] in mon_dict:
						month = mon_dict[dv[:3]]
					else:
						continue
					if len(dv) <= 7:
						date = '0' + dv[-4:-3]
						year = '20' + dv[-2:]
					elif len(dv) == 8:
						date = dv[-5:-3]
						year = '20' + dv[-2:]
					else:
						date = dv[-7:-5]
						year = dv[-4:]

					if valid([year, month, date]):
						formatted_date = year + '-' + month + '-' + date
						return formatted_date

			elif regex == 4:
				for dv in date_v:
					if dv[3:5] in mon_dict:
						month = mon_dict[dv[3:5]]
					else:
						continue
					date = dv[:2]
					year = dv[-4:]
					if valid([year, month, date]):
						formatted_date = year + '-' + month + '-' + date
						return formatted_date
			elif regex == 5:
				for dv in date_v:
					if dv[3:5] in mon_dict:
						month = mon_dict[dv[3:5]]
					else:
						continue
					date = dv[:2]
					year = '20' + dv[-2:]
					if valid([year, month, date]):
						formatted_date = year + '-' + month + '-' + date
						return formatted_date
			elif regex == 6:
				for dv in date_v:
					if dv[2:5] in mon_dict:
						month = mon_dict[dv[2:5]]
					else:
						continue
					date = '0' + dv[:1]
					year = dv[-4:]
					if valid([year, month, date]):
						formatted_date = year + '-' + month + '-' + date
						return formatted_date
			elif regex == 7:
				for dv in date_v:
					if dv[2:5] in mon_dict:
						month = mon_dict[dv[2:5]]
					else:
						continue
					date = '0' + dv[:1]
					year = '20' + dv[-2:]
					if valid([year, month, date]):
						formatted_date = year + '-' + month + '-' + date
						return formatted_date
			elif regex == 8:
				for dv in date_v:
					if dv[:3] in mon_dict:
						month = mon_dict[dv[:3]]
					else:
						continue
					date = dv[-8:-6]
					year = dv[-4:]
					if valid([year, month, date]):
						formatted_date = year + '-' + month + '-' + date
						return formatted_date
			elif regex > 8:
				#				date_val.append([date_v, repn])
				for x in date_v:
					matches = datefinder.find_dates(x)
					dt = [str(i).split(' ')[0].split('-') for i in matches]
					if dt != []:
						for dv in dt:
							if valid(dv):
								formatted_date = '-'.join(dv)
								return formatted_date
			else:
				return None
	#return none if no valid match found
	return None
