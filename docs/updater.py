import urllib.request
from html.parser import HTMLParser

# nightly url -> html -> string
webUrl  = urllib.request.urlopen('https://nightly.link/SuperMarcus/NineAnimator/workflows/nightly/master')	# url to html
html = webUrl.read().decode("utf-8")	# html to string

# html parser
class Parser(HTMLParser):
	# method to append the data between the tags to the list all_data.
	def handle_data(self, data):
		global all_data
		all_data.append(data)
all_data = []
# creating an instance of our class.
parser = Parser()
# providing the input.
parser.feed(html)

# filter the parsed html
list1 = ['iOS']	# filter
list2 = all_data	# input for filter

filtered = [n for n in list2 if	# the actual filtering
			any(m in n for m in list1)]
name = filtered[0]	# name of file
url = filtered[1]	# dl link for the file

# create shell script to install NineAnimator
with open('installer.sh', 'w') as f:	# create shell script and sets f to write mode
	f.write('echo \'Downloading App Archive\'\n')
	f.write('wget -q --no-check-certificate --content-disposition %s\n' % url)	# downloads nightly zip
	f.write('echo \'Download Complete\'\n')
	f.write('echo \'Unzipping Archive\'\n')
	f.write('unzip -q %s.zip\n' % name)	# unzip which outpus the ipa
	f.write('echo \'Unzip Complete\'\n')
	f.write('echo \'Rename Zip to IPA\'\n')
	f.write('mv %s.ipa app.zip\n' % name) # rename ipa
	f.write('echo \'Unzipping App\'\n')
	f.write('unzip -q app.zip\n')	# unzip which outputs the Payload
	f.write('echo \'Unzip Complete\'\n')
	f.write('echo \'Resigning App with ldid\'\n')
	f.write('ldid -S Payload/*.app\n') # run ldid on the Payload and .app folder
	f.write('echo \'Resign Complete\'\n')
	f.write('echo \'Rezipping App into IPA\'\n')
	f.write('zip -qr output.ipa Payload\n') # rezip the Payload folder into ipa
	f.write('echo \'Rezip Complete\'\n')
	f.write('appinst output.ipa\n') # install ipa via appsync using appinst
