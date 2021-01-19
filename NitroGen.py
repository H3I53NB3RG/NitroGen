import random
import string
import requests
import subprocess
from colorama import Fore

class NitroGenerator:
        
    def __init__(self):
        self.banner()
        self.userInput()


    def banner(self):
        subprocess.call(["clear"])

        f = open("banner.txt","r")
        print(f.read())
        f.close()



    def userInput(self):
        #print(Fore.GREEN + '[+]' + Fore.RESET + ' Enter \'0\' If U Want This Script To Keep Running')
        numOfCodes = input(Fore.GREEN + '[+]' + Fore.RESET + ' Enter The Number Of Working Nitro Codes U Want To Generate : ') #Number of Codes To Generate
    
        if numOfCodes:
            try:
                numOfCodes = int(numOfCodes)
                if numOfCodes > 0:
                    print(Fore.GREEN + '[+]' + Fore.RESET + ' The Script Will Generate [' + Fore.GREEN + str(numOfCodes) + Fore.RESET + '] Working Nitro Codes')
                    self.check(numOfCodes)
                else:
                    print(Fore.GREEN + '[+]' + Fore.RESET + ' Zero ? For Real ?? Okay, Done!')
                    exit()
                
            except Exception as e:
                print(Fore.RED + '[-]' + Fore.RESET + ' This Must Be a Number WTF ?!')
                exit()
        else:
            print(Fore.RED + '[-]' + Fore.RESET + ' Maybe U Have To Enter The Number OF Codes To Generate ?!')
            exit()


    def breakLoop(self, numOfCodes, numOfworkingCodes):
        if numOfworkingCodes == numOfCodes:
            print('=' * 78)
            print(Fore.GREEN + '[+]' + Fore.RESET + ' Done! Generated ' + str(numOfworkingCodes) + 'Working Nitro Codes')
            exit()


    def gencode(self):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(16))


    def check(self, numOfCodes):       
        numOfGeneratedCodes = 0 #Number of Nitro Codes The Script Will Generate And Check
        numOfworkingCodes = 0 #Number of Working Codes The Script Generated
        
        proxy_list = []

        with open('proxy_list.txt') as f:
            proxy_list = f.readlines()

        for proxy in proxy_list:
                proxies = {'https': proxy.strip()}
                print('=' * 78)
                print(Fore.GREEN + '[+]' + Fore.RESET + ' Connecting To : [' + proxy[7:-1] + '] ...')

                #Genrating The Firt Code
                code = self.gencode()

                try:
                        #Starting a Session With This Proxy
                        session = requests.Session()
                        session.proxies.update(proxies)

                        print(Fore.GREEN + '[+]' + Fore.RESET + ' Session Started!')

                        while True:
                                response = session.get('https://discord.com/api/v7/entitlements/gift-codes/' + code + '?with_application=false&with_subscription_plan=true')
                                data = response.json()

                                if data["message"] == 'Unknown Gift Code':
                                        numOfGeneratedCodes += 1

                                        
                                        print(Fore.RED + Fore.RED + '[-]' + Fore.RESET + '' + Fore.RESET + ' Invalid Code : ' + code + '\t\t\t\t\t[' + Fore.GREEN + str(numOfGeneratedCodes) + ']')
                                        self.breakLoop(numOfCodes, numOfworkingCodes)
                                        
                                elif data["message"] == 'You are being rate limited.':
                                        print(Fore.RED + '[-]' + Fore.RESET + ' Proxy Is Being Rate Limited, Switching Proxy')
                                        break
                                    
                                else:
                                        numOfGeneratedCodes += 1
                                        numOfworkingCodes += 1

                                        print(Fore.GREEN + '[+]' + Fore.RESET + ' Valid Code : ' + code + '\t\t\t\t\t[' + Fore.GREEN + str(numOfGeneratedCodes) + ']')
                                        
                                        file = open("workedcodes.txt", "a+")
                                        file.write("\n" + code + "\t" + data["subscription_plan"]["name"] + "\t" + data["expires_at"]) 

                                        self.breakLoop(numOfCodes, numOfworkingCodes)
                                
                                code = self.gencode()
                                
                except Exception as e:
                        print(Fore.RED + '[-]' + Fore.RESET + ' Faild To Connect, Switching Proxy ...')
                        continue

        print('=' * 78)
        print(Fore.RED + '[-]' + Fore.RESET + ' No More Proxies To Use')
        print(Fore.GREEN + '[+]' + Fore.RESET + ' Number Of Genrated Codes : ' + str(numOfGeneratedCodes)) 
        print(Fore.GREEN + '[+]' + Fore.RESET + ' Number Of Working Codes : ' + str(numOfworkingCodes))


NitroGenerator()
