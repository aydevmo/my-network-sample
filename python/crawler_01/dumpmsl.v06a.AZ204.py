#Note: This script downloads AZ-204 exam learning content from its website. 
#Note: This script does not intend to violate terms of use. Please refer to the link below before using. 
#      https://learn.microsoft.com/en-us/legal/termsofuse
#Note: This script writes to a file named tocsafewrite.htm in the end. That's the table of contents portion. 
#      This script also prints content on screen. The user needs to redirect the content to a file using shell features. 
#      Then combine the above two parts.  

from urllib import request, parse
import re
import io

path_base = "https://learn.microsoft.com/en-us/training/"

#modulebase = "https://learn.microsoft.com/en-us/training/modules/"

#url="https://learn.microsoft.com/en-us/certifications/exams/az-204"

#produce_content. True: Print all content. False: Skip content. Print section titles only. 
produce_content = True

text_exam = ""   #will be used below. #holds webpage text for processing.

toc = []   #table of contents

url_paths_raw = '''
	Line  537: 			<a class="card-title" id="learn.wwl.create-azure-app-service-web-apps_title" href="/en-us/training/paths/create-azure-app-service-web-apps/"><!---->AZ-204: Create Azure App Service web apps<!----></a>
	Line  584: 			<a class="card-title" id="learn.wwl.implement-azure-functions_title" href="/en-us/training/paths/implement-azure-functions/"><!---->AZ-204: Implement Azure Functions<!----></a>
	Line  627: 			<a class="card-title" id="learn.wwl.develop-solutions-that-use-blob-storage_title" href="/en-us/training/paths/develop-solutions-that-use-blob-storage/"><!---->AZ-204: Develop solutions that use Blob storage<!----></a>
	Line  670: 			<a class="card-title" id="learn.wwl.az-204-develop-solutions-that-use-azure-cosmos-db_title" href="/en-us/training/paths/az-204-develop-solutions-that-use-azure-cosmos-db/"><!---->AZ-204: Develop solutions that use Azure Cosmos DB<!----></a>
	Line  713: 			<a class="card-title" id="learn.wwl.az-204-implement-iaas-solutions_title" href="/en-us/training/paths/az-204-implement-iaas-solutions/"><!---->AZ-204: Implement infrastructure as a service solutions<!----></a>
	Line  756: 			<a class="card-title" id="learn.wwl.az-204-implement-authentication-authorization_title" href="/en-us/training/paths/az-204-implement-authentication-authorization/"><!---->AZ-204: Implement user authentication and authorization<!----></a>
	Line  799: 			<a class="card-title" id="learn.wwl.az-204-implement-secure-cloud-solutions_title" href="/en-us/training/paths/az-204-implement-secure-cloud-solutions/"><!---->AZ-204: Implement secure cloud solutions<!----></a>
	Line  842: 			<a class="card-title" id="learn.wwl.az-204-implement-api-management_title" href="/en-us/training/paths/az-204-implement-api-management/"><!---->AZ-204: Implement API Management<!----></a>
	Line  885: 			<a class="card-title" id="learn.wwl.az-204-develop-event-based-solutions_title" href="/en-us/training/paths/az-204-develop-event-based-solutions/"><!---->AZ-204: Develop event-based solutions<!----></a>
	Line  928: 			<a class="card-title" id="learn.wwl.az-204-develop-message-based-solutions_title" href="/en-us/training/paths/az-204-develop-message-based-solutions/"><!---->AZ-204: Develop message-based solutions<!----></a>
	Line  971: 			<a class="card-title" id="learn.wwl.az-204-instrument-solutions-to-support-monitoring-logging_title" href="/en-us/training/paths/az-204-instrument-solutions-support-monitoring-logging/"><!---->AZ-204: Instrument solutions to support monitoring and logging<!----></a>'''
	
#AZ-204 match <a class="card-title" id="learn.wwl.az-204-implement-secure-cloud-solutions_title" href="/en-us/training/paths/az-204-implement-secure-cloud-solutions/">
#str_pat = re.compile(r'<a class=\"card-title\" id=\".*\" href=\"\/en-us\/training\/(.*?)\"')
#learn_paths = str_pat.findall(url_paths_raw)

re_obj = re.compile(r'.*<a class=\"card-title\" id=\".*\" href=\"\/en-us\/training\/(.*?)\"><!---->(.*?)<!---->')

path_list = []              #Learning Path URL
path_title_list = []        #Learning Path Title

url_paths_raw = url_paths_raw.split('\n')

for line in url_paths_raw:
    tokens = re_obj.match(line)
    if tokens:
        path_list.append(path_base + tokens.group(1))
        path_title_list.append(tokens.group(2))

########## Learning Paths ##########
    
for mspath, path_title in zip(path_list, path_title_list):
    print("[Path] " + path_title + "<br/>")
    print(mspath + "<br/>")
    toc.append("<br/>[*Path] " + path_title + "<br/>");
    
    with request.urlopen(mspath) as f:
        text_exam= f.read().decode("utf-8")
        text_exam = text_exam.split('\n')
        
    #AZ-204 match <a href="../../modules/configure-web-app-settings/" class="is-hidden-tablet is-absolute-fills module-link" data-linktype="relative-path"></a>
    re_obj = re.compile(r'.*<a href=\"\.\.\/\.\.\/(.*?)\" class=\"is-hidden-tablet is-absolute-fills module-link\"')
    
    #AZ-204 match module title <h3 class="font-size-h6 margin-none has-content-margin-right-xxl-tablet">Explore Azure App Service</h3>
    re_obj_title = re.compile(r'.*<h3 class=\"font-size-h6 margin-none has-content-margin-right-xxl-tablet\">(.*?)<\/h3>')
    
    learn_modules = []
    module_titles = []
   
    for line in text_exam:
        tokens = re_obj.match(line)
        if tokens:
            relative_path = tokens.group(1)
            learn_modules.append( path_base + relative_path)
            
        tokens = re_obj_title.match(line)
        if tokens:
            title = tokens.group(1)
            module_titles.append( title )

########## Learning Modules ##########

    for msmodule,module_title in zip(learn_modules,module_titles):
        print("  [Module] " + module_title + "<br/>")
        toc.append("<br/>  [**Module] " + module_title + "<br/>")
    
        msmodule_url = msmodule
        print("  " + msmodule_url + "<br/>")
        
        text_exam = ""
        with request.urlopen(msmodule_url) as f:
            text_exam=f.read().decode("utf-8")
            text_exam = text_exam.split('\n')
        
        #AZ-204 match unit <a class="unit-title display-block font-size-md has-line-height-reset" href="3-azure-app-service-plans" data-linktype="relative-path">Examine Azure App Service plans</a>
        
        re_obj = re.compile(r'.*<a class=\"unit-title display-block font-size-md has-line-height-reset\" href=\"(.*?)\" data-linktype="relative-path">(.*?)</a>')
        
        learn_units=[]
        unit_titles=[]
        
        for line in text_exam:
            
            tokens = re_obj.match(line)
            
            if tokens:
                learn_units.append( msmodule + tokens.group(1))
                unit_titles.append(tokens.group(2))

########## Learning Units ##########

        for msunit,unit_title in zip(learn_units, unit_titles):
            print("<br/><a name='" + msunit + "'>    [Unit] " + unit_title + "</a><br/>")
            toc.append("<a href='#" + msunit + "'>    [Unit] " + unit_title + "</a><br/>\n")
        
            msunit_url = msunit
            print("    " + msunit_url + "<br/>")
            print()

            if not produce_content:
                continue  #disable unit content printing
            
            text_exam = ""
            
            with request.urlopen(msunit_url) as f:
                text_exam=f.read().decode('utf-8')
            
            s = io.StringIO(text_exam)
            
            toggle_content = False

            for line in s:
                #Below is a quick and dirty way to tell if the main content body has been reached.  
                if '<!-- <content> -->' in line or '<!-- </content> -->' in line:
                    toggle_content = not toggle_content
                if toggle_content:
                    try:
                        print(line)
                    except:
                        print(line.encode("utf-8"))
                    
                #UnicodeEncodeError: 'charmap' codec can't encode character '\u202f' in position 265: character maps to <undefined>
                #https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
            
    
toc.append("<br/>")
with open('tocsafewrite.htm','wt') as f:
    for entry in toc:
        f.write(entry)
        
    f.write("\n\n")
    f.write('<head><style>body {background-color: #c0c0c0;}</style></head> ')
    f.write("\n\n")

#print(toc)

