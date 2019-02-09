from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'Invoke-PortScan',

            'Author': ['Goude 2012, TrueSec'],

            'Description': ('Scan for IP-Addresses, HostNames and open Ports in your Network.'),

            'Background' : True,

            'OutputExtension' : None,
            
            'NeedsAdmin' : False,

            'OpsecSafe' : True,
            
            'Language' : 'powershell',

            'MinLanguageVersion' : '2',
            
            'Comments': [
                'https://raw.githubusercontent.com/samratashok/nishang/master/Scan/Invoke-PortScan.ps1'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'StartAddress' : {
                'Description'   :   "Start Address of the desired range.",
                'Required'      :   True,
                'Value'         :   ''
            },
            'EndAddress' : {
                'Description'   :   "End Address of the desired range.",
                'Required'      :   True,
                'Value'         :   ''
            },
            'ResolveHost' : {
                'Description'   :   "Resolves Hostnames",
                'Required'      :   False,
                'Value'         :   ''
            },
            'Ports' : {
                'Description'   :   "Ports That should be scanned, default values are: 21,22,23,53,69,71,80,98,110,139,111,389,443,445,1080,1433,2001,2049,3001,3128,5222,6667,6868,7777,7878,8080,1521,3306,3389,5801,5900,5555,5901",
                'Required'      :   False,
                'Value'         :   ''
            },
            'TimeOut' : {
                'Description'   :   "Time (in MilliSeconds) before TimeOut, Default set to 100",
                'Required'      :   False,
                'Value'         :   ''
            },
            'ScanPort' : {
                'Description'   :   "Perform a Port Scan",
                'Required'      :   False,
                'Value'         :   'true'
            }

        }    
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self, obfuscate=False, obfuscationCommand=""):

        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/situational_awareness/network/Invoke-PortScan.ps1"
        if obfuscate:
            helpers.obfuscate_module(moduleSource=moduleSource, obfuscationCommand=obfuscationCommand)
            moduleSource = moduleSource.replace("module_source", "obfuscated_module_source")
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        script = moduleCode

        scriptEnd = "Invoke-PortScan"

        for option,values in self.options.iteritems():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        # if we're just adding a switch
                        scriptEnd += " -" + str(option)
                    else:
                        scriptEnd += " -" + str(option) + " " + str(values['Value']) 

        if obfuscate:
            scriptEnd = helpers.obfuscate(self.mainMenu.installPath, psScript=scriptEnd, obfuscationCommand=obfuscationCommand)
        script += scriptEnd
        return script
